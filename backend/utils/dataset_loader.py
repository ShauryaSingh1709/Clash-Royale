"""
==========================================================================
🏆 CLASH ROYALE DECK ANALYZER - Dataset Loader
==========================================================================

Reusable utility for loading datasets with proper error handling and caching.

Usage:
    from backend.utils.dataset_loader import DatasetLoader

    loader = DatasetLoader()
    cards_df = loader.load_cards()
    decks_df = loader.load_decks()
"""

import pandas as pd
from pathlib import Path
from typing import Optional
from backend.config.settings import Config
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class DatasetLoader:
    """
    Centralized dataset loader for all CSV files.
    
    Features:
        - Lazy loading (loads only when needed)
        - In-memory caching (loads once, reuses)
        - Error handling with logging
        - Type-safe DataFrame returns
    """

    def __init__(self, data_path: Optional[Path] = None) -> None:
        """
        Initialize DatasetLoader.

        Args:
            data_path: Optional custom data path. Defaults to Config.PROCESSED_DATA_PATH
        """
        self.data_path: Path = data_path or Config.PROCESSED_DATA_PATH
        self._cache: dict[str, pd.DataFrame] = {}
        logger.info(f"DatasetLoader initialized with path: {self.data_path}")

    # ========================================================================
    # 🔧 PRIVATE METHODS
    # ========================================================================

    def _load_csv(self, filename: str) -> pd.DataFrame:
        """
        Load CSV file with caching and error handling.

        Args:
            filename: Name of the CSV file (e.g., 'cards_cleaned.csv')

        Returns:
            pd.DataFrame: Loaded dataset

        Raises:
            FileNotFoundError: If the file does not exist
        """
        # Return from cache if already loaded
        if filename in self._cache:
            logger.debug(f"Returning cached: {filename}")
            return self._cache[filename]

        # Load from disk
        file_path: Path = self.data_path / filename

        if not file_path.exists():
            logger.error(f"❌ File not found: {file_path}")
            raise FileNotFoundError(f"Dataset file not found: {file_path}")

        try:
            df = pd.read_csv(file_path)
            self._cache[filename] = df
            logger.info(f"✅ Loaded: {filename} | Shape: {df.shape}")
            return df
        except Exception as e:
            logger.error(f"❌ Failed to load {filename}: {e}")
            raise

    # ========================================================================
    # 📥 PUBLIC LOADERS
    # ========================================================================

    def load_cards(self) -> pd.DataFrame:
        """Load the cards dataset."""
        return self._load_csv(Config.CARDS_FILE)

    def load_decks(self) -> pd.DataFrame:
        """Load the decks dataset."""
        return self._load_csv(Config.DECKS_FILE)

    def load_battles(self) -> pd.DataFrame:
        """Load the battles dataset."""
        return self._load_csv(Config.BATTLES_FILE)

    def load_meta(self) -> pd.DataFrame:
        """Load the meta statistics dataset."""
        return self._load_csv(Config.META_FILE)

    def load_all(self) -> dict[str, pd.DataFrame]:
        """
        Load all datasets at once.

        Returns:
            dict: Dictionary with keys 'cards', 'decks', 'battles', 'meta'
        """
        logger.info("Loading all datasets...")
        return {
            "cards":   self.load_cards(),
            "decks":   self.load_decks(),
            "battles": self.load_battles(),
            "meta":    self.load_meta()
        }

    def clear_cache(self) -> None:
        """Clear the in-memory dataset cache."""
        self._cache.clear()
        logger.info("Cache cleared")

    def reload(self, filename: str) -> pd.DataFrame:
        """
        Force reload a specific dataset from disk.

        Args:
            filename: Name of the file to reload

        Returns:
            pd.DataFrame: Reloaded dataset
        """
        if filename in self._cache:
            del self._cache[filename]
        return self._load_csv(filename)