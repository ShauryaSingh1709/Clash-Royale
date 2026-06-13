














import pandas as pd
from pathlib import Path
from typing import Optional
from backend.config.settings import Config
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class DatasetLoader:










    def __init__(self, data_path: Optional[Path] = None) -> None:






        self.data_path: Path = data_path or Config.PROCESSED_DATA_PATH
        self._cache: dict[str, pd.DataFrame] = {}
        logger.info(f"DatasetLoader initialized with path: {self.data_path}")





    def _load_csv(self, filename: str) -> pd.DataFrame:













        if filename in self._cache:
            logger.debug(f"Returning cached: {filename}")
            return self._cache[filename]


        file_path: Path = self.data_path / filename

        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            raise FileNotFoundError(f"Dataset file not found: {file_path}")

        try:
            df = pd.read_csv(file_path)
            self._cache[filename] = df
            logger.info(f"Loaded: {filename} | Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"Failed to load {filename}: {e}")
            raise





    def load_cards(self) -> pd.DataFrame:

        return self._load_csv(Config.CARDS_FILE)

    def load_decks(self) -> pd.DataFrame:

        return self._load_csv(Config.DECKS_FILE)

    def load_battles(self) -> pd.DataFrame:

        return self._load_csv(Config.BATTLES_FILE)

    def load_meta(self) -> pd.DataFrame:

        return self._load_csv(Config.META_FILE)

    def load_all(self) -> dict[str, pd.DataFrame]:






        logger.info("Loading all datasets...")
        return {
            "cards":   self.load_cards(),
            "decks":   self.load_decks(),
            "battles": self.load_battles(),
            "meta":    self.load_meta()
        }

    def clear_cache(self) -> None:

        self._cache.clear()
        logger.info("Cache cleared")

    def reload(self, filename: str) -> pd.DataFrame:









        if filename in self._cache:
            del self._cache[filename]
        return self._load_csv(filename)