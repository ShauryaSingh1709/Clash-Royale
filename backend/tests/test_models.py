from backend.models.card import Card
from backend.models.deck import Deck
from backend.models.battle import Battle
from backend.utils.dataset_loader import DatasetLoader
from backend.utils.logger import get_logger

logger = get_logger("test_models")


def test_card():

    print("\n" + "=" * 60)
    print("TEST 1: CARD CLASS")
    print("=" * 60)

    card = Card(
        name="Hog Rider",
        elixir_cost=4,
        rarity="Rare",
        card_type="Troop",
        damage=264,
        hitpoints=776,
        archetype="Hog Cycle",
        win_rate=55.5,
        usage_rate=20.3
    )

    print(card)
    print(f"   Is cheap?:           {card.is_cheap}")
    print(f"   Cost category:       {card.cost_category}")
    print(f"   Damage per elixir:   {card.damage_per_elixir}")
    print(f"   HP per elixir:       {card.hp_per_elixir}")
    print(f"   Is troop?:           {card.is_troop}")


def test_deck():

    print("\n" + "=" * 60)
    print("TEST 2: DECK CLASS")
    print("=" * 60)

    loader = DatasetLoader()
    cards_df = loader.load_cards()
    card_lookup = cards_df.set_index("name").to_dict("index")

    user_deck = ["Hog Rider", "Musketeer", "Ice Spirit", "Skeletons",
                 "Fireball", "The Log", "Cannon", "Ice Golem"]

    deck = Deck.from_card_names(user_deck, card_lookup)

    print(deck)
    print(f"\nDECK STATS:")
    print(f"   Average Elixir:      {deck.average_elixir}")
    print(f"   Total Elixir:        {deck.total_elixir}")
    print(f"   Average Damage:      {deck.average_damage}")
    print(f"   Average HP:          {deck.average_hp}")
    print(f"   Primary Archetype:   {deck.primary_archetype}")

    print(f"\nCOMPOSITION:")
    print(f"   Troops:    {deck.num_troops}")
    print(f"   Spells:    {deck.num_spells}")
    print(f"   Buildings: {deck.num_buildings}")
    print(f"   Legendary: {deck.num_legendary}")

    print(f"\nANALYSIS:")
    print(f"   Is cheap cycle?:        {deck.is_cheap_cycle}")
    print(f"   Is heavy beatdown?:     {deck.is_heavy_beatdown}")
    print(f"   Has win condition?:     {deck.has_win_condition}")
    print(f"   Weakest card:           {deck.get_weakest_card().name}")
    print(f"   Strongest card:         {deck.get_strongest_card().name}")
    print(f"   'Hog Rider' in deck?:   {'Hog Rider' in deck}")


def test_battle():

    print("\n" + "=" * 60)
    print("TEST 3: BATTLE CLASS")
    print("=" * 60)

    loader = DatasetLoader()
    cards_df = loader.load_cards()
    card_lookup = cards_df.set_index("name").to_dict("index")

    deck1 = Deck.from_card_names(
        ["Hog Rider", "Musketeer", "Ice Spirit", "Skeletons",
         "Fireball", "The Log", "Cannon", "Ice Golem"],
        card_lookup
    )

    deck2 = Deck.from_card_names(
        ["Giant", "Wizard", "Mini PEKKA", "Archers",
         "Arrows", "Knight", "Bomber", "Goblins"],
        card_lookup
    )

    battle = Battle(
        battle_id=1,
        player_1_deck=deck1,
        player_2_deck=deck2,
        player_1_crowns=3,
        player_2_crowns=1,
        player_1_trophies=5200,
        player_2_trophies=5050,
        duration_sec=185,
        game_mode="Ladder"
    )

    print(battle)
    print(f"\nBATTLE STATS:")
    print(f"   Winner:            {battle.winner}")
    print(f"   Crown Difference:  {battle.crown_difference}")
    print(f"   Dominant Win?:     {battle.is_dominant_win}")
    print(f"   Match Type:        {battle.match_type}")
    print(f"   Duration:          {battle.duration_minutes} minutes")
    print(f"   Intensity:         {battle.battle_intensity} total crowns")


def main():

    print("\n" + "=" * 70)
    print("TESTING STEP 3: OOP MODELS")
    print("=" * 70)

    test_card()
    test_deck()
    test_battle()

    print("\n" + "=" * 70)
    print("ALL MODEL TESTS PASSED!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()