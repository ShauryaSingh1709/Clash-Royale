"""
==========================================================================
🏆 CLASH ROYALE DECK ANALYZER - ML Model Loader
==========================================================================

Loads all trained machine learning models into memory.

Implements Singleton pattern - models load ONCE at startup,
then reused for every API request (fast & efficient).

Usage:
    from backend.ml.model_loader import ModelLoader

    loader = ModelLoader()
    win_rate_model = loader.win_rate_model
    scaler = loader.scaler
"""

import joblib
import pickle
from pathlib import Path
from typing import Optional, Any
from backend.config.settings import Config
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ModelLoader:
    """
    Singleton class to load all ML models into memory.
    
    Loads models once at startup, then provides fast access.
    Prevents re-loading models on every request (huge performance gain).
    
    Models loaded:
        1. Win Rate Predictor       (Random Forest)
        2. Deck Strength Scorer     (Gradient Boosting)
        3. Archetype Classifier     (Random Forest)
        4. Similar Deck Finder      (KNN)
        5. Scaler                   (StandardScaler)
        6. Label Encoder            (for archetype labels)
        7. Card Binarizer           (MultiLabelBinarizer)
        8. Card Lookup              (Dictionary)
    """

    _instance: Optional["ModelLoader"] = None
    _models_loaded: bool = False

    def __new__(cls) -> "ModelLoader":
        """Singleton pattern - only one instance ever exists."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        """Initialize and load all models (only once)."""
        if not ModelLoader._models_loaded:
            self.models_path: Path = Config.MODELS_PATH
            self._load_all_models()
            ModelLoader._models_loaded = True

    # ========================================================================
    # 🔧 PRIVATE LOADING METHODS
    # ========================================================================

    def _load_pkl(self, filename: str, use_pickle: bool = False) -> Any:
        """
        Load a pickle file safely with error handling.

        Args:
            filename:    Name of the .pkl file
            use_pickle:  Use pickle instead of joblib (for non-sklearn objects)

        Returns:
            Loaded model object

        Raises:
            FileNotFoundError: If file doesn't exist
        """
        file_path: Path = self.models_path / filename

        if not file_path.exists():
            logger.error(f"❌ Model file not found: {file_path}")
            raise FileNotFoundError(f"Model file not found: {file_path}")

        try:
            if use_pickle:
                with open(file_path, "rb") as f:
                    model = pickle.load(f)
            else:
                model = joblib.load(file_path)
            logger.info(f"✅ Loaded: {filename}")
            return model
        except Exception as e:
            logger.error(f"❌ Failed to load {filename}: {e}")
            raise

    def _load_all_models(self) -> None:
        """Load all ML models and supporting files."""
        logger.info("=" * 60)
        logger.info("🤖 LOADING ML MODELS INTO MEMORY")
        logger.info("=" * 60)

        # ML Models
        self.win_rate_model = self._load_pkl(Config.WIN_RATE_MODEL)
        self.strength_model = self._load_pkl(Config.STRENGTH_MODEL)
        self.archetype_model = self._load_pkl(Config.ARCHETYPE_MODEL)
        self.similar_deck_model = self._load_pkl(Config.SIMILAR_DECK_MODEL)

        # Preprocessing objects
        self.scaler = self._load_pkl(Config.SCALER_FILE)
        self.label_encoder = self._load_pkl(Config.LABEL_ENCODER_FILE)
        self.card_binarizer = self._load_pkl(Config.CARD_BINARIZER_FILE)

        # Card lookup (uses pickle)
        self.card_lookup = self._load_pkl(Config.CARD_LOOKUP_FILE, use_pickle=True)

        logger.info("=" * 60)
        logger.info(f"🎉 ALL MODELS LOADED ({len(self.list_loaded_models())} total)")
        logger.info("=" * 60)

    # ========================================================================
    # 🛠️ PUBLIC METHODS
    # ========================================================================

    def list_loaded_models(self) -> list[str]:
        """Returns list of all loaded model names."""
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
        """Returns info about all loaded models."""
        return {
            "loaded_models": self.list_loaded_models(),
            "total_models": len(self.list_loaded_models()),
            "models_path": str(self.models_path),
            "valid_cards_count": len(self.card_lookup),
            "available_archetypes": list(self.label_encoder.classes_),
        }

    def get_valid_cards(self) -> set:
        """Returns set of all valid card names."""
        return set(self.card_lookup.keys())

    def reload(self) -> None:
        """Force reload all models from disk."""
        logger.warning("🔄 Reloading all models...")
        ModelLoader._models_loaded = False
        self._load_all_models()
        ModelLoader._models_loaded = True