"""
Itinerary Routes — AI-generated day-wise travel itinerary using IBM watsonx.ai.
"""

from flask import Blueprint, jsonify, request
from services.itinerary_service import generate_itinerary_sync

itinerary_bp = Blueprint("itinerary", __name__)


@itinerary_bp.post("/generate")
def generate():
    """
    Generate a full day-wise itinerary using IBM watsonx.ai Llama 3.3 model,
    augmented with RAG context from ChromaDB.
    """
    data = request.get_json(silent=True) or {}

    source         = str(data.get("source", "")).strip()
    destination    = str(data.get("destination", "")).strip()
    transport_type = str(data.get("transport_type", "flight")).strip()
    hotel_type     = str(data.get("hotel_type", "standard")).strip()
    interests      = data.get("interests", [])
    if isinstance(interests, str):
        interests = [i.strip() for i in interests.split(",") if i.strip()]

    try:
        budget    = int(data.get("budget", 0))
        days      = int(data.get("days", 0))
        travelers = int(data.get("travelers", 0))
    except (TypeError, ValueError):
        return jsonify({"error": "budget, days, and travelers must be integers."}), 422

    if not source:
        return jsonify({"error": "source is required."}), 422
    if not destination:
        return jsonify({"error": "destination is required."}), 422
    if budget < 1000:
        return jsonify({"error": "budget must be at least 1000."}), 422
    if not (1 <= days <= 30):
        return jsonify({"error": "days must be between 1 and 30."}), 422
    if not (1 <= travelers <= 20):
        return jsonify({"error": "travelers must be between 1 and 20."}), 422

    try:
        result = generate_itinerary_sync(
            source=source,
            destination=destination,
            budget=budget,
            days=days,
            travelers=travelers,
            interests=interests,
            transport_type=transport_type,
            hotel_type=hotel_type,
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
