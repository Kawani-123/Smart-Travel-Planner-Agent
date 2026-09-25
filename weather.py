"""
Weather Routes — Current weather and forecast for destinations.
"""

from flask import Blueprint, jsonify, request
from services.weather_service import get_weather, get_forecast

weather_bp = Blueprint("weather", __name__)


@weather_bp.get("/current")
def current_weather():
    """Fetch current weather for a city using OpenWeather API."""
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "city query parameter is required."}), 400
    data = get_weather(city)
    if "error" in data:
        return jsonify({"error": data["error"]}), 502
    return jsonify(data)


@weather_bp.get("/forecast")
def weather_forecast():
    """Fetch N-day forecast for a city."""
    city = request.args.get("city", "").strip()
    try:
        days = int(request.args.get("days", 5))
    except (TypeError, ValueError):
        return jsonify({"error": "days must be an integer."}), 400

    if not city:
        return jsonify({"error": "city query parameter is required."}), 400
    if not (1 <= days <= 7):
        return jsonify({"error": "days must be between 1 and 7."}), 400

    data = get_forecast(city, days)
    if "error" in data:
        return jsonify({"error": data["error"]}), 502
    return jsonify(data)
