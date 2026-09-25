"""
Itinerary Service — IBM watsonx.ai Llama 3.3 70B + ChromaDB RAG.
"""

import os
from typing import List
from dotenv import load_dotenv

load_dotenv()

IBM_API_KEY = os.getenv("IBM_API_KEY", "")
PROJECT_ID  = os.getenv("PROJECT_ID", "")
IBM_REGION  = os.getenv("IBM_REGION", "au-syd")

WATSONX_URL = f"https://{IBM_REGION}.ml.cloud.ibm.com"


# ── IBM watsonx.ai auth ───────────────────────────────────────────────────────

def _get_iam_token() -> str:
    """Exchange IBM API key for IAM bearer token."""
    import requests
    resp = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "apikey": IBM_API_KEY,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=15,
    )
    resp.raise_for_status()
    return resp.json()["access_token"]


def _call_watsonx(prompt: str, max_new_tokens: int = 2048) -> str:
    """Call IBM watsonx.ai text generation endpoint."""
    import requests

    token = _get_iam_token()

    payload = {
        "model_id": "meta-llama/llama-3-3-70b-instruct",
        "input": prompt,
        "parameters": {
            "decoding_method": "greedy",
            "max_new_tokens": max_new_tokens,
            "temperature": 0.7,
            "repetition_penalty": 1.1,
        },
        "project_id": PROJECT_ID,
    }

    resp = requests.post(
        f"{WATSONX_URL}/ml/v1/text/generation?version=2023-05-29",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        timeout=120,
    )
    resp.raise_for_status()
    return resp.json()["results"][0]["generated_text"]


# ── RAG retrieval ─────────────────────────────────────────────────────────────

def _get_rag_context(destination: str, interests: List[str]) -> str:
    """Retrieve relevant travel knowledge from ChromaDB (thread-safe)."""
    try:
        import sys
        RAG_DIR = os.path.normpath(os.path.join(os.path.dirname(__file__), "../rag"))
        if RAG_DIR not in sys.path:
            sys.path.insert(0, RAG_DIR)
        from knowledge_base import query_knowledge_base

        query = f"{destination} travel tips attractions food budget {' '.join(interests)}"
        docs = query_knowledge_base(query, destination=destination, n_results=4)
        return "\n\n".join(docs) if docs else ""
    except RuntimeError as e:
        # ChromaDB thread pool shuts down during interpreter exit — safe to ignore
        print(f"[WARN] RAG skipped (thread pool shutdown): {e}")
        return ""
    except Exception as e:
        print(f"[WARN] RAG retrieval failed: {e}")
        return ""


# ── Prompt builder ────────────────────────────────────────────────────────────

def _build_prompt(
    source: str,
    destination: str,
    budget: int,
    days: int,
    travelers: int,
    interests: List[str],
    transport_type: str,
    hotel_type: str,
    rag_context: str,
) -> str:
    interests_str = ", ".join(interests) if interests else "general sightseeing"

    context_section = ""
    if rag_context:
        context_section = f"""
## Reference Knowledge Base:
{rag_context}

Use the above knowledge base information to make the itinerary accurate, specific, and detailed.
"""

    return f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
You are an expert Indian travel planner with deep knowledge of all Indian destinations.
You create detailed, practical, and exciting travel itineraries.
Always use Indian Rupees (₹) for all costs.
Format your response exactly as instructed.
<|eot_id|><|start_header_id|>user<|end_header_id|>

Create a complete {days}-day travel itinerary for the following trip:

