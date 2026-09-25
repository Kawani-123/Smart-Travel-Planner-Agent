<div align="center">

# ✈️ Smart Travel Planner Agent

### AI-Powered Personalized Travel Planning System

[![Flask](https://img.shields.io/badge/Backend-Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![IBM watsonx](https://img.shields.io/badge/LLM-IBM_watsonx.ai-1F70C1?style=for-the-badge&logo=ibm&logoColor=white)](https://www.ibm.com/watsonx)
[![ChromaDB](https://img.shields.io/badge/VectorDB-ChromaDB-F97316?style=for-the-badge)](https://docs.trychroma.com)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)
[![Render](https://img.shields.io/badge/Deployed_on-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)

**[🌐 Live Demo](https://smart-travel-planner-agent.onrender.com)** &nbsp;•&nbsp; **[📂 GitHub Repository](https://github.com/Goldi-Insights/Smart-Travel-Planner-Agent)**

</div>

---

## 📌 Overview

The **Smart Travel Planner Agent** eliminates the complexity of traditional travel planning — where users have to juggle multiple websites for weather, costs, guides, and itineraries — by consolidating everything into a single intelligent platform.

It uses a **multi-agent AI architecture** powered by IBM watsonx.ai, LangFlow, ChromaDB, and Scikit-Learn to deliver seamless, personalized travel plans in seconds.

---

## ✨ Key Features

| Feature | Description |
|---|---|
| 🤖 **Personalized AI Planning** | Custom itineraries generated based on user preferences, budget & destination |
| 📍 **Destination Recommendation** | AI-powered destination matching tailored to traveler interests |
| 💰 **ML Cost Prediction** | Random Forest Regressor estimates flights, hotels & transport costs |
| 🌦️ **Real-Time Weather** | Live weather data via OpenWeather API for climate-aware planning |
| 📚 **RAG Knowledge Base** | ChromaDB semantic search fetches destination guides & travel tips |
| 🏗️ **Multi-Agent Architecture** | Specialized agents work in sequence, each owning a distinct planning task |
| 🧠 **IBM watsonx.ai LLM** | Llama 3.3 70B Instruct generates fluent, contextually rich travel plans |
| 🔁 **LangFlow Orchestration** | Visual workflow builder for the entire multi-agent pipeline |

---

## 🏗️ System Architecture

```
User
 │
 ▼
Frontend UI (HTML / CSS / JS)
 │
 ▼
Flask Backend (REST API)
 │
 ├──▶ Input Parser Agent       → Extracts travel preferences
 ├──▶ Destination Agent        → Recommends best destinations
 ├──▶ Weather Agent            → Fetches real-time forecast (OpenWeather API)
 ├──▶ Cost Prediction Agent    → Estimates expenses (Random Forest ML)
 ├──▶ RAG Knowledge Agent      → Retrieves destination info (ChromaDB)
 └──▶ Travel Concierge Agent   → Aggregates all outputs
              │
              ▼
     IBM watsonx.ai (Llama 3.3 70B)
              │
              ▼
     Personalized Day-by-Day Itinerary
```

---

## 🛠️ Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | Flask, REST APIs |
| **AI / LLM** | IBM watsonx.ai — Llama 3.3 70B Instruct |
| **Machine Learning** | Random Forest Regressor, Scikit-Learn |
| **RAG / Vector DB** | ChromaDB, LangChain |
| **External APIs** | OpenWeather API |
| **Workflow Orchestration** | LangFlow |
| **Deployment** | Render |
| **Version Control** | GitHub |

---

## 📂 Project Structure

```
Smart-Travel-Planner-Agent/
├── app.py                      ← Flask entry point
├── requirements.txt            ← Python dependencies
├── .env                        ← API keys & config (not committed)
│
├── routes/
│   ├── travel.py               ← /api/travel/* — destinations & recommendations
│   ├── weather.py              ← /api/weather/* — current weather & forecast
│   ├── predict.py              ← /api/predict/* — ML cost prediction
│   └── itinerary.py            ← /api/itinerary/* — AI itinerary generation
│
├── services/
│   ├── destination_service.py
│   ├── weather_service.py
│   ├── predict_service.py
│   └── itinerary_service.py
│
├── ml/
│   ├── train.py                ← Run once to train the ML model
│   └── predict.py              ← ML inference logic
│
├── rag/
│   └── knowledge_base.py       ← ChromaDB RAG setup
│
├── data/
│   ├── dataset.csv
│   └── chroma_db/              ← Vector DB (auto-created on first run)
│
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- IBM watsonx.ai account (API key + Project ID)
- OpenWeather API key

### 1. Clone the Repository

```bash
git clone https://github.com/Goldi-Insights/Smart-Travel-Planner-Agent.git
cd Smart-Travel-Planner-Agent
```

### 2. Create & Activate Virtual Environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root directory and fill in your credentials:

```env
IBM_API_KEY=your_ibm_api_key_here
PROJECT_ID=your_watsonx_project_id
IBM_REGION=au-syd                    # Options: us-south, eu-de, jp-tok, au-syd

OPENWEATHER_API_KEY=your_openweather_key

API_HOST=0.0.0.0
API_PORT=8000
FRONTEND_URL=http://localhost:5500
ENVIRONMENT=development
```

### 5. Train the ML Model *(one-time step)*

```bash
python ml/train.py
```

### 6. Start the Flask Server

```bash
python app.py
```

The API will be available at **`http://localhost:8000`**

Open `frontend/index.html` using a local server (e.g., VS Code Live Server on port **5500**).

---

## 📡 API Reference

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | API info |
| `GET` | `/health` | Server health check |

---

### Travel — `/api/travel`

| Method | Endpoint | Parameters |
|--------|----------|------------|
| `GET` | `/api/travel/destinations` | — |
| `GET` | `/api/travel/destination/<name>` | `name` e.g. `Goa` |
| `GET` | `/api/travel/recommend` | `budget`, `days`, `travelers`, `interests` |

---

### Weather — `/api/weather`

| Method | Endpoint | Parameters |
|--------|----------|------------|
| `GET` | `/api/weather/current` | `city` |
| `GET` | `/api/weather/forecast` | `city`, `days` (1–7) |

---

### Cost Prediction — `/api/predict`

| Method | Endpoint | Body (JSON) |
|--------|----------|-------------|
| `POST` | `/api/predict/cost` | `destination`, `days`, `travelers`, `transport_type`, `hotel_type` |
| `GET` | `/api/predict/destinations` | — |

**Example:**

```bash
curl -X POST http://localhost:8000/api/predict/cost \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "Goa",
    "days": 5,
    "travelers": 2,
    "transport_type": "flight",
    "hotel_type": "standard"
  }'
```

---

### Itinerary Generation — `/api/itinerary`

| Method | Endpoint | Body (JSON) |
|--------|----------|-------------|
| `POST` | `/api/itinerary/generate` | `source`, `destination`, `budget`, `days`, `travelers`, `interests[]`, `transport_type`, `hotel_type` |

**Example:**

```bash
curl -X POST http://localhost:8000/api/itinerary/generate \
  -H "Content-Type: application/json" \
  -d '{
    "source": "Mumbai",
    "destination": "Goa",
    "budget": 25000,
    "days": 5,
    "travelers": 2,
    "interests": ["beaches", "food"],
    "transport_type": "flight",
    "hotel_type": "standard"
  }'
```

---

## 🤖 Multi-Agent Workflow

| Step | Agent | Responsibility |
|------|-------|----------------|
| 1 | **Input Parser Agent** | Extracts travel preferences — destination, duration, budget, accommodation |
| 2 | **Destination Agent** | Recommends destinations tailored to user needs |
| 3 | **Weather Agent** | Fetches real-time weather conditions via OpenWeather API |
| 4 | **Cost Prediction Agent** | Estimates total trip expenses using the trained ML model |
| 5 | **RAG Knowledge Agent** | Retrieves destination guides and travel tips from ChromaDB |
| 6 | **Travel Concierge Agent** | Aggregates all agent outputs into a unified prompt |
| 7 | **IBM watsonx.ai** | Generates the final personalized day-by-day travel itinerary |

---

## 🧠 ML Cost Prediction Model

A **Random Forest Regressor** was trained on a custom travel cost dataset. It accepts five features:

- **Destination** — Location-specific cost factors
- **Duration** — Number of travel days
- **Travelers** — Group size (accounts for discounts)
- **Transport Mode** — Air / Train / Bus / Car
- **Hotel Category** — Budget / Standard / Luxury

Random Forest was chosen for its robustness against overfitting, ability to model non-linear relationships, and interpretability via feature importance.

---

## 🔄 Key Changes: FastAPI → Flask

| Feature | FastAPI (Original) | Flask (This Version) |
|---|---|---|
| Framework | `FastAPI` | `Flask` |
| CORS | `fastapi.middleware.cors` | `flask-cors` |
| Routers | `APIRouter` | `Blueprint` |
| Request Params | Pydantic models / `Query()` | `request.args` / `request.get_json()` |
| Responses | Auto-serialized | `jsonify()` |
| Async Routes | Native `async def` | `asyncio.run()` wrapper |
| Validation | Pydantic + FastAPI | Manual checks |
| Auto Docs | `/docs` (Swagger UI) | Not included — use Postman |

---

## 🔮 Future Roadmap

- [ ] Hotel & Flight booking integration (Booking.com / Skyscanner / Amadeus APIs)
- [ ] Native iOS & Android mobile application
- [ ] Voice-based travel assistant (Alexa / Google Assistant)
- [ ] Multi-language support (Hindi, Spanish, French, Mandarin)
- [ ] Collaborative filtering for advanced personalized recommendations
- [ ] Real-time travel expense tracker
- [ ] Social features — share itineraries & community-curated routes

---

## 📚 References

- [IBM watsonx.ai Documentation](https://www.ibm.com/watsonx)
- [LangFlow Documentation](https://docs.langflow.org)
- [ChromaDB Documentation](https://docs.trychroma.com)
- [OpenWeather API](https://openweathermap.org/api)
- [Scikit-Learn Documentation](https://scikit-learn.org/stable)
- [Flask Documentation](https://flask.palletsprojects.com)
- [LangChain Documentation](https://python.langchain.com)

---

<div align="center">

Developed by Goldi using IBM watsonx.ai • LangFlow • ChromaDB • Scikit-Learn

**[⭐ Star this repo if you found it useful!](https://github.com/Goldi-Insights/Smart-Travel-Planner-Agent)**

</div>
