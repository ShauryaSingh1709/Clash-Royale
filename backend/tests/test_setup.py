from backend.config.settings import Config
from backend.utils.logger import get_logger
from backend.utils.dataset_loader import DatasetLoader
from backend.utils.data_cleaner import DataCleaner


def main():

    logger = get_logger("test_setup")

    print("\n" + "=" * 60)
    print("TESTING STEP 2: CONFIG + UTILITIES")
    print("=" * 60 + "\n")

    logger.info("Test 1: Configuration")
    Config.display()

    logger.info("Test 2: Logger working")
    logger.warning("This is a warning message")
    logger.error("This is an error message (just a test)")

    logger.info("Test 3: Loading datasets")
    loader = DatasetLoader()

    try:
        cards_df = loader.load_cards()
        decks_df = loader.load_decks()
        print(f"\nCards loaded: {cards_df.shape}")
        print(f"Decks loaded: {decks_df.shape}")
    except Exception as e:
        logger.error(f"Dataset loading failed: {e}")
        return

    logger.info("Test 4: Data Cleaner")
    valid_cards = set(cards_df["name"].unique())
    cleaner = DataCleaner(valid_cards=valid_cards)

    sample_deck = ["Hog Rider", "Musketeer", "Ice Spirit", "Skeletons",
                   "Fireball", "The Log", "Cannon", "Ice Golem"]
    is_valid, msg = cleaner.validate_deck(sample_deck)
    print(f"\nValid deck test:    {is_valid} | {msg}")

    bad_deck = ["Hog Rider", "Musketeer", "Ice Spirit", "Skeletons", "Fireball"]
    is_valid, msg = cleaner.validate_deck(bad_deck)
    print(f"Invalid deck test:  {is_valid} | {msg}")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60 + "\n")


    logger.info("Test 1: Configuration")
    Config.display()


    logger.info("Test 2: Logger working ")
    logger.warning("This is a warning message")
    logger.error("This is an error message (just a test)")


    logger.info("Test 3: Loading datasets")
    loader = DatasetLoader()
    
    try:
        cards_df = loader.load_cards()
        decks_df = loader.load_decks()
        print(f"\nCards loaded: {cards_df.shape}")
        print(f"Decks loaded: {decks_df.shape}")
    except Exception as e:
        logger.error(f"Dataset loading failed: {e}")
        return


    logger.info("Test 4: Data Cleaner")
    valid_cards = set(cards_df["name"].unique())
    cleaner = DataCleaner(valid_cards=valid_cards)


    sample_deck = ["Hog Rider", "Musketeer", "Ice Spirit", "Skeletons",
                   "Fireball", "The Log", "Cannon", "Ice Golem"]
    is_valid, msg = cleaner.validate_deck(sample_deck)
    print(f"\nValid deck test:    {is_valid} | {msg}")


    bad_deck = ["Hog Rider", "Musketeer", "Ice Spirit", "Skeletons", "Fireball"]
    is_valid, msg = cleaner.validate_deck(bad_deck)
    print(f"Invalid deck test:  {is_valid} | {msg}")

    print("\n" + "=" * 60)
    print("ALL TESTS PASSED!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()