**Trip Details:**
- From: {source}
- Destination: {destination}
- Total Budget: ₹{budget:,}
- Duration: {days} days
- Travelers: {travelers} person(s)
- Budget per person: ₹{budget // travelers:,}
- Transport: {transport_type}
- Accommodation: {hotel_type} hotel
- Interests: {interests_str}
{context_section}

**Provide the following in your response:**

### 🗺️ Day-wise Itinerary
For each day (Day 1 through Day {days}), provide:
- Morning activity with time and cost
- Afternoon activity with time and cost
- Evening activity with time and cost
- Recommended dinner spot with approximate cost

### 💡 Travel Tips
Provide 5 practical travel tips specific to {destination}.

### 💰 Budget Breakdown
Provide a detailed budget breakdown:
- Transport cost (total)
- Accommodation cost (per night × {days} nights)
- Food cost (per day × {days} days)
- Activities & sightseeing
- Shopping & miscellaneous
- Total estimated cost

### 🍽️ Food Recommendations
List 5 must-try dishes and 3 recommended restaurants with price range.

### 📋 Packing Checklist
Provide a destination-specific packing list with 10 essential items.

<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""


# ── Mock response (when no IBM credentials) ───────────────────────────────────

def _mock_itinerary(destination: str, days: int, budget: int, travelers: int) -> str:
    per_person = budget // travelers
    return f"""### 🗺️ Day-wise Itinerary

**Day 1 — Arrival & Orientation**
- 🌅 Morning (09:00): Arrive at {destination}, check in to hotel. Freshen up and have a local breakfast (~₹200/person)
- ☀️ Afternoon (13:00): Explore the main market area and local landmarks (~₹500 entry fees)
- 🌆 Evening (18:00): Sunset visit to the most iconic viewpoint. Enjoy local snacks
- 🍽️ Dinner (20:00): Authentic local restaurant — try the regional speciality (~₹400/person)

**Day 2 — Key Attractions**
- 🌅 Morning (08:00): Visit the top heritage/nature site (book tickets in advance, ~₹300/person)
- ☀️ Afternoon (13:00): Guided tour of secondary attraction (~₹500 with guide)
- 🌆 Evening (17:00): Cultural show or local market (~₹200–400)
- 🍽️ Dinner (20:00): Highly-rated local restaurant (~₹500/person)

**Day 3 — Day Trip / Adventure**
- 🌅 Morning (07:00): Early morning day trip to nearby nature spot (~₹1500 including transport)
- ☀️ Afternoon (14:00): Return and relax at hotel / beach / hill
- 🌆 Evening (18:00): Shopping for local souvenirs (~₹500–1000)
- 🍽️ Dinner (20:00): Farewell dinner at the best-reviewed restaurant (~₹600/person)

{"".join([f"""
**Day {d} — Explore & Relax**
- 🌅 Morning: Explore nearby village or hidden gem (~₹300)
- ☀️ Afternoon: Leisure time, water sports or trekking (~₹800)
- 🌆 Evening: Rooftop cafe or local hangout (~₹300)
- 🍽️ Dinner: Street food trail (~₹250/person)
""" for d in range(4, days + 1)])}

### 💡 Travel Tips
1. 📅 Book accommodation and transport at least 2 weeks in advance for best prices
2. 💱 Carry sufficient cash — many local shops and eateries don't accept cards
3. 🌡️ Check the weather forecast before each day and dress accordingly
4. 🗺️ Download offline Google Maps of {destination} before you arrive
5. 📸 Visit popular spots early morning to avoid crowds and get great photos

### 💰 Budget Breakdown
| Category | Cost (Total) |
|---|---|
| Transport (flights/trains) | ₹{int(budget * 0.30):,} |
| Accommodation ({days} nights) | ₹{int(budget * 0.30):,} |
| Food & Dining | ₹{int(budget * 0.20):,} |
| Activities & Entry Fees | ₹{int(budget * 0.12):,} |
| Shopping & Miscellaneous | ₹{int(budget * 0.08):,} |
| **Total Estimated Cost** | **₹{budget:,}** |

Per person: ₹{per_person:,}

### 🍽️ Food Recommendations

**Must-Try Dishes:**
1. Local staple dish 1 — the region's most famous food
2. Street food specialty — available on every corner
3. Traditional dessert — a sweet you can't leave without trying
4. Seafood/vegetarian specialty — fresh and locally sourced
5. Breakfast item — the perfect way to start each day

**Recommended Restaurants:**
- 🌟 Fine Dining Option: Premium experience (₹1000–2000/person)
- 🍴 Mid-range Favourite: Great food, great value (₹400–700/person)
- 🥘 Budget Gem: Authentic local flavours (₹150–300/person)

### 📋 Packing Checklist
1. ✅ Valid Government ID (Aadhaar/Passport)
2. ✅ Comfortable walking shoes
3. ✅ Sunscreen SPF 50+
4. ✅ Reusable water bottle
5. ✅ Light cotton/warm clothes (season appropriate)
6. ✅ Power bank for phone
7. ✅ First aid kit and personal medicines
8. ✅ Camera or phone with ample storage
9. ✅ Cash (₹5000 emergency fund)
10. ✅ Travel insurance documents

*Note: This is a demo itinerary. Add your IBM_API_KEY to .env for AI-powered personalized itineraries using Llama 3.3 70B.*"""


# ── Main service function (SYNC — Flask compatible) ───────────────────────────

def generate_itinerary_sync(
    source: str,
    destination: str,
    budget: int,
    days: int,
    travelers: int,
    interests: List[str],
    transport_type: str,
    hotel_type: str,
) -> dict:
    """
    Generate a complete travel itinerary (synchronous version for Flask).
    Uses IBM watsonx.ai if credentials are available, else returns rich mock data.
    """
    # Get RAG context synchronously
    rag_context = _get_rag_context(destination, interests)

    itinerary_text = ""
    source_used = "ibm_watsonx"

    if IBM_API_KEY and PROJECT_ID:
        try:
            prompt = _build_prompt(
                source, destination, budget, days, travelers,
                interests, transport_type, hotel_type, rag_context
            )
            itinerary_text = _call_watsonx(prompt)
            source_used = "ibm_watsonx_llama33"
        except Exception as e:
            print(f"[WARN] watsonx.ai call failed: {e}. Falling back to mock.")
            itinerary_text = _mock_itinerary(destination, days, budget, travelers)
            source_used = "mock_fallback"
    else:
        itinerary_text = _mock_itinerary(destination, days, budget, travelers)
        source_used = "demo_mock"

    return {
        "destination": destination,
        "source": source,
        "days": days,
        "travelers": travelers,
        "budget": budget,
        "interests": interests,
        "itinerary": itinerary_text,
        "rag_context_used": bool(rag_context),
        "model_source": source_used,
    }


# Keep async version as alias for backward compat
async def generate_itinerary(*args, **kwargs):
    return generate_itinerary_sync(*args, **kwargs)
