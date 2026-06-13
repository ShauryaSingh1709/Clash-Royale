



















import pandas as pd
import numpy as np
from typing import Optional
from backend.ml.model_loader import ModelLoader
from backend.models.deck import Deck
from backend.config.settings import Config
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class MLPredictor:











    def __init__(self, model_loader: Optional[ModelLoader] = None) -> None:






        self.loader: ModelLoader = model_loader or ModelLoader()
        self.card_lookup: dict = self.loader.card_lookup
        logger.info("MLPredictor initialized")





    def _build_deck(self, card_names: list[str]) -> Deck:

        return Deck.from_card_names(card_names, self.card_lookup)

    def _prepare_features(self, deck: Deck) -> np.ndarray:









        features_dict = deck.to_ml_features()
        features_df = pd.DataFrame([features_dict])[Config.FEATURE_COLUMNS]
        return self.loader.scaler.transform(features_df)





    def predict_win_rate(self, card_names: list[str]) -> dict:









        deck = self._build_deck(card_names)
        features = self._prepare_features(deck)
        win_rate = float(self.loader.win_rate_model.predict(features)[0])


        if 45 <= win_rate <= 60:
            confidence = "High"
        elif 40 <= win_rate <= 65:
            confidence = "Medium"
        else:
            confidence = "Low"

        return {
            "predicted_win_rate": round(win_rate, 2),
            "confidence": confidence
        }

    def predict_strength(self, card_names: list[str]) -> dict:









        deck = self._build_deck(card_names)
        features = self._prepare_features(deck)
        score = float(self.loader.strength_model.predict(features)[0])
        score = max(0, min(100, score))


        if score >= 85:
            grade = "S"
        elif score >= 75:
            grade = "A"
        elif score >= 65:
            grade = "B"
        elif score >= 55:
            grade = "C"
        elif score >= 45:
            grade = "D"
        else:
            grade = "F"

        return {
            "strength_score": round(score, 2),
            "grade": grade
        }

    def predict_archetype(self, card_names: list[str]) -> dict:









        deck = self._build_deck(card_names)
        features = self._prepare_features(deck)


        pred_idx = self.loader.archetype_model.predict(features)[0]
        archetype = self.loader.label_encoder.inverse_transform([pred_idx])[0]


        probabilities = self.loader.archetype_model.predict_proba(features)[0]
        classes = self.loader.label_encoder.classes_

        all_probs = {
            cls: round(float(prob) * 100, 2)
            for cls, prob in zip(classes, probabilities)
        }

        confidence = round(float(max(probabilities)) * 100, 2)

        return {
            "predicted_archetype": archetype,
            "confidence": confidence,
            "all_probabilities": all_probs
        }

    def find_similar_decks(self, card_names: list[str], top_n: int = 5) -> list[dict]:











        user_vector = self.loader.card_binarizer.transform([card_names])


        distances, indices = self.loader.similar_deck_model.kneighbors(
            user_vector, n_neighbors=top_n + 1
        )


        from backend.utils.dataset_loader import DatasetLoader
        decks_df = DatasetLoader().load_decks()

        similar_decks = []
        for i, (dist, idx) in enumerate(zip(distances[0], indices[0])):

            if i == 0 and dist == 0:
                continue
            if len(similar_decks) >= top_n:
                break

            deck_row = decks_df.iloc[idx]
            similar_decks.append({
                "deck_id": int(deck_row["deck_id"]),
                "cards": [deck_row[f"card_{j}"] for j in range(1, 9)],
                "archetype": deck_row["archetype"],
                "avg_elixir": float(deck_row["avg_elixir"]),
                "win_rate": float(deck_row["win_rate"]),
                "quality": deck_row.get("quality", "Unknown"),
                "similarity_score": round((1 - float(dist)) * 100, 2)
            })

        return similar_decks

    def suggest_card_replacements(
        self, card_names: list[str], top_n: int = 3
    ) -> dict:










        deck = self._build_deck(card_names)
        weakest = deck.get_weakest_card()

        if not weakest:
            return {"weakest_card": None, "replacements": []}


        from backend.utils.dataset_loader import DatasetLoader
        cards_df = DatasetLoader().load_cards()


        candidates = cards_df[
            (cards_df["elixir_cost"].between(
                weakest.elixir_cost - 1, weakest.elixir_cost + 1
            )) &
            (cards_df["type"] == weakest.card_type) &
            (cards_df["win_rate"] > weakest.win_rate) &
            (~cards_df["name"].isin(card_names))
        ].nlargest(top_n, "win_rate")

        replacements = []
        for _, row in candidates.iterrows():
            replacements.append({
                "name": row["name"],
                "elixir_cost": int(row["elixir_cost"]),
                "rarity": row["rarity"],
                "type": row["type"],
                "win_rate": round(float(row["win_rate"]), 2),
                "usage_rate": round(float(row["usage_rate"]), 2),
                "improvement": round(
                    float(row["win_rate"]) - float(weakest.win_rate), 2
                )
            })

        return {
            "weakest_card": {
                "name": weakest.name,
                "win_rate": weakest.win_rate,
                "elixir_cost": weakest.elixir_cost,
                "type": weakest.card_type
            },
            "replacements": replacements
        }





    def predict_all(self, card_names: list[str]) -> dict:









        logger.info(f"🔮 Running full prediction on deck: {card_names[:3]}...")

        deck = self._build_deck(card_names)

        return {
            "deck": {
                "cards": card_names,
                "avg_elixir": deck.average_elixir,
                "composition": {
                    "troops": deck.num_troops,
                    "spells": deck.num_spells,
                    "buildings": deck.num_buildings,
                    "legendary": deck.num_legendary,
                }
            },
            "win_rate_prediction": self.predict_win_rate(card_names),
            "strength_prediction": self.predict_strength(card_names),
            "archetype_prediction": self.predict_archetype(card_names),
            "similar_decks": self.find_similar_decks(card_names, top_n=3),
            "improvement_suggestions": self.suggest_card_replacements(
                card_names, top_n=3
            )
        }