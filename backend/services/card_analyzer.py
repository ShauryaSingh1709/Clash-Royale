from typing import Optional
import pandas as pd
from backend.utils.dataset_loader import DatasetLoader
from backend.models.card import Card
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class CardAnalyzer:
    def __init__(self, loader: Optional[DatasetLoader] = None) -> None:
        self.loader = loader or DatasetLoader()
        self._cards_df: Optional[pd.DataFrame] = None
        logger.info("CardAnalyzer initialized")
    @property
    def cards_df(self) -> pd.DataFrame:
        if self._cards_df is None:
            self._cards_df = self.loader.load_cards()
        return self._cards_df
    def get_all_cards(self) -> list[dict]:
        return self.cards_df.to_dict("records")
    def get_card_details(self, card_name: str) -> Optional[dict]:
        row = self.cards_df[self.cards_df["name"] == card_name]
        if row.empty:
            logger.warning(f"Card not found: {card_name}")
            return None
        card_data = row.iloc[0].to_dict()
        card = Card.from_dict(card_data)
        return card.to_dict()
    def search_cards(self, query: str) -> list[dict]:
        if not query:
            return []
        mask = self.cards_df["name"].str.contains(query, case=False, na=False)
        return self.cards_df[mask].to_dict("records")
    def filter_cards(
        self,
        rarity: Optional[str] = None,
        card_type: Optional[str] = None,
        archetype: Optional[str] = None,
        min_elixir: Optional[int] = None,
        max_elixir: Optional[int] = None,
    ) -> list[dict]:
        df = self.cards_df.copy()

        if rarity:
            df = df[df["rarity"].str.lower() == rarity.lower()]
        if card_type:
            df = df[df["type"].str.lower() == card_type.lower()]
        if archetype:
            df = df[df["archetype"].str.lower() == archetype.lower()]
        if min_elixir is not None:
            df = df[df["elixir_cost"] >= min_elixir]
        if max_elixir is not None:
            df = df[df["elixir_cost"] <= max_elixir]

        return df.to_dict("records")
    def get_top_cards_by_win_rate(self, n: int = 10) -> list[dict]:

        return self.cards_df.nlargest(n, "win_rate").to_dict("records")

    def get_top_cards_by_usage(self, n: int = 10) -> list[dict]:

        return self.cards_df.nlargest(n, "usage_rate").to_dict("records")

    def get_top_cards_by_popularity(self, n: int = 10) -> list[dict]:

        return self.cards_df.nlargest(n, "popularity_score").to_dict("records")

    def get_cards_by_archetype(self, archetype: str) -> list[dict]:

        df = self.cards_df[
            self.cards_df["archetype"].str.lower() == archetype.lower()
        ]
        return df.to_dict("records")
    def get_card_statistics(self) -> dict:

        df = self.cards_df

        return {
            "total_cards": len(df),
            "rarity_distribution": df["rarity"].value_counts().to_dict(),
            "type_distribution": df["type"].value_counts().to_dict(),
            "archetype_distribution": df["archetype"].value_counts().to_dict(),
            "average_elixir": round(float(df["elixir_cost"].mean()), 2),
            "average_win_rate": round(float(df["win_rate"].mean()), 2),
            "average_usage_rate": round(float(df["usage_rate"].mean()), 2),
            "elixir_range": {
                "min": int(df["elixir_cost"].min()),
                "max": int(df["elixir_cost"].max()),
            },
        }