














from typing import Optional
from backend.ml.predictor import MLPredictor
from backend.services.deck_analyzer import DeckAnalyzer
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class RecommendationEngine:









    def __init__(
        self,
        predictor: Optional[MLPredictor] = None,
        deck_analyzer: Optional[DeckAnalyzer] = None
    ) -> None:

        self.predictor = predictor or MLPredictor()
        self.deck_analyzer = deck_analyzer or DeckAnalyzer(predictor=self.predictor)
        logger.info("RecommendationEngine initialized")





    def find_similar_decks(self, card_names: list[str], top_n: int = 5) -> dict:










        validation = self.deck_analyzer.validate_deck(card_names)
        if not validation["valid"]:
            return {"success": False, "error": validation["message"]}

        similar = self.predictor.find_similar_decks(card_names, top_n=top_n)

        return {
            "success": True,
            "user_deck": card_names,
            "similar_decks": similar,
            "total_found": len(similar)
        }





    def suggest_improvements(
        self, card_names: list[str], top_n: int = 3
    ) -> dict:










        validation = self.deck_analyzer.validate_deck(card_names)
        if not validation["valid"]:
            return {"success": False, "error": validation["message"]}

        suggestions = self.predictor.suggest_card_replacements(
            card_names, top_n=top_n
        )


        expected_improvement = 0.0
        if suggestions["replacements"]:
            best = suggestions["replacements"][0]
            expected_improvement = best.get("improvement", 0)

        return {
            "success": True,
            "user_deck": card_names,
            "weakest_card": suggestions["weakest_card"],
            "replacements": suggestions["replacements"],
            "expected_improvement_pct": round(expected_improvement, 2)
        }





    def get_full_recommendation(self, card_names: list[str]) -> dict:











        validation = self.deck_analyzer.validate_deck(card_names)
        if not validation["valid"]:
            return {"success": False, "error": validation["message"]}

        logger.info(f"🎯 Generating full recommendation for deck")


        analysis = self.deck_analyzer.analyze_deck(card_names)
        similar = self.find_similar_decks(card_names, top_n=3)
        improvements = self.suggest_improvements(card_names, top_n=3)
        full_ml = self.predictor.predict_all(card_names)

        return {
            "success": True,
            "user_deck": card_names,
            "analysis": analysis,
            "similar_decks": similar.get("similar_decks", []),
            "improvements": improvements,
            "ml_predictions": {
                "win_rate": full_ml["win_rate_prediction"],
                "strength": full_ml["strength_prediction"],
                "archetype": full_ml["archetype_prediction"]
            }
        }