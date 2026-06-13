"""
==========================================================================
🏆 CLASH ROYALE DECK ANALYZER - Meta Routes
==========================================================================

REST API endpoints for meta-level statistics and trends.

Endpoints:
    GET /meta/summary       → Overall meta stats
    GET /meta/popular       → Most popular cards
    GET /meta/underrated    → Underrated cards
    GET /meta/archetypes    → Archetype distribution
    GET /meta/trends        → Meta trends across seasons
    GET /meta/top-decks     → Top performing decks
"""

from flask import Blueprint, jsonify, request
from backend.services.meta_analyzer import MetaAnalyzer
from backend.utils.logger import get_logger

logger = get_logger(__name__)

meta_bp = Blueprint("meta", __name__, url_prefix="/meta")

_meta_analyzer: MetaAnalyzer = None


def get_meta_analyzer() -> MetaAnalyzer:
    """Get or create MetaAnalyzer instance."""
    global _meta_analyzer
    if _meta_analyzer is None:
        _meta_analyzer = MetaAnalyzer()
    return _meta_analyzer


# ============================================================================
# 📊 ROUTES
# ============================================================================

@meta_bp.route("/summary", methods=["GET"])
def get_summary():
    """Get overall meta summary."""
    try:
        analyzer = get_meta_analyzer()
        return jsonify({
            "success": True,
            "summary": analyzer.get_meta_summary()
        }), 200
    except Exception as e:
        logger.error(f"Error in get_summary: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@meta_bp.route("/popular", methods=["GET"])
def get_popular_cards():
    """Get most popular cards."""
    try:
        n = request.args.get("n", default=10, type=int)
        analyzer = get_meta_analyzer()
        return jsonify({
            "success": True,
            "top_n": n,
            "cards": analyzer.get_most_popular_cards(n)
        }), 200
    except Exception as e:
        logger.error(f"Error in get_popular_cards: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@meta_bp.route("/underrated", methods=["GET"])
def get_underrated_cards():
    """Get underrated cards (high win rate, low usage)."""
    try:
        n = request.args.get("n", default=10, type=int)
        analyzer = get_meta_analyzer()
        return jsonify({
            "success": True,
            "top_n": n,
            "cards": analyzer.get_underrated_cards(n)
        }), 200
    except Exception as e:
        logger.error(f"Error in get_underrated_cards: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@meta_bp.route("/archetypes", methods=["GET"])
def get_archetypes():
    """Get archetype distribution and performance."""
    try:
        analyzer = get_meta_analyzer()
        return jsonify({
            "success": True,
            "distribution": analyzer.get_archetype_distribution(),
            "performance": analyzer.get_archetype_performance()
        }), 200
    except Exception as e:
        logger.error(f"Error in get_archetypes: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@meta_bp.route("/trends", methods=["GET"])
def get_trends():
    """Get meta trends across seasons."""
    try:
        analyzer = get_meta_analyzer()
        return jsonify({
            "success": True,
            "trends": analyzer.get_meta_trends()
        }), 200
    except Exception as e:
        logger.error(f"Error in get_trends: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@meta_bp.route("/top-decks", methods=["GET"])
def get_top_decks():
    """Get top performing decks."""
    try:
        n = request.args.get("n", default=10, type=int)
        analyzer = get_meta_analyzer()
        return jsonify({
            "success": True,
            "top_n": n,
            "decks": analyzer.get_top_decks(n)
        }), 200
    except Exception as e:
        logger.error(f"Error in get_top_decks: {e}")
        return jsonify({"success": False, "error": str(e)}), 500