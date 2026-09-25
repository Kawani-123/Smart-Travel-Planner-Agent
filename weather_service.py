"""
Weather Service — OpenWeather API integration.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
BASE_URL = "https://api.openweathermap.org/data/2.5"

# Map Indian destination names to city names that OpenWeather recognises
CITY_MAP = {
    "Andaman": "Port Blair",
    "Kerala": "Thiruvananthapuram",
    "Ladakh": "Leh",
    "Shimla": "Shimla",
    "Jaipur": "Jaipur",
    "Goa": "Panaji",
}


def _resolve_city(city: str) -> str:
    return CITY_MAP.get(city.strip().title(), city.strip())


def get_weather(city: str) -> dict:
    """Fetch current weather for a city."""
    if not API_KEY:
        return _mock_weather(city)

    resolved = _resolve_city(city)
    try:
        resp = requests.get(
            f"{BASE_URL}/weather",
            params={"q": f"{resolved},IN", "appid": API_KEY, "units": "metric"},
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        return {
            "city": city,
            "resolved_city": resolved,
            "temperature": round(data["main"]["temp"]),
            "feels_like": round(data["main"]["feels_like"]),
            "humidity": data["main"]["humidity"],
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "icon_url": f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
            "wind_speed": data["wind"]["speed"],
            "visibility": data.get("visibility", 0) // 1000,
            "sunrise": data["sys"]["sunrise"],
            "sunset": data["sys"]["sunset"],
            "country": data["sys"]["country"],
        }
    except requests.exceptions.HTTPError as e:
        # Any API error (401 invalid key, 404 city not found, etc.) → use mock
        print(f"[WARN] Weather API HTTP error ({e.response.status_code}), using mock data.")
        return _mock_weather(city)
    except Exception as e:
        print(f"[WARN] Weather API error: {e}, using mock data.")
        return _mock_weather(city)


def get_forecast(city: str, days: int = 5) -> dict:
    """Fetch multi-day weather forecast."""
    if not API_KEY:
        return _mock_forecast(city, days)

    resolved = _resolve_city(city)
    try:
        resp = requests.get(
            f"{BASE_URL}/forecast",
            params={
                "q": f"{resolved},IN",
                "appid": API_KEY,
                "units": "metric",
                "cnt": days * 8,  # 3-hour intervals
            },
            timeout=10,
        )
        resp.raise_for_status()
        data = resp.json()

        # Group by day
        daily = {}
        for item in data["list"]:
            date = item["dt_txt"].split(" ")[0]
            if date not in daily:
                daily[date] = {
                    "date": date,
                    "temps": [],
                    "descriptions": [],
                    "humidity": [],
                    "icons": [],
                }
            daily[date]["temps"].append(item["main"]["temp"])
            daily[date]["descriptions"].append(item["weather"][0]["description"])
            daily[date]["humidity"].append(item["main"]["humidity"])
            daily[date]["icons"].append(item["weather"][0]["icon"])

        forecast_list = []
        for date, info in list(daily.items())[:days]:
            forecast_list.append({
                "date": date,
                "temp_min": round(min(info["temps"])),
                "temp_max": round(max(info["temps"])),
                "humidity": round(sum(info["humidity"]) / len(info["humidity"])),
                "description": max(set(info["descriptions"]), key=info["descriptions"].count).title(),
                "icon": info["icons"][0],
                "icon_url": f"https://openweathermap.org/img/wn/{info['icons'][0]}@2x.png",
            })

        return {"city": city, "forecast": forecast_list}
    except requests.exceptions.HTTPError as e:
        # Any API error → fall back to mock forecast
        print(f"[WARN] Forecast API HTTP error ({e.response.status_code}), using mock data.")
        return _mock_forecast(city, days)
    except Exception as e:
        print(f"[WARN] Forecast API error: {e}, using mock data.")
        return _mock_forecast(city, days)


# ── Mock responses (when API key is missing / for demos) ──────────────────────

MOCK_WEATHER_DATA = {
    "Goa":     {"temp": 30, "feels_like": 34, "humidity": 75, "desc": "Partly Cloudy", "icon": "02d", "wind": 4.2},
    "Jaipur":  {"temp": 28, "feels_like": 31, "humidity": 40, "desc": "Clear Sky",    "icon": "01d", "wind": 3.5},
    "Kerala":  {"temp": 27, "feels_like": 30, "humidity": 85, "desc": "Humid & Warm", "icon": "02d", "wind": 5.1},
    "Shimla":  {"temp": 12, "feels_like":  9, "humidity": 60, "desc": "Cool & Clear", "icon": "01d", "wind": 6.0},
    "Andaman": {"temp": 29, "feels_like": 33, "humidity": 80, "desc": "Tropical Heat","icon": "04d", "wind": 4.8},
    "Ladakh":  {"temp":  8, "feels_like":  4, "humidity": 30, "desc": "Cold & Dry",   "icon": "01d", "wind": 7.2},
}


def _mock_weather(city: str) -> dict:
    m = MOCK_WEATHER_DATA.get(city.title(), {"temp": 25, "feels_like": 27, "humidity": 60, "desc": "Clear Sky", "icon": "01d", "wind": 3.0})
    return {
        "city": city,
        "resolved_city": city,
        "temperature": m["temp"],
        "feels_like": m["feels_like"],
        "humidity": m["humidity"],
        "description": m["desc"],
        "icon": m["icon"],
        "icon_url": f"https://openweathermap.org/img/wn/{m['icon']}@2x.png",
        "wind_speed": m["wind"],
        "visibility": 10,
        "country": "IN",
        "note": "Mock data — add OPENWEATHER_API_KEY to .env for real data",
    }


def _mock_forecast(city: str, days: int) -> dict:
    base = MOCK_WEATHER_DATA.get(city.title(), {"temp": 25, "feels_like": 27, "humidity": 60, "desc": "Clear Sky", "icon": "01d", "wind": 3.0})
    from datetime import datetime, timedelta
    forecast = []
    for i in range(days):
        date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
        forecast.append({
            "date": date,
            "temp_min": base["temp"] - 3,
            "temp_max": base["temp"] + 2,
            "humidity": base["humidity"],
            "description": base["desc"],
            "icon": base["icon"],
            "icon_url": f"https://openweathermap.org/img/wn/{base['icon']}@2x.png",
        })
    return {"city": city, "forecast": forecast, "note": "Mock data — add OPENWEATHER_API_KEY to .env for real data"}
