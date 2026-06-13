"""
==========================================================================
🏆 CLASH ROYALE DECK ANALYZER - Main Flask Application
==========================================================================

Application factory pattern for clean Flask app initialization.

Run:
    python -m backend.app
    OR
    python backend/app.py
"""

from flask import Flask, jsonify
from flask_cors import CORS
from backend.config.settings import Config
from backend.utils.logger import get_logger

# Import all route blueprints
from backend.routes.card_routes import card_bp
from backend.routes.deck_routes import deck_bp
from backend.routes.meta_routes import meta_bp
from backend.routes.recommendation_routes import recommend_bp

# Pre-load ML models (cached for fast requests)
from backend.ml.model_loader import ModelLoader

logger = get_logger(__name__)


def create_app() -> Flask:
    """
    Application factory function.

    Returns:
        Flask: Configured Flask app instance
    """
    app = Flask(__name__)

    # ── CORS ────────────────────────────────────────────
    CORS(app, origins=Config.CORS_ORIGINS)

    # ── Configuration ────────────────────────────────────
    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_REQUEST_SIZE

    # ── Pre-load ML models at startup ───────────────────
    logger.info("🚀 Pre-loading ML models...")
    ModelLoader()  # Singleton - loads once
    logger.info("✅ ML models ready!")

    # ── Register Blueprints ─────────────────────────────
    api_prefix = Config.API_PREFIX

    app.register_blueprint(card_bp, url_prefix=f"{api_prefix}/cards")
    app.register_blueprint(deck_bp, url_prefix=f"{api_prefix}/decks")
    app.register_blueprint(meta_bp, url_prefix=f"{api_prefix}/meta")
    app.register_blueprint(recommend_bp, url_prefix=f"{api_prefix}/recommend")

    # ── Root endpoint ───────────────────────────────────
    @app.route("/")
    def root():
        """Welcome endpoint."""
        return jsonify({
            "name": "🏆 Clash Royale Deck Analyzer API",
            "version": "1.0.0",
            "status": "running",
            "api_prefix": api_prefix,
            "endpoints": {
                "health": f"{api_prefix}/health",
                "cards": f"{api_prefix}/cards",
                "decks": f"{api_prefix}/decks/analyze",
                "meta": f"{api_prefix}/meta/summary",
                "recommend": f"{api_prefix}/recommend/full"
            },
            "documentation": "https://github.com/ShauryaSingh1709/Clash-Royale"
        }), 200

    # ── Health check ────────────────────────────────────
    @app.route(f"{api_prefix}/health")
    def health():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "service": "Clash Royale Deck Analyzer API",
            "ml_models_loaded": True
        }), 200

    # ── Error handlers ──────────────────────────────────
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "Endpoint not found",
            "code": 404
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": "Method not allowed",
            "code": 405
        }), 405

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Internal server error: {error}")
        return jsonify({
            "success": False,
            "error": "Internal server error",
            "code": 500
        }), 500

    logger.info("=" * 60)
    logger.info("🏆 CLASH ROYALE DECK ANALYZER API")
    logger.info("=" * 60)
    logger.info(f"📡 Server: http://{Config.HOST}:{Config.PORT}")
    logger.info(f"🌐 API Prefix: {api_prefix}")
    logger.info(f"🐛 Debug Mode: {Config.DEBUG}")
    logger.info("=" * 60)

    return app


# ============================================================================
# 🚀 RUN SERVER
# ============================================================================

if __name__ == "__main__":
    app = create_app()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )