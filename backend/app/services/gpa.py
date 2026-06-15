GPA_RULES = {
    "default": {
        "name": "通用标准（4.0 制）",
        "rules": [
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
        ],
    },
    "engineering": {
        "name": "工学院标准（严格4.0制）",
        "rules": [
            (95, 4.0, "A"),
            (90, 3.7, "A-"),
            (85, 3.3, "B+"),
            (80, 3.0, "B"),
            (75, 2.7, "B-"),
            (70, 2.3, "C+"),
            (66, 2.0, "C"),
            (62, 1.5, "C-"),
            (60, 1.0, "D"),
            (0, 0.0, "F"),
        ],
    },
    "arts": {
        "name": "文学院标准（宽松4.0制）",
        "rules": [
            (85, 4.0, "A"),
            (80, 3.7, "A-"),
            (77, 3.3, "B+"),
            (73, 3.0, "B"),
            (70, 2.7, "B-"),
            (67, 2.3, "C+"),
            (63, 2.0, "C"),
            (60, 1.5, "C-"),
            (58, 1.0, "D"),
            (0, 0.0, "F"),
        ],
    },
    "business": {
        "name": "商学院标准（4.3制）",
        "rules": [
            (90, 4.3, "A+"),
            (85, 4.0, "A"),
            (82, 3.7, "A-"),
            (78, 3.3, "B+"),
            (75, 3.0, "B"),
            (72, 2.7, "B-"),
            (68, 2.3, "C+"),
            (64, 2.0, "C"),
            (60, 1.7, "C-"),
            (0, 0.0, "F"),
        ],
    },
}


COLLEGE_TO_RULE = {
    "计算机学院": "default",
    "计算机科学与技术学院": "default",
    "工学院": "engineering",
    "机械工程学院": "engineering",
    "电子信息学院": "engineering",
    "文学院": "arts",
    "外国语学院": "arts",
    "新闻传播学院": "arts",
    "商学院": "business",
    "经济管理学院": "business",
    "管理学院": "business",
}


DEFAULT_RULE = "default"


def resolve_rule_name(college=None, rule_name=None):
    if rule_name and rule_name in GPA_RULES:
        return rule_name
    if college:
        mapped = COLLEGE_TO_RULE.get(college)
        if mapped:
            return mapped
        for key, value in COLLEGE_TO_RULE.items():
            if key in college or college in key:
                return value
    return DEFAULT_RULE


def list_rules():
    return [
        {"key": key, "name": value["name"]} for key, value in GPA_RULES.items()
    ]


def _get_rules(rule_name):
    rule_name = rule_name or DEFAULT_RULE
    return GPA_RULES.get(rule_name, GPA_RULES[DEFAULT_RULE])["rules"]


def _match_rule(score, rule_name=None):
    score = float(score)
    for threshold, point, letter in _get_rules(rule_name):
        if score >= threshold:
            return point, letter
    return 0.0, "F"


def score_to_point(score, rule_name=None):
    return _match_rule(score, rule_name)[0]


def score_to_letter(score, rule_name=None):
    return _match_rule(score, rule_name)[1]


def calculate_summary(grades, rule_name=None):
    total_credit = sum(grade.credit for grade in grades)
    weighted_points = sum(grade.credit * score_to_point(grade.score, rule_name) for grade in grades)
    passed_credit = sum(grade.credit for grade in grades if grade.score >= 60)
    return {
        "courseCount": len(grades),
        "totalCredit": round(total_credit, 2),
        "passedCredit": round(passed_credit, 2),
        "gpa": round(weighted_points / total_credit, 2) if total_credit else 0,
        "averageScore": round(sum(grade.score for grade in grades) / len(grades), 2) if grades else 0,
    }
