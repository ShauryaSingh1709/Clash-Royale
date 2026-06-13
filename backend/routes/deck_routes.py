












from flask import Blueprint, jsonify, request
from backend.services.deck_analyzer import DeckAnalyzer
from backend.utils.logger import get_logger

logger = get_logger(__name__)

deck_bp = Blueprint("decks", __name__, url_prefix="/decks")

_deck_analyzer: DeckAnalyzer = None


def get_deck_analyzer() -> DeckAnalyzer:

    global _deck_analyzer
    if _deck_analyzer is None:
        _deck_analyzer = DeckAnalyzer()
    return _deck_analyzer


def _extract_deck_from_request() -> tuple[list, str]:

    data = request.get_json()
    if not data:
        return None, "Request body must be JSON"

    cards = data.get("cards")
    if not cards:
        return None, "Field 'cards' is required (list of 8 card names)"

    return cards, None






@deck_bp.route("/analyze", methods=["POST"])
def analyze_deck():








    try:
        cards, error = _extract_deck_from_request()
        if error:
            return jsonify({"success": False, "error": error}), 400

        analyzer = get_deck_analyzer()
        result = analyzer.analyze_deck(cards)

        status_code = 200 if result["success"] else 400
        return jsonify(result), status_code

    except Exception as e:
        logger.error(f"Error in analyze_deck: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@deck_bp.route("/validate", methods=["POST"])
def validate_deck():








    try:
        cards, error = _extract_deck_from_request()
        if error:
            return jsonify({"success": False, "error": error}), 400

        analyzer = get_deck_analyzer()
        result = analyzer.validate_deck(cards)

        return jsonify({
            "success": True,
            "validation": result
        }), 200

    except Exception as e:
        logger.error(f"Error in validate_deck: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


@deck_bp.route("/score", methods=["POST"])
def score_deck():








    try:
        cards, error = _extract_deck_from_request()
        if error:
            return jsonify({"success": False, "error": error}), 400

        analyzer = get_deck_analyzer()

        validation = analyzer.validate_deck(cards)
        if not validation["valid"]:
            return jsonify({
                "success": False,
                "error": validation["message"]
            }), 400

        score = analyzer.score_deck(cards)
        return jsonify({
            "success": True,
            "scoring": score
        }), 200

    except Exception as e:
        logger.error(f"Error in score_deck: {e}")
        return jsonify({"success": False, "error": str(e)}), 500