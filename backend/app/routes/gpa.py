from flask import Blueprint, jsonify

from ..services.gpa import list_rules

gpa_bp = Blueprint("gpa", __name__)


@gpa_bp.get("/rules")
def get_rules():
    return jsonify(list_rules())
