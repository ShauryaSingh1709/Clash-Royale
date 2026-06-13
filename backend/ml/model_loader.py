

import joblib
import pickle
from pathlib import Path
from typing import Optional, Any
from backend.config.settings import Config
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ModelLoader:


    _instance: Optional["ModelLoader"] = None
    _models_loaded: bool = False

    def __new__(cls) -> "ModelLoader":

        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:

        if not ModelLoader._models_loaded:
            self.models_path: Path = Config.MODELS_PATH
            self._load_all_models()
            ModelLoader._models_loaded = True





    def _load_pkl(self, filename: str, use_pickle: bool = False) -> Any:













        file_path: Path = self.models_path / filename

        if not file_path.exists():
            logger.error(f"Model file not found: {file_path}")
            raise FileNotFoundError(f"Model file not found: {file_path}")

        try:
            if use_pickle:
                with open(file_path, "rb") as f:
                    model = pickle.load(f)
            else:
                model = joblib.load(file_path)
            logger.info(f"Loaded: {filename}")
            return model
        except Exception as e:
            logger.error(f"Failed to load {filename}: {e}")
            raise

    def _load_all_models(self) -> None:

        logger.info("=" * 60)
        logger.info("LOADING ML MODELS INTO MEMORY")
        logger.info("=" * 60)


        self.win_rate_model = self._load_pkl(Config.WIN_RATE_MODEL)
        self.strength_model = self._load_pkl(Config.STRENGTH_MODEL)
        self.archetype_model = self._load_pkl(Config.ARCHETYPE_MODEL)
        self.similar_deck_model = self._load_pkl(Config.SIMILAR_DECK_MODEL)


        self.scaler = self._load_pkl(Config.SCALER_FILE)
        self.label_encoder = self._load_pkl(Config.LABEL_ENCODER_FILE)
        self.card_binarizer = self._load_pkl(Config.CARD_BINARIZER_FILE)


        self.card_lookup = self._load_pkl(Config.CARD_LOOKUP_FILE, use_pickle=True)

        logger.info("=" * 60)
        logger.info(f"ALL MODELS LOADED ({len(self.list_loaded_models())} total)")
        logger.info("=" * 60)





    def list_loaded_models(self) -> list[str]:

        return [
            "win_rate_model",
            "strength_model",
            "archetype_model",
            "similar_deck_model",
            "scaler",
            "label_encoder",
            "card_binarizer",
            "card_lookup",
        ]

    def get_model_info(self) -> dict:

        return {
            "loaded_models": self.list_loaded_models(),
            "total_models": len(self.list_loaded_models()),
            "models_path": str(self.models_path),
            "valid_cards_count": len(self.card_lookup),
            "available_archetypes": list(self.label_encoder.classes_),
        }

    def get_valid_cards(self) -> set:

        return set(self.card_lookup.keys())

    def reload(self) -> None:

        logger.warning("Reloading all models...")
        ModelLoader._models_loaded = False
        self._load_all_models()
        ModelLoader._models_loaded = True