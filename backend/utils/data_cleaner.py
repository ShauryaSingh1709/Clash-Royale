"""
==========================================================================
🏆 CLASH ROYALE DECK ANALYZER - Data Cleaner Utility
==========================================================================

Validation and cleaning utilities for user input data.

Usage:
    from backend.utils.data_cleaner import DataCleaner

    cleaner = DataCleaner()
    is_valid, error = cleaner.validate_deck(user_deck)
"""

from typing import Optional
from backend.config.settings import Config
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class DataCleaner:
    """
    Utility class for validating and cleaning user input.
    
    Methods:
        - validate_deck: Check if a deck is valid
        - clean_card_name: Standardize card name format
        - validate_card_name: Check if card exists
    """

    def __init__(self, valid_cards: Optional[set] = None) -> None:
        """
        Initialize DataCleaner.

        Args:
            valid_cards: Optional set of valid card names for validation
        """
        self.valid_cards: set = valid_cards or set()
        logger.info("DataCleaner initialized")

    # ========================================================================
    # ✅ VALIDATION METHODS
    # ========================================================================

    def validate_deck(self, deck: list[str]) -> tuple[bool, str]:
        """
        Validate a deck of cards.

        Args:
            deck: List of card names

        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        # Check type
        if not isinstance(deck, list):
            return False, "Deck must be a list of card names"

        # Check size
        if len(deck) != Config.DECK_SIZE:
            return False, f"Deck must contain exactly {Config.DECK_SIZE} cards (got {len(deck)})"

        # Check for duplicates
        if len(set(deck)) != len(deck):
            return False, "Deck cannot contain duplicate cards"

        # Check all cards are strings
        if not all(isinstance(card, str) for card in deck):
            return False, "All cards must be strings"

        # Check empty strings
        if any(not card.strip() for card in deck):
            return False, "Card names cannot be empty"

        # Check cards exist (if valid_cards provided)
        if self.valid_cards:
            invalid_cards = [c for c in deck if c not in self.valid_cards]
            if invalid_cards:
                return False, f"Invalid cards: {', '.join(invalid_cards)}"

        return True, "Valid"

    def validate_card_name(self, card_name: str) -> tuple[bool, str]:
        """
        Validate a single card name.

        Args:
            card_name: Name of the card

        Returns:
            tuple: (is_valid: bool, error_message: str)
        """
        if not isinstance(card_name, str):
            return False, "Card name must be a string"

        if not card_name.strip():
            return False, "Card name cannot be empty"

        if self.valid_cards and card_name not in self.valid_cards:
            return False, f"Card '{card_name}' does not exist"

        return True, "Valid"

    # ========================================================================
    # 🧹 CLEANING METHODS
    # ========================================================================

    @staticmethod
    def clean_card_name(card_name: str) -> str:
        """
        Standardize a card name (strip whitespace, title case).

        Args:
            card_name: Raw card name

        Returns:
            str: Cleaned card name
        """
        if not isinstance(card_name, str):
            return ""
        return card_name.strip().title()

    @staticmethod
    def clean_deck(deck: list[str]) -> list[str]:
        """
        Clean all card names in a deck.

        Args:
            deck: List of raw card names

        Returns:
            list: List of cleaned card names
        """
        return [DataCleaner.clean_card_name(card) for card in deck if card]

    def update_valid_cards(self, valid_cards: set) -> None:
        """Update the set of valid card names."""
        self.valid_cards = valid_cards
        logger.info(f"Updated valid cards count: {len(self.valid_cards)}")