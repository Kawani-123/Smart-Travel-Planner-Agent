"""
run.py — Use THIS to start the server (not app.py directly via flask CLI).
This guarantees debug mode and reloader are OFF, preventing the WinError 10038.

Usage:
    python run.py
"""
import os

# Force these BEFORE importing Flask/app — overrides any .env or CLI flags
os.environ["FLASK_DEBUG"] = "0"
os.environ["FLASK_ENV"] = "production"

from app import app, _init_knowledge_base

if __name__ == "__main__":
    print("🚀  Smart Travel Planner (Flask) starting...")
    print("📦  Loading ChromaDB knowledge base...")
    _init_knowledge_base()

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))

    print(f"\n✅  Server ready!")
    print(f"🌐  Open in browser  →  http://localhost:{port}")
    print(f"🔌  API base         →  http://localhost:{port}/api")
    print(f"❤️   Health check    →  http://localhost:{port}/health")
    print(f"\n🛑  Press Ctrl+C to stop\n")

    app.run(
        host=host,
        port=port,
        debug=False,        # NO debug mode — prevents watchdog reloader
        threaded=True,      # Handle multiple requests concurrently
        use_reloader=False, # NO file watcher — prevents WinError 10038
    )
