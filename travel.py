"""
Travel Routes — Destination information and recommendations.
"""

from flask import Blueprint, jsonify, request
from services.destination_service import get_destination_info, get_all_destinations

travel_bp = Blueprint("travel", __name__)


@travel_bp.get("/destinations")
def list_destinations():
    """Return all supported destinations."""
    return jsonify({"destinations": get_all_destinations()})


@travel_bp.get("/destination/<name>")
def destination_detail(name: str):
    """Return detailed info for a specific destination."""
    info = get_destination_info(name)
    if not info:
        return jsonify({"error": f"Destination '{name}' not found."}), 404
    return jsonify(info)


@travel_bp.get("/recommend")
def recommend():
    """Recommend destinations based on budget, days, and interests."""
    try:
        budget    = int(request.args.get("budget", 0))
        days      = int(request.args.get("days", 0))
        travelers = int(request.args.get("travelers", 0))
        interests = request.args.get("interests", "")
    except (TypeError, ValueError):
        return jsonify({"error": "budget, days, travelers must be integers."}), 400

    if not (budget and days and travelers):
        return jsonify({"error": "budget, days, and travelers are required."}), 400
    if not (1 <= days <= 30):
        return jsonify({"error": "days must be between 1 and 30."}), 400
    if not (1 <= travelers <= 20):
        return jsonify({"error": "travelers must be between 1 and 20."}), 400

    from services.destination_service import recommend_destinations
    recs = recommend_destinations(budget, days, travelers, interests)
    return jsonify({"recommendations": recs})
