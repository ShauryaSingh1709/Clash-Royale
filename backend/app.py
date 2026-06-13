"""
==========================================================================
🏆 CLASH ROYALE DECK ANALYZER - Main Flask Application
==========================================================================

Application factory pattern + serves frontend HTML pages.

Run:
    python -m backend.app
"""

from pathlib import Path
from flask import Flask, jsonify, send_from_directory, render_template
from flask_cors import CORS
from backend.config.settings import Config
from backend.utils.logger import get_logger

# Import all route blueprints
from backend.routes.card_routes import card_bp
from backend.routes.deck_routes import deck_bp
from backend.routes.meta_routes import meta_bp
from backend.routes.recommendation_routes import recommend_bp

# Pre-load ML models
from backend.ml.model_loader import ModelLoader

logger = get_logger(__name__)

# Frontend path
FRONTEND_DIR: Path = Config.BASE_DIR / "frontend"


def create_app() -> Flask:
    """Application factory function."""
    app = Flask(
        __name__,
        static_folder=str(FRONTEND_DIR),
        static_url_path="/static"
    )

    # ── CORS ────────────────────────────────────────────
    CORS(app, origins=Config.CORS_ORIGINS)

    # ── Configuration ────────────────────────────────────
    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_REQUEST_SIZE

    # ── Pre-load ML models at startup ───────────────────
    logger.info("🚀 Pre-loading ML models...")
    ModelLoader()
    logger.info("✅ ML models ready!")

    # ── Register API Blueprints ─────────────────────────
    api_prefix = Config.API_PREFIX

    app.register_blueprint(card_bp, url_prefix=f"{api_prefix}/cards")
    app.register_blueprint(deck_bp, url_prefix=f"{api_prefix}/decks")
    app.register_blueprint(meta_bp, url_prefix=f"{api_prefix}/meta")
    app.register_blueprint(recommend_bp, url_prefix=f"{api_prefix}/recommend")

    # ════════════════════════════════════════════════════
    # 🎨 FRONTEND ROUTES (Serve HTML pages)
    # ════════════════════════════════════════════════════

    @app.route("/")
    def home():
        """Serve home page."""
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.route("/analyzer")
    def analyzer():
        """Serve deck analyzer page."""
        return send_from_directory(FRONTEND_DIR, "analyzer.html")

    @app.route("/cards")
    def cards():
        """Serve cards explorer page."""
        return send_from_directory(FRONTEND_DIR, "cards.html")

    @app.route("/dashboard")
    def dashboard():
        """Serve meta dashboard page."""
        return send_from_directory(FRONTEND_DIR, "dashboard.html")

    @app.route("/about")
    def about():
        """Serve about page."""
        return send_from_directory(FRONTEND_DIR, "about.html")
    
    @app.route("/docs")
    def docs():
        return send_from_directory(FRONTEND_DIR, "docs.html")

    @app.route("/api-reference")
    @app.route("/api")
    def api_reference():
        return send_from_directory(FRONTEND_DIR, "api.html")

    @app.route("/tutorials")
    def tutorials():
        return send_from_directory(FRONTEND_DIR, "tutorials.html")

    @app.route("/contributing")
    def contributing():
        return send_from_directory(FRONTEND_DIR, "contributing.html")

    @app.route("/bugs")
    def bugs():
        return send_from_directory(FRONTEND_DIR, "bugs.html")
    
    @app.route("/privacy")
    def privacy():
        return send_from_directory(FRONTEND_DIR, "privacy.html")

    @app.route("/terms")
    def terms():
        return send_from_directory(FRONTEND_DIR, "terms.html")

    # ── API Health Check ─────────────────────────────────
    @app.route(f"{api_prefix}/health")
    def health():
        return jsonify({
            "status": "healthy",
            "service": "Clash Royale Deck Analyzer API",
            "ml_models_loaded": True
        }), 200

    # ── API Info endpoint ────────────────────────────────
    @app.route(f"{api_prefix}")
    def api_info():
        return jsonify({
            "name": "🏆 Clash Royale Deck Analyzer API",
            "version": "1.0.0",
            "status": "running",
            "endpoints": {
                "cards": f"{api_prefix}/cards",
                "decks": f"{api_prefix}/decks/analyze",
                "meta": f"{api_prefix}/meta/summary",
                "recommend": f"{api_prefix}/recommend/full"
            }
        }), 200

    # ── Error handlers ──────────────────────────────────
    @app.errorhandler(404)
    def not_found(error):
        # If API path, return JSON
        from flask import request
        if request.path.startswith(api_prefix):
            return jsonify({
                "success": False,
                "error": "Endpoint not found",
                "code": 404
            }), 404
        # Otherwise serve home page (SPA-like)
        return send_from_directory(FRONTEND_DIR, "index.html")

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "code": 500
        }), 500

    logger.info("=" * 60)
    logger.info("🏆 CLASH ROYALE DECK ANALYZER")
    logger.info("=" * 60)
    logger.info(f"📡 Server: http://{Config.HOST}:{Config.PORT}")
    logger.info(f"🎨 Frontend served from: {FRONTEND_DIR}")
    logger.info(f"🌐 API Prefix: {api_prefix}")
    logger.info("=" * 60)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )