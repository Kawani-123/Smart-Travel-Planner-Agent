"""
Smart Travel Planner — Flask Backend
Serves the frontend AND the REST API.

IMPORTANT: Run via:  python run.py
           NOT via:  flask run  (which enables debug/reloader by default)
"""

import os

# Block Flask debug/reloader at the module level — must be before Flask import
os.environ["FLASK_DEBUG"] = "0"
os.environ["FLASK_ENV"] = "production"

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT  = os.getenv("ENVIRONMENT", "development")
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:8000")

# ── App ───────────────────────────────────────────────────────────────────────
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)
app.config["DEBUG"] = False

CORS(app, origins="*" if ENVIRONMENT == "development" else [FRONTEND_URL])

# ── Blueprints ────────────────────────────────────────────────────────────────
from routes.travel    import travel_bp
from routes.weather   import weather_bp
from routes.predict   import predict_bp
from routes.itinerary import itinerary_bp

app.register_blueprint(travel_bp,    url_prefix="/api/travel")
app.register_blueprint(weather_bp,   url_prefix="/api/weather")
app.register_blueprint(predict_bp,   url_prefix="/api/predict")
app.register_blueprint(itinerary_bp, url_prefix="/api/itinerary")

# ── Favicon ───────────────────────────────────────────────────────────────────
@app.get("/favicon.ico")
def favicon():
    from flask import send_from_directory
    return send_from_directory(app.static_folder, "favicon.ico", mimetype="image/x-icon")

# ── Frontend ──────────────────────────────────────────────────────────────────
@app.get("/")
def index():
    return render_template("index.html")

# ── Health ────────────────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return jsonify({"status": "ok", "version": "1.0.0"})

# ── 404 ───────────────────────────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    if request.path.startswith("/api/"):
        return jsonify({"error": "Endpoint not found"}), 404
    return render_template("index.html"), 404

# ── ChromaDB init ─────────────────────────────────────────────────────────────
def _init_knowledge_base():
    try:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "chroma_db")
        if not os.path.exists(db_path):
            print("[STARTUP] Building RAG knowledge base...")
            from rag.knowledge_base import build_knowledge_base
            build_knowledge_base()
            print("[STARTUP] Knowledge base ready.")
        else:
            print("[STARTUP] ChromaDB knowledge base: OK")
    except Exception as e:
        print(f"[WARN] ChromaDB init skipped: {e}")

# ── Entry point (use run.py instead) ─────────────────────────────────────────
if __name__ == "__main__":
    print("⚠️  Running via app.py directly. Use 'python run.py' for best results.")
    _init_knowledge_base()
    app.run(
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        debug=False,
        threaded=True,
        use_reloader=False,
    )
