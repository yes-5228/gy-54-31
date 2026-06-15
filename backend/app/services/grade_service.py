from ..extensions import db
from ..models import Grade, Student
from .gpa import (
    GPA_RULES,
    calculate_summary,
    DEFAULT_RULE,
    enrich_grade_gpa,
    resolve_rule_name,
)
from .appeal_service import enrich_grade_appeal_status, get_latest_appeal_status


def build_grade_view(grade, rule_name=None):
    college = grade.student.college
    resolved_rule = resolve_rule_name(college=college, rule_name=rule_name)
    rule_meta = GPA_RULES.get(resolved_rule, GPA_RULES[DEFAULT_RULE])
    rule_display = rule_meta["name"]

    data = grade.to_dict()

    enrich_grade_gpa(data, resolved_rule)
    enrich_grade_appeal_status(data, grade)

    basic = {
        "id": data["id"],
        "student": data["student"],
        "courseCode": data["courseCode"],
        "courseName": data["courseName"],
        "credit": data["credit"],
        "score": data["score"],
        "semester": data["semester"],
        "teacher": data["teacher"],
        "createdAt": data["createdAt"],
        "updatedAt": data["updatedAt"],
    }

    gpa = {
        "ruleKey": resolved_rule,

        "ruleName": rule_display,
        "point": data["gpaPoint"],
        "letter": data["letter"],
    }

    appeal = {
        "status": get_latest_appeal_status(grade),
    }

    data["basic"] = basic
    data["gpa"] = gpa
    data["appeal"] = appeal

    return data


def build_grade_views(grades, rule_name=None):
    return [build_grade_view(grade, rule_name) for grade in grades]


def list_grades():
    return Grade.query.order_by(Grade.updated_at.desc()).all()


def get_or_create_student(student_no, name, college="", major="", class_name=""):
    student = Student.query.filter_by(student_no=student_no).first()
    if student:
        student.name = name or student.name
        student.college = college if college is not None else student.college
        student.major = major if major is not None else student.major
        student.class_name = class_name if class_name is not None else student.class_name
        return student

    student = Student(
        student_no=student_no,
        name=name,
        college=college or "",
        major=major or "",
        class_name=class_name or "",
    )
    db.session.add(student)
    return student


def create_grade(payload):
    student = get_or_create_student(
        payload["studentNo"],
        payload["studentName"],
        payload.get("college", ""),
        payload.get("major", ""),
        payload.get("className", ""),
    )
    grade = Grade(
        student=student,
        course_code=payload["courseCode"],
        course_name=payload["courseName"],
        credit=float(payload["credit"]),
        score=float(payload["score"]),
        semester=payload["semester"],
        teacher=payload["teacher"],
    )
    db.session.add(grade)
    db.session.commit()
    return grade


def update_grade(grade, payload):
    if "courseCode" in payload:
        grade.course_code = payload["courseCode"]
    if "courseName" in payload:
        grade.course_name = payload["courseName"]
    if "credit" in payload:
        grade.credit = float(payload["credit"])
    if "score" in payload:
        grade.score = float(payload["score"])
    if "semester" in payload:
        grade.semester = payload["semester"]
    if "teacher" in payload:
        grade.teacher = payload["teacher"]
    db.session.commit()
    return grade


def get_transcript(student_no, rule_name=None):
    student = Student.query.filter_by(student_no=student_no).first()
    if not student:
        return None

    grades = Grade.query.filter_by(student_id=student.id).order_by(Grade.semester.desc(), Grade.course_code).all()

    resolved_rule = resolve_rule_name(college=student.college, rule_name=rule_name)
    rule_meta = GPA_RULES.get(resolved_rule, GPA_RULES[DEFAULT_RULE])

    summary = calculate_summary(grades, resolved_rule)
    summary["ruleKey"] = resolved_rule
    summary["ruleName"] = rule_meta["name"]

    return {
        "student": student.to_dict(),
        "ruleKey": resolved_rule,
        "ruleName": rule_meta["name"],
        "summary": summary,
        "grades": build_grade_views(grades, rule_name=resolved_rule),
    }
