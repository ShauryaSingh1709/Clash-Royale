













from typing import Optional
from backend.config.settings import Config
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class DataCleaner:









    def __init__(self, valid_cards: Optional[set] = None) -> None:






        self.valid_cards: set = valid_cards or set()
        logger.info("DataCleaner initialized")





    def validate_deck(self, deck: list[str]) -> tuple[bool, str]:










        if not isinstance(deck, list):
            return False, "Deck must be a list of card names"


        if len(deck) != Config.DECK_SIZE:
            return False, f"Deck must contain exactly {Config.DECK_SIZE} cards (got {len(deck)})"


        if len(set(deck)) != len(deck):
            return False, "Deck cannot contain duplicate cards"


        if not all(isinstance(card, str) for card in deck):
            return False, "All cards must be strings"


        if any(not card.strip() for card in deck):
            return False, "Card names cannot be empty"


        if self.valid_cards:
            invalid_cards = [c for c in deck if c not in self.valid_cards]
            if invalid_cards:
                return False, f"Invalid cards: {', '.join(invalid_cards)}"

        return True, "Valid"

    def validate_card_name(self, card_name: str) -> tuple[bool, str]:









        if not isinstance(card_name, str):
            return False, "Card name must be a string"

        if not card_name.strip():
            return False, "Card name cannot be empty"

        if self.valid_cards and card_name not in self.valid_cards:
            return False, f"Card '{card_name}' does not exist"

        return True, "Valid"





    @staticmethod
    def clean_card_name(card_name: str) -> str:









        if not isinstance(card_name, str):
            return ""
        return card_name.strip().title()

    @staticmethod
    def clean_deck(deck: list[str]) -> list[str]:









        return [DataCleaner.clean_card_name(card) for card in deck if card]

    def update_valid_cards(self, valid_cards: set) -> None:

        self.valid_cards = valid_cards
        logger.info(f"Updated valid cards count: {len(self.valid_cards)}")