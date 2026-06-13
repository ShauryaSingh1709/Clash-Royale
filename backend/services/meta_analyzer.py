from typing import Optional
import pandas as pd
from backend.utils.dataset_loader import DatasetLoader
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class MetaAnalyzer:


    def __init__(self, loader: Optional[DatasetLoader] = None) -> None:

        self.loader = loader or DatasetLoader()
        self._cards_df: Optional[pd.DataFrame] = None
        self._decks_df: Optional[pd.DataFrame] = None
        self._meta_df: Optional[pd.DataFrame] = None
        logger.info("MetaAnalyzer initialized")

    @property
    def cards_df(self) -> pd.DataFrame:
        if self._cards_df is None:
            self._cards_df = self.loader.load_cards()
        return self._cards_df

    @property
    def decks_df(self) -> pd.DataFrame:
        if self._decks_df is None:
            self._decks_df = self.loader.load_decks()
        return self._decks_df

    @property
    def meta_df(self) -> pd.DataFrame:
        if self._meta_df is None:
            self._meta_df = self.loader.load_meta()
        return self._meta_df
    def get_meta_summary(self) -> dict:

        return {
            "total_cards": len(self.cards_df),
            "total_decks_analyzed": len(self.decks_df),
            "total_meta_records": len(self.meta_df),
            "average_card_win_rate": round(float(self.cards_df["win_rate"].mean()), 2),
            "average_card_usage": round(float(self.cards_df["usage_rate"].mean()), 2),
            "average_deck_win_rate": round(float(self.decks_df["win_rate"].mean()), 2),
            "average_deck_elixir": round(float(self.decks_df["avg_elixir"].mean()), 2),
            "seasons_tracked": sorted(self.meta_df["season"].unique().tolist())
        }
    def get_most_popular_cards(self, n: int = 10) -> list[dict]:

        cols = ["name", "rarity", "type", "elixir_cost", "usage_rate", "win_rate"]
        return self.cards_df.nlargest(n, "usage_rate")[cols].to_dict("records")

    def get_highest_winrate_cards(self, n: int = 10) -> list[dict]:

        cols = ["name", "rarity", "type", "elixir_cost", "win_rate", "usage_rate"]
        return self.cards_df.nlargest(n, "win_rate")[cols].to_dict("records")

    def get_underrated_cards(self, n: int = 10) -> list[dict]:

        df = self.cards_df.copy()
        df["underrated_score"] = df["win_rate"] / (df["usage_rate"] + 1)
        cols = ["name", "rarity", "type", "win_rate", "usage_rate", "underrated_score"]
        return df.nlargest(n, "underrated_score")[cols].to_dict("records")
    def get_archetype_distribution(self) -> dict:

        counts = self.decks_df["archetype"].value_counts()
        total = len(self.decks_df)

        return {
            "counts": counts.to_dict(),
            "percentages": {
                k: round((v / total) * 100, 2) for k, v in counts.items()
            },
            "most_popular_archetype": counts.index[0] if len(counts) > 0 else None
        }

    def get_top_decks(self, n: int = 10) -> list[dict]:
        sorted_decks = self.decks_df.sort_values("win_rate", ascending=False)
        

        seen_decks = set()
        unique_decks = []
        
        for _, row in sorted_decks.iterrows():

            cards_key = tuple(sorted([row[f"card_{i}"] for i in range(1, 9)]))
            
            if cards_key not in seen_decks:
                seen_decks.add(cards_key)
                unique_decks.append(row)
                
                if len(unique_decks) >= n:
                    break
        

        base_cols = [
            "deck_id", "card_1", "card_2", "card_3", "card_4",
            "card_5", "card_6", "card_7", "card_8",
            "avg_elixir", "archetype", "win_rate"
        ]
        

        optional_cols = ["deck_name", "tier", "source", "quality", "usage_count", "total_battles"]
        for col in optional_cols:
            if col in self.decks_df.columns:
                base_cols.append(col)
        
        return [
            {col: deck[col] for col in base_cols if col in deck.index}
            for deck in unique_decks
        ]

    def get_archetype_performance(self) -> list[dict]:

        grouped = self.decks_df.groupby("archetype").agg(
            avg_win_rate=("win_rate", "mean"),
            avg_elixir=("avg_elixir", "mean"),
            total_decks=("deck_id", "count")
        ).round(2).reset_index()

        return grouped.to_dict("records")
    def get_meta_trends(self) -> dict:

        seasonal = self.meta_df.groupby("season").agg(
            avg_win_rate=("win_rate", "mean"),
            avg_usage=("usage_rate", "mean")
        ).round(2).reset_index()

        return {
            "seasonal_data": seasonal.to_dict("records"),
            "rising_cards": self._get_trend_cards("Rising"),
            "falling_cards": self._get_trend_cards("Falling"),
            "stable_cards": self._get_trend_cards("Stable")
        }

    def _get_trend_cards(self, trend: str, n: int = 10) -> list[str]:

        cards = self.meta_df[self.meta_df["trend"] == trend]["card_name"].unique()
        return list(cards[:n])

    def get_seasonal_data(self, season: str) -> list[dict]:

        df = self.meta_df[self.meta_df["season"] == season]
        return df.to_dict("records")

    def get_card_meta_history(self, card_name: str) -> list[dict]:

        df = self.meta_df[self.meta_df["card_name"] == card_name]
        return df.sort_values("season").to_dict("records")