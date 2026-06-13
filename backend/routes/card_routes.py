"""
==========================================================================
🏆 CLASH ROYALE DECK ANALYZER - Card Routes
==========================================================================

REST API endpoints for card-related queries.

Endpoints:
    GET /cards                  → All cards
    GET /cards/<name>           → Single card details
    GET /cards/search?q=query   → Search cards
    GET /cards/top/win-rate     → Top by win rate
    GET /cards/top/usage        → Top by usage
    GET /cards/stats            → Overall card statistics
"""

from flask import Blueprint, jsonify, request
from backend.services.card_analyzer import CardAnalyzer
from backend.utils.logger import get_logger

logger = get_logger(__name__)

# Create Blueprint
card_bp = Blueprint("cards", __name__, url_prefix="/cards")

# Initialize service (singleton-like)
_card_analyzer: CardAnalyzer = None


def get_card_analyzer() -> CardAnalyzer:
    """Get or create CardAnalyzer instance."""
    global _card_analyzer
    if _card_analyzer is None:
        _card_analyzer = CardAnalyzer()
    return _card_analyzer


# ============================================================================
# 📋 ROUTES
# ============================================================================

@card_bp.route("", methods=["GET"])
def get_all_cards():
    """Get all cards with optional filters."""
    try:
        analyzer = get_card_analyzer()

        # Optional query params
        rarity = request.args.get("rarity")
        card_type = request.args.get("type")
        archetype = request.args.get("archetype")
        min_elixir = request.args.get("min_elixir", type=int)
        max_elixir = request.args.get("max_elixir", type=int)

        # If filters provided, use filter method
        if any([rarity, card_type, archetype, min_elixir, max_elixir]):
            cards = analyzer.filter_cards(
                rarity=rarity, card_type=card_type, archetype=archetype,
                min_elixir=min_elixir, max_elixir=max_elixir
            )
        else:
            cards = analyzer.get_all_cards()

        return jsonify({
            "success": True,
            "total": len(cards),
            "cards": cards
        }), 200

    except Exception as e:
        logger.error(f"Error in get_all_cards: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@card_bp.route("/<string:card_name>", methods=["GET"])
def get_card_details(card_name: str):
    """Get details of a specific card."""
    try:
        analyzer = get_card_analyzer()
        card = analyzer.get_card_details(card_name)

        if not card:
            return jsonify({
                "success": False,
                "error": f"Card '{card_name}' not found"
            }), 404

        return jsonify({
            "success": True,
            "card": card
        }), 200

    except Exception as e:
        logger.error(f"Error in get_card_details: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@card_bp.route("/search", methods=["GET"])
def search_cards():
    """Search cards by name."""
    try:
        query = request.args.get("q", "").strip()

        if not query:
            return jsonify({
                "success": False,
                "error": "Query parameter 'q' is required"
            }), 400

        analyzer = get_card_analyzer()
        results = analyzer.search_cards(query)

        return jsonify({
            "success": True,
            "query": query,
            "total": len(results),
            "results": results
        }), 200

    except Exception as e:
        logger.error(f"Error in search_cards: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@card_bp.route("/top/win-rate", methods=["GET"])
def get_top_by_win_rate():
    """Get top cards by win rate."""
    try:
        n = request.args.get("n", default=10, type=int)
        analyzer = get_card_analyzer()
        cards = analyzer.get_top_cards_by_win_rate(n)

        return jsonify({
            "success": True,
            "metric": "win_rate",
            "top_n": n,
            "cards": cards
        }), 200

    except Exception as e:
        logger.error(f"Error in get_top_by_win_rate: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@card_bp.route("/top/usage", methods=["GET"])
def get_top_by_usage():
    """Get top cards by usage rate."""
    try:
        n = request.args.get("n", default=10, type=int)
        analyzer = get_card_analyzer()
        cards = analyzer.get_top_cards_by_usage(n)

        return jsonify({
            "success": True,
            "metric": "usage_rate",
            "top_n": n,
            "cards": cards
        }), 200

    except Exception as e:
        logger.error(f"Error in get_top_by_usage: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@card_bp.route("/stats", methods=["GET"])
def get_card_stats():
    """Get overall card statistics."""
    try:
        analyzer = get_card_analyzer()
        stats = analyzer.get_card_statistics()

        return jsonify({
            "success": True,
            "statistics": stats
        }), 200

    except Exception as e:
        logger.error(f"Error in get_card_stats: {e}")
        return jsonify({"success": False, "error": str(e)}), 500