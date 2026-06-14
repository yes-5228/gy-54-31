GPA_RULES = [
    (90, 4.0, "A"),
    (85, 3.7, "A-"),
    (82, 3.3, "B+"),
    (78, 3.0, "B"),
    (75, 2.7, "B-"),
    (72, 2.3, "C+"),
    (68, 2.0, "C"),
    (64, 1.5, "C-"),
    (60, 1.0, "D"),
    (0, 0.0, "F"),
]


def _match_rule(score):
    score = float(score)
    for threshold, point, letter in GPA_RULES:
        if score >= threshold:
            return point, letter
    return 0.0, "F"


def score_to_point(score):
    return _match_rule(score)[0]


def score_to_letter(score):
    return _match_rule(score)[1]


def enrich_grade_gpa(grade_dict):
    score = grade_dict["score"]
    grade_dict["gpaPoint"] = score_to_point(score)
    grade_dict["letter"] = score_to_letter(score)
    return grade_dict


def calculate_summary(grades):
    total_credit = sum(grade.credit for grade in grades)
    weighted_points = sum(grade.credit * score_to_point(grade.score) for grade in grades)
    passed_credit = sum(grade.credit for grade in grades if grade.score >= 60)
    return {
        "courseCount": len(grades),
        "totalCredit": round(total_credit, 2),
        "passedCredit": round(passed_credit, 2),
        "gpa": round(weighted_points / total_credit, 2) if total_credit else 0,
        "averageScore": round(sum(grade.score for grade in grades) / len(grades), 2) if grades else 0,
    }
