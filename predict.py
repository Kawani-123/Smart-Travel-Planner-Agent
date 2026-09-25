"""
Predict Routes — Trip cost prediction via trained Random Forest ML model.
"""

from flask import Blueprint, jsonify, request
from services.predict_service import predict_trip_cost

predict_bp = Blueprint("predict", __name__)


@predict_bp.post("/cost")
def predict_cost_endpoint():
    """
    Predict trip cost using the trained Random Forest model.
    Expects JSON body: destination, days, travelers, transport_type, hotel_type
    """
    data = request.get_json(silent=True) or {}

    destination    = str(data.get("destination", "")).strip()
    transport_type = str(data.get("transport_type", "flight")).strip()
    hotel_type     = str(data.get("hotel_type", "standard")).strip()

    try:
        days      = int(data.get("days", 0))
        travelers = int(data.get("travelers", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "days and travelers must be integers."}), 422

    if not destination:
        return jsonify({"error": "destination is required."}), 422
    if not (1 <= days <= 30):
        return jsonify({"error": "days must be between 1 and 30."}), 422
    if not (1 <= travelers <= 20):
        return jsonify({"error": "travelers must be between 1 and 20."}), 422

    try:
        result = predict_trip_cost(
            destination=destination,
            days=days,
            travelers=travelers,
            transport_type=transport_type,
            hotel_type=hotel_type,
        )
        return jsonify(result)
    except FileNotFoundError as e:
        return jsonify({"error": f"ML model not trained yet. Run: python ml/train.py — {e}"}), 503
    except ValueError as e:
        return jsonify({"error": str(e)}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@predict_bp.get("/destinations")
def valid_destinations():
    """Return the list of destinations the ML model supports."""
    return jsonify({
        "destinations":    ["Goa", "Jaipur", "Kerala", "Shimla", "Andaman", "Ladakh"],
        "transport_types": ["flight", "train", "bus"],
        "hotel_types":     ["budget", "standard", "luxury"],
    })
