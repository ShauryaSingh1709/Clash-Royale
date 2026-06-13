












import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


class Config:










    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    BACKEND_DIR: Path = BASE_DIR / "backend"
    DATASET_DIR: Path = BASE_DIR / "dataset"
    RAW_DATA_PATH: Path = DATASET_DIR / "raw"
    PROCESSED_DATA_PATH: Path = DATASET_DIR / "processed"
    MODELS_PATH: Path = BACKEND_DIR / "ml" / "models"
    LOGS_PATH: Path = BASE_DIR / "logs"




    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = int(os.getenv("PORT", 5000))
    DEBUG: bool = os.getenv("FLASK_DEBUG", "True").lower() == "true"




    CARDS_FILE: str = "cards_cleaned.csv"
    DECKS_FILE: str = "decks_cleaned.csv"
    BATTLES_FILE: str = "battles_cleaned.csv"
    META_FILE: str = "meta_cleaned.csv"




    WIN_RATE_MODEL: str = "win_rate_predictor.pkl"
    STRENGTH_MODEL: str = "deck_strength_scorer.pkl"
    ARCHETYPE_MODEL: str = "archetype_classifier.pkl"
    SIMILAR_DECK_MODEL: str = "similar_deck_finder.pkl"
    SCALER_FILE: str = "scaler.pkl"
    LABEL_ENCODER_FILE: str = "label_encoder.pkl"
    CARD_BINARIZER_FILE: str = "card_binarizer.pkl"
    CARD_LOOKUP_FILE: str = "card_lookup.pkl"




    FEATURE_COLUMNS: list = [
        "avg_elixir", "total_elixir", "avg_damage", "avg_hp",
        "avg_card_win_rate", "avg_card_usage",
        "num_legendary", "num_epic", "num_rare", "num_common",
        "num_troops", "num_spells", "num_buildings"
    ]




    DECK_SIZE: int = 8
    MIN_ELIXIR: int = 1
    MAX_ELIXIR: int = 9
    VALID_RARITIES: list = ["Common", "Rare", "Epic", "Legendary", "Champion"]
    VALID_CARD_TYPES: list = ["Troop", "Spell", "Building"]
    VALID_ARCHETYPES: list = ["Beatdown", "Control", "Cycle", "Siege", "Hog Cycle"]




    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    LOG_FORMAT: str = "%(asctime)s | %(levelname)-8s | %(name)-25s | %(message)s"
    LOG_DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"




    API_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list = ["*"]
    MAX_REQUEST_SIZE: int = 16 * 1024 * 1024

    @classmethod
    def ensure_directories(cls) -> None:

        for path in [cls.LOGS_PATH, cls.PROCESSED_DATA_PATH, cls.MODELS_PATH]:
            path.mkdir(parents=True, exist_ok=True)

    @classmethod
    def display(cls) -> None:

        print("=" * 60)
        print("🏆 CLASH ROYALE DECK ANALYZER - Configuration")
        print("=" * 60)
        print(f"📂 BASE_DIR:           {cls.BASE_DIR}")
        print(f"📂 MODELS_PATH:        {cls.MODELS_PATH}")
        print(f"📂 PROCESSED_DATA:     {cls.PROCESSED_DATA_PATH}")
        print(f"🌐 HOST:PORT:          {cls.HOST}:{cls.PORT}")
        print(f"🐛 DEBUG:              {cls.DEBUG}")
        print(f"📝 LOG_LEVEL:          {cls.LOG_LEVEL}")
        print("=" * 60)



Config.ensure_directories()