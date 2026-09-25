"""
Destination Service — Static destination data + recommendation logic.
"""

from typing import Optional

DESTINATIONS = {
    "Goa": {
        "name": "Goa",
        "state": "Goa",
        "region": "West India",
        "type": ["beach", "nightlife", "heritage", "food"],
        "best_season": "November – February",
        "language": "Konkani, English, Hindi",
        "currency": "INR",
        "avg_budget_per_day": {"budget": 1500, "standard": 3500, "luxury": 10000},
        "highlights": [
            "Baga & Calangute Beach",
            "Dudhsagar Waterfalls",
            "Basilica of Bom Jesus",
            "Fort Aguada",
            "Anjuna Flea Market",
        ],
        "image_url": "https://images.unsplash.com/photo-1614082242765-7c98ca0f3df3?w=600",
        "description": (
            "India's beach paradise — vibrant nightlife, colonial heritage, "
            "stunning coastline, and unforgettable seafood await you."
        ),
        "tags": ["beach", "party", "history", "seafood", "water sports"],
    },
    "Jaipur": {
        "name": "Jaipur",
        "state": "Rajasthan",
        "region": "North India",
        "type": ["heritage", "culture", "shopping", "food"],
        "best_season": "October – March",
        "language": "Rajasthani, Hindi",
        "currency": "INR",
        "avg_budget_per_day": {"budget": 1200, "standard": 3000, "luxury": 12000},
        "highlights": [
            "Amber Fort",
            "Hawa Mahal",
            "City Palace",
            "Jantar Mantar",
            "Chokhi Dhani",
        ],
        "image_url": "https://images.unsplash.com/photo-1524492412937-b28074a5d7da?w=600",
        "description": (
            "The Pink City of India — royal forts, vibrant bazaars, "
            "majestic palaces, and the rich tapestry of Rajputana culture."
        ),
        "tags": ["history", "culture", "shopping", "royalty", "architecture"],
    },
    "Kerala": {
        "name": "Kerala",
        "state": "Kerala",
        "region": "South India",
        "type": ["nature", "backwaters", "wellness", "food"],
        "best_season": "October – February",
        "language": "Malayalam",
        "currency": "INR",
        "avg_budget_per_day": {"budget": 1500, "standard": 4000, "luxury": 12000},
        "highlights": [
            "Alleppey Backwaters",
            "Munnar Tea Gardens",
            "Fort Kochi",
            "Periyar Wildlife Sanctuary",
            "Varkala Beach",
        ],
        "image_url": "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?w=600",
        "description": (
            "God's Own Country — serene backwaters, misty hill stations, "
            "Ayurvedic retreats, and the most delicious coconut-based cuisine."
        ),
        "tags": ["nature", "houseboat", "ayurveda", "tea", "wildlife"],
    },
    "Shimla": {
        "name": "Shimla",
        "state": "Himachal Pradesh",
        "region": "North India",
        "type": ["hill station", "adventure", "heritage", "nature"],
        "best_season": "March – June / December – February",
        "language": "Hindi, Pahadi",
        "currency": "INR",
        "avg_budget_per_day": {"budget": 1000, "standard": 2500, "luxury": 8000},
        "highlights": [
            "Mall Road",
            "The Ridge",
            "Jakhu Temple",
            "Kufri Ski Resort",
            "Toy Train (Kalka–Shimla)",
        ],
        "image_url": "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=600",
        "description": (
            "The Queen of Hill Stations — snow-covered peaks, Victorian architecture, "
            "the famous toy train, and crisp Himalayan air."
        ),
        "tags": ["snow", "hills", "heritage", "trekking", "skiing"],
    },
    "Andaman": {
        "name": "Andaman",
        "state": "Andaman & Nicobar Islands",
        "region": "Bay of Bengal",
        "type": ["beach", "water sports", "history", "nature"],
        "best_season": "October – May",
        "language": "Hindi, Bengali, Tamil, Telugu",
        "currency": "INR",
        "avg_budget_per_day": {"budget": 2500, "standard": 5000, "luxury": 15000},
        "highlights": [
            "Radhanagar Beach",
            "Cellular Jail",
            "Havelock Island",
            "Scuba Diving & Snorkelling",
            "Ross Island",
        ],
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=600",
        "description": (
            "A tropical paradise in the Bay of Bengal — pristine beaches, "
            "vibrant coral reefs, rich colonial history, and world-class diving."
        ),
        "tags": ["diving", "snorkelling", "beaches", "history", "coral reefs"],
    },
    "Ladakh": {
        "name": "Ladakh",
        "state": "Ladakh (UT)",
        "region": "North India (Himalayan)",
        "type": ["adventure", "culture", "nature", "trekking"],
        "best_season": "June – September",
        "language": "Ladakhi, Hindi, Urdu",
        "currency": "INR",
        "avg_budget_per_day": {"budget": 2000, "standard": 4500, "luxury": 12000},
        "highlights": [
            "Pangong Tso Lake",
            "Nubra Valley & Bactrian Camels",
            "Thiksey Monastery",
            "Khardung La Pass",
            "Magnetic Hill",
        ],
        "image_url": "https://images.unsplash.com/photo-1609766857413-5597df5c4b73?w=600",
        "description": (
            "The Land of High Passes — otherworldly landscapes, "
            "ancient Buddhist monasteries, crystal-clear high-altitude lakes, "
            "and the ultimate adventure on earth."
        ),
        "tags": ["mountains", "adventure", "buddhism", "trekking", "lakes"],
    },
}


def get_all_destinations() -> list:
    """Return list of all destination names with basic info."""
    return [
        {
            "name": d["name"],
            "state": d["state"],
            "region": d["region"],
            "tags": d["tags"],
            "description": d["description"],
            "image_url": d["image_url"],
            "best_season": d["best_season"],
        }
        for d in DESTINATIONS.values()
    ]


def get_destination_info(name: str) -> Optional[dict]:
    """Return full info for a destination."""
    return DESTINATIONS.get(name.strip().title())


def recommend_destinations(
    budget: int,
    days: int,
    travelers: int,
    interests: str,
) -> list:
    """
    Score and rank destinations based on user inputs.

    Scoring criteria:
    - Budget fit (estimated cost vs provided budget)
    - Interest tag match
    """
    interest_list = [i.strip().lower() for i in interests.split(",") if i.strip()]
    scored = []

    for dest in DESTINATIONS.values():
        hotel = "budget" if budget // travelers // days < 2000 else (
            "luxury" if budget // travelers // days > 6000 else "standard"
        )
        daily_cost = dest["avg_budget_per_day"].get(hotel, dest["avg_budget_per_day"]["standard"])
        estimated_total = daily_cost * days * travelers

        budget_score = max(0, 100 - abs(estimated_total - budget) / budget * 100)

        tag_matches = sum(
            1
            for interest in interest_list
            if any(interest in tag for tag in dest["tags"])
        )
        interest_score = min(tag_matches * 25, 100)

        total_score = (budget_score * 0.5) + (interest_score * 0.5)

        scored.append({
            **dest,
            "match_score": round(total_score),
            "estimated_total_cost": estimated_total,
            "recommended_hotel": hotel,
        })

    scored.sort(key=lambda x: x["match_score"], reverse=True)
    return scored[:4]
