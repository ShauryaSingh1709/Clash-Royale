"""
==========================================================================
🏆 CLASH ROYALE DECK ANALYZER - Recommendation Routes
==========================================================================

REST API endpoints for smart deck recommendations.

Endpoints:
    POST /recommend/similar       → Find similar decks
    POST /recommend/improvements  → Suggest card improvements
    POST /recommend/full          → Complete recommendation report
"""

from flask import Blueprint, jsonify, request
from backend.services.recommendation_engine import RecommendationEngine
from backend.utils.logger import get_logger

logger = get_logger(__name__)

recommend_bp = Blueprint("recommend", __name__, url_prefix="/recommend")

_engine: RecommendationEngine = None


def get_engine() -> RecommendationEngine:
    """Get or create RecommendationEngine instance."""
    global _engine
    if _engine is None:
        _engine = RecommendationEngine()
    return _engine


def _extract_deck_from_request() -> tuple[list, str]:
    """Helper to extract deck from JSON request."""
    data = request.get_json()
    if not data:
        return None, "Request body must be JSON"
    cards = data.get("cards")
    if not cards:
        return None, "Field 'cards' is required (list of 8 card names)"
    return cards, None


# ============================================================================
# 💡 ROUTES
# ============================================================================

@recommend_bp.route("/similar", methods=["POST"])
def find_similar():
    """
    Find decks similar to user's deck.

    Request body:
        {
            "cards": ["Hog Rider", ...],
            "top_n": 5
        }
    """
    try:
        cards, error = _extract_deck_from_request()
        if error:
            return jsonify({"success": False, "error": error}), 400

        data = request.get_json()
        top_n = data.get("top_n", 5)

        engine = get_engine()
        result = engine.find_similar_decks(cards, top_n=top_n)

        status_code = 200 if result["success"] else 400
        return jsonify(result), status_code

    except Exception as e:
        logger.error(f"Error in find_similar: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@recommend_bp.route("/improvements", methods=["POST"])
def suggest_improvements():
    """
    Suggest improvements for user's deck.

    Request body:
        {
            "cards": ["Hog Rider", ...],
            "top_n": 3
        }
    """
    try:
        cards, error = _extract_deck_from_request()
        if error:
            return jsonify({"success": False, "error": error}), 400

        data = request.get_json()
        top_n = data.get("top_n", 3)

        engine = get_engine()
        result = engine.suggest_improvements(cards, top_n=top_n)

        status_code = 200 if result["success"] else 400
        return jsonify(result), status_code

    except Exception as e:
        logger.error(f"Error in suggest_improvements: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@recommend_bp.route("/full", methods=["POST"])
def full_recommendation():
    """
    Get complete recommendation report (everything).

    Request body:
        {
            "cards": ["Hog Rider", ...]
        }
    """
    try:
        cards, error = _extract_deck_from_request()
        if error:
            return jsonify({"success": False, "error": error}), 400

        engine = get_engine()
        result = engine.get_full_recommendation(cards)

        status_code = 200 if result["success"] else 400
        return jsonify(result), status_code

    except Exception as e:
        logger.error(f"Error in full_recommendation: {e}")
        return jsonify({"success": False, "error": str(e)}), 500