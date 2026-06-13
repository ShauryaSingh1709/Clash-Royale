















from flask import Blueprint, jsonify, request
from backend.services.meta_analyzer import MetaAnalyzer
from backend.utils.logger import get_logger

logger = get_logger(__name__)

meta_bp = Blueprint("meta", __name__, url_prefix="/meta")

_meta_analyzer: MetaAnalyzer = None


def get_meta_analyzer() -> MetaAnalyzer:

    global _meta_analyzer
    if _meta_analyzer is None:
        _meta_analyzer = MetaAnalyzer()
    return _meta_analyzer






@meta_bp.route("/summary", methods=["GET"])
def get_summary():

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