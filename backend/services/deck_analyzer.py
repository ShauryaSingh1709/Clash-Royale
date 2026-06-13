"""
==========================================================================
🏆 CLASH ROYALE DECK ANALYZER - Deck Analyzer Service
==========================================================================

Service for analyzing decks: validation, scoring, strengths/weaknesses.

Usage:
    from backend.services.deck_analyzer import DeckAnalyzer

    analyzer = DeckAnalyzer()
    result = analyzer.analyze_deck(["Hog Rider", ...])
"""

from typing import Optional
from backend.ml.predictor import MLPredictor
from backend.models.deck import Deck
from backend.utils.dataset_loader import DatasetLoader
from backend.utils.data_cleaner import DataCleaner
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class DeckAnalyzer:
    """
    Service for complete deck analysis.

    Combines OOP deck logic + ML predictions + business rules.

    Methods:
        - analyze_deck(cards):                Full analysis
        - get_strengths_weaknesses(cards):    Identify pros/cons
        - validate_deck(cards):               Check if deck is valid
        - score_deck(cards):                  Get comprehensive scores
    """

    def __init__(
        self,
        predictor: Optional[MLPredictor] = None,
        loader: Optional[DatasetLoader] = None
    ) -> None:
        """Initialize DeckAnalyzer."""
        self.predictor = predictor or MLPredictor()
        self.loader = loader or DatasetLoader()
        self.card_lookup = self.predictor.card_lookup
        self.cleaner = DataCleaner(valid_cards=set(self.card_lookup.keys()))
        logger.info("DeckAnalyzer initialized")

    # ========================================================================
    # ✅ VALIDATION
    # ========================================================================

    def validate_deck(self, card_names: list[str]) -> dict:
        """
        Validate a deck of cards.

        Args:
            card_names: List of card names

        Returns:
            dict: {valid: bool, error: str | None}
        """
        is_valid, message = self.cleaner.validate_deck(card_names)
        return {
            "valid": is_valid,
            "message": message,
            "deck_size": len(card_names) if isinstance(card_names, list) else 0
        }

    # ========================================================================
    # 🔍 ANALYSIS
    # ========================================================================

    def get_strengths_weaknesses(self, card_names: list[str]) -> dict:
        """
        Identify strengths and weaknesses of a deck.

        Args:
            card_names: List of 8 card names

        Returns:
            dict: {strengths: list, weaknesses: list}
        """
        deck = Deck.from_card_names(card_names, self.card_lookup)

        strengths: list[str] = []
        weaknesses: list[str] = []

        # ── ELIXIR ANALYSIS ───────────────────────────
        if deck.is_cheap_cycle:
            strengths.append("⚡ Fast cycle potential (low elixir cost)")
        if deck.is_heavy_beatdown:
            strengths.append("💪 Strong push potential (high damage)")
        if deck.average_elixir > 4.5:
            weaknesses.append("🐢 Slow cycle (high elixir average)")
        if deck.average_elixir < 3.0:
            weaknesses.append("💔 Limited damage output (very low elixir)")

        # ── COMPOSITION ANALYSIS ──────────────────────
        if deck.num_spells >= 2:
            strengths.append("🎯 Good spell coverage")
        if deck.num_spells == 0:
            weaknesses.append("❌ No spells - vulnerable to swarms")

        if deck.num_buildings >= 1:
            strengths.append("🛡️ Defensive structure available")
        elif not deck.has_win_condition:
            weaknesses.append("🏚️ No buildings & no win condition")

        if deck.num_troops >= 5:
            strengths.append("⚔️ Strong troop presence")
        if deck.num_troops < 4:
            weaknesses.append("⚠️ Few troops in deck")

        # ── WIN CONDITION ─────────────────────────────
        if deck.has_win_condition:
            strengths.append("🏆 Has clear win condition")
        else:
            weaknesses.append("❓ No clear win condition")

        # ── CARD QUALITY ──────────────────────────────
        if deck.average_card_win_rate >= 52:
            strengths.append("📈 Cards with proven win rates")
        if deck.average_card_win_rate < 48:
            weaknesses.append("📉 Low average card win rates")

        # ── LEGENDARY COUNT ───────────────────────────
        if deck.num_legendary >= 3:
            strengths.append("👑 High-tier legendary cards")
        if deck.num_legendary == 0:
            weaknesses.append("📊 No legendary cards (limited power)")

        # Default if nothing found
        if not strengths:
            strengths.append("⚖️ Balanced deck composition")
        if not weaknesses:
            weaknesses.append("✅ No major weaknesses detected")

        return {
            "strengths": strengths,
            "weaknesses": weaknesses
        }

    def score_deck(self, card_names: list[str]) -> dict:
        """
        Comprehensive deck scoring.

        Returns:
            dict: Multiple scoring metrics
        """
        win_rate = self.predictor.predict_win_rate(card_names)
        strength = self.predictor.predict_strength(card_names)
        archetype = self.predictor.predict_archetype(card_names)

        # Overall grade based on strength
        overall_grade = strength["grade"]

        # Rating message
        score = strength["strength_score"]
        if score >= 80:
            rating_message = "🏆 Top-tier deck! Excellent choice."
        elif score >= 65:
            rating_message = "💪 Strong deck with great potential."
        elif score >= 50:
            rating_message = "✅ Solid deck for ladder play."
        elif score >= 35:
            rating_message = "⚠️ Below average - consider improvements."
        else:
            rating_message = "❌ Weak deck - significant changes needed."

        return {
            "win_rate": win_rate,
            "strength": strength,
            "archetype": archetype,
            "overall_grade": overall_grade,
            "rating_message": rating_message
        }

    # ========================================================================
    # 🎯 COMPLETE ANALYSIS
    # ========================================================================

    def analyze_deck(self, card_names: list[str]) -> dict:
        """
        Complete deck analysis combining all features.

        Args:
            card_names: List of 8 card names

        Returns:
            dict: Complete analysis report
        """
        # Validate first
        validation = self.validate_deck(card_names)
        if not validation["valid"]:
            return {
                "success": False,
                "error": validation["message"]
            }

        # Build deck and get all info
        deck = Deck.from_card_names(card_names, self.card_lookup)
        score = self.score_deck(card_names)
        sw = self.get_strengths_weaknesses(card_names)

        logger.info(f"✅ Deck analyzed | Score: {score['strength']['strength_score']}")

        return {
            "success": True,
            "deck": deck.to_dict(),
            "scoring": score,
            "strengths": sw["strengths"],
            "weaknesses": sw["weaknesses"]
        }