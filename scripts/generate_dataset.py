"""
Clash Royale Dataset Generator
================================
Generates realistic CSV datasets for the Clash Royale Deck Analyzer project.

Files Generated:
    - cards.csv       : All 100+ Clash Royale cards with stats
    - decks.csv       : 500 popular deck combinations
    - battles.csv     : 5000 simulated battle records
    - meta_stats.csv  : Card usage and win rate statistics

Author: Clash Royale Deck Analyzer Team
"""

import pandas as pd
import numpy as np
import random
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

# Output directory
OUTPUT_DIR = Path("dataset/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ====================================================================
# 1. CARDS DATA
# ====================================================================

CARDS_DATA = [
    # name, elixir, rarity, type, arena, damage, hp, archetype
    ("Knight", 3, "Common", "Troop", 0, 79, 685, "Beatdown"),
    ("Archers", 3, "Common", "Troop", 0, 42, 125, "Control"),
    ("Bomber", 3, "Common", "Troop", 2, 75, 150, "Control"),
    ("Goblins", 2, "Common", "Troop", 1, 47, 80, "Cycle"),
    ("Spear Goblins", 2, "Common", "Troop", 1, 32, 52, "Cycle"),
    ("Skeletons", 1, "Common", "Troop", 2, 67, 67, "Cycle"),
    ("Minions", 3, "Common", "Troop", 0, 40, 90, "Control"),
    ("Minion Horde", 5, "Common", "Troop", 4, 40, 90, "Control"),
    ("Barbarians", 5, "Common", "Troop", 3, 75, 262, "Beatdown"),
    ("Royal Giant", 6, "Common", "Troop", 7, 122, 1200, "Siege"),
    ("Cannon", 3, "Common", "Building", 3, 67, 380, "Control"),
    ("Tesla", 4, "Common", "Building", 4, 79, 450, "Control"),
    ("Mortar", 4, "Common", "Building", 1, 110, 600, "Siege"),
    ("Fire Spirit", 2, "Common", "Troop", 5, 169, 60, "Cycle"),
    ("Ice Spirit", 1, "Common", "Troop", 8, 79, 90, "Cycle"),
    ("Royal Recruits", 7, "Common", "Troop", 10, 75, 286, "Beatdown"),
    ("Rascals", 5, "Common", "Troop", 11, 70, 286, "Control"),
    ("Elite Barbarians", 6, "Common", "Troop", 9, 188, 524, "Beatdown"),

    ("Mini PEKKA", 4, "Rare", "Troop", 0, 340, 642, "Control"),
    ("Musketeer", 4, "Rare", "Troop", 0, 142, 340, "Control"),
    ("Giant", 5, "Rare", "Troop", 0, 132, 2000, "Beatdown"),
    ("Valkyrie", 4, "Rare", "Troop", 1, 152, 836, "Control"),
    ("Fireball", 4, "Rare", "Spell", 0, 572, 0, "Control"),
    ("Arrows", 3, "Common", "Spell", 0, 137, 0, "Control"),
    ("Hog Rider", 4, "Rare", "Troop", 4, 264, 776, "Hog Cycle"),
    ("Wizard", 5, "Rare", "Troop", 5, 152, 598, "Control"),
    ("Three Musketeers", 9, "Rare", "Troop", 7, 142, 340, "Beatdown"),
    ("Battle Ram", 4, "Rare", "Troop", 9, 132, 595, "Beatdown"),
    ("Zappies", 4, "Rare", "Troop", 11, 49, 252, "Control"),
    ("Mega Minion", 3, "Rare", "Troop", 6, 138, 252, "Control"),
    ("Goblin Hut", 5, "Rare", "Building", 1, 32, 682, "Control"),
    ("Furnace", 4, "Rare", "Building", 8, 169, 612, "Control"),
    ("Bomb Tower", 4, "Rare", "Building", 2, 75, 950, "Control"),
    ("Flying Machine", 4, "Rare", "Troop", 6, 128, 252, "Control"),
    ("Ice Golem", 2, "Rare", "Troop", 8, 36, 1090, "Cycle"),

    ("Witch", 5, "Epic", "Troop", 5, 56, 696, "Beatdown"),
    ("Skeleton Army", 3, "Epic", "Troop", 2, 67, 67, "Control"),
    ("Baby Dragon", 4, "Epic", "Troop", 0, 100, 1152, "Beatdown"),
    ("Prince", 5, "Epic", "Troop", 1, 220, 1100, "Beatdown"),
    ("Giant Skeleton", 6, "Epic", "Troop", 1, 130, 2126, "Beatdown"),
    ("Balloon", 5, "Epic", "Troop", 6, 600, 1050, "Beatdown"),
    ("PEKKA", 7, "Epic", "Troop", 4, 510, 3286, "Beatdown"),
    ("Goblin Barrel", 3, "Epic", "Spell", 1, 47, 80, "Cycle"),
    ("Freeze", 4, "Epic", "Spell", 0, 100, 0, "Control"),
    ("Rocket", 6, "Rare", "Spell", 0, 1300, 0, "Siege"),
    ("Tombstone", 3, "Rare", "Building", 5, 50, 380, "Control"),
    ("Dark Prince", 4, "Epic", "Troop", 1, 158, 1101, "Beatdown"),
    ("Lightning", 6, "Epic", "Spell", 0, 877, 0, "Control"),
    ("X-Bow", 6, "Epic", "Building", 1, 26, 1200, "Siege"),
    ("Poison", 4, "Epic", "Spell", 0, 128, 0, "Control"),
    ("Hunter", 4, "Epic", "Troop", 11, 79, 754, "Control"),
    ("Goblin Gang", 3, "Common", "Troop", 9, 50, 80, "Cycle"),
    ("Bowler", 5, "Epic", "Troop", 10, 100, 928, "Beatdown"),
    ("Executioner", 5, "Epic", "Troop", 11, 150, 754, "Control"),
    ("Cannon Cart", 5, "Epic", "Troop", 12, 132, 1086, "Beatdown"),
    ("Electro Wizard", 4, "Legendary", "Troop", 11, 79, 598, "Control"),
    ("Royal Ghost", 3, "Legendary", "Troop", 7, 158, 686, "Control"),

    ("Princess", 3, "Legendary", "Troop", 7, 70, 216, "Control"),
    ("Ice Wizard", 3, "Legendary", "Troop", 8, 49, 598, "Control"),
    ("Miner", 3, "Legendary", "Troop", 6, 102, 1000, "Cycle"),
    ("Sparky", 6, "Legendary", "Troop", 6, 1300, 1357, "Beatdown"),
    ("Lava Hound", 7, "Legendary", "Troop", 0, 39, 3150, "Beatdown"),
    ("Inferno Dragon", 4, "Legendary", "Troop", 6, 30, 1004, "Beatdown"),
    ("Graveyard", 5, "Legendary", "Spell", 1, 107, 67, "Control"),
    ("The Log", 2, "Legendary", "Spell", 6, 240, 0, "Control"),
    ("Lumberjack", 4, "Legendary", "Troop", 6, 187, 686, "Beatdown"),
    ("Night Witch", 4, "Legendary", "Troop", 6, 142, 1004, "Beatdown"),
    ("Bandit", 3, "Legendary", "Troop", 9, 158, 750, "Control"),
    ("Mega Knight", 7, "Legendary", "Troop", 10, 158, 2842, "Beatdown"),
    ("Magic Archer", 4, "Legendary", "Troop", 11, 79, 446, "Control"),
    ("Ram Rider", 5, "Legendary", "Troop", 12, 90, 1050, "Beatdown"),
    ("Fisherman", 3, "Legendary", "Troop", 13, 158, 700, "Control"),

    ("Skeleton Barrel", 3, "Common", "Troop", 12, 23, 280, "Cycle"),
    ("Flying Machine", 4, "Rare", "Troop", 6, 128, 252, "Control"),
    ("Wall Breakers", 2, "Epic", "Troop", 12, 158, 134, "Cycle"),
    ("Royal Hogs", 5, "Rare", "Troop", 10, 75, 540, "Beatdown"),
    ("Zap", 2, "Common", "Spell", 5, 159, 0, "Control"),
    ("Tornado", 3, "Epic", "Spell", 6, 88, 0, "Control"),
    ("Clone", 3, "Epic", "Spell", 9, 0, 0, "Beatdown"),
    ("Mirror", 1, "Epic", "Spell", 5, 0, 0, "Beatdown"),
    ("Heal Spirit", 1, "Rare", "Troop", 13, 56, 67, "Cycle"),
    ("Elixir Collector", 6, "Rare", "Building", 5, 0, 870, "Beatdown"),
    ("Inferno Tower", 5, "Rare", "Building", 4, 30, 870, "Control"),
    ("Royal Delivery", 3, "Common", "Spell", 9, 159, 1300, "Control"),
    ("Earthquake", 3, "Rare", "Spell", 8, 89, 0, "Siege"),
    ("Goblin Cage", 4, "Rare", "Building", 10, 56, 800, "Control"),
    ("Battle Healer", 4, "Rare", "Troop", 13, 75, 1232, "Beatdown"),
    ("Firecracker", 3, "Common", "Troop", 12, 84, 216, "Control"),
    ("Elixir Golem", 3, "Rare", "Troop", 6, 39, 1900, "Beatdown"),
    ("Mother Witch", 4, "Legendary", "Troop", 12, 38, 598, "Control"),
    ("Royal Champion", 7, "Champion", "Troop", 0, 150, 1804, "Beatdown"),
    ("Archer Queen", 5, "Champion", "Troop", 0, 122, 904, "Control"),
    ("Skeleton King", 4, "Champion", "Troop", 0, 105, 1804, "Beatdown"),
    ("Mighty Miner", 4, "Champion", "Troop", 0, 95, 1300, "Control"),
    ("Phoenix", 4, "Champion", "Troop", 0, 80, 800, "Control"),
    ("Goblinstein", 5, "Champion", "Troop", 0, 130, 1200, "Beatdown"),
    ("Little Prince", 3, "Champion", "Troop", 0, 70, 600, "Control"),
    ("Monk", 5, "Champion", "Troop", 0, 100, 1400, "Beatdown"),
]


def generate_cards_csv():
    """Generate the cards.csv file with all Clash Royale cards."""
    print("📦 Generating cards.csv...")

    cards = []
    for idx, (name, elixir, rarity, ctype, arena, dmg, hp, archetype) in enumerate(CARDS_DATA, 1):
        # Generate realistic win rate (45-58%)
        win_rate = round(np.random.uniform(45, 58), 2)
        # Generate usage rate (1-25%)
        usage_rate = round(np.random.uniform(1, 25), 2)
        # Generate popularity score
        popularity = round((win_rate * 0.4 + usage_rate * 0.6), 2)

        cards.append({
            "card_id": idx,
            "name": name,
            "elixir_cost": elixir,
            "rarity": rarity,
            "type": ctype,
            "arena_unlocked": arena,
            "damage": dmg,
            "hitpoints": hp,
            "archetype": archetype,
            "win_rate": win_rate,
            "usage_rate": usage_rate,
            "popularity_score": popularity
        })

    df = pd.DataFrame(cards)
    df.to_csv(OUTPUT_DIR / "cards.csv", index=False)
    print(f"✅ cards.csv created with {len(df)} cards\n")
    return df


def generate_decks_csv(cards_df: pd.DataFrame, num_decks: int = 500):
    """Generate the decks.csv file with popular deck combinations."""
    print(f"🃏 Generating decks.csv with {num_decks} decks...")

    archetypes = ["Beatdown", "Control", "Cycle", "Siege", "Hog Cycle"]
    decks = []

    for deck_id in range(1, num_decks + 1):
        # Pick archetype
        archetype = random.choice(archetypes)

        # Select 8 random cards
        deck_cards = cards_df.sample(8)
        card_names = deck_cards["name"].tolist()
        avg_elixir = round(deck_cards["elixir_cost"].mean(), 2)

        # Generate metrics
        win_rate = round(np.random.uniform(40, 65), 2)
        usage_count = np.random.randint(100, 10000)
        total_battles = np.random.randint(1000, 50000)

        decks.append({
            "deck_id": deck_id,
            "card_1": card_names[0],
            "card_2": card_names[1],
            "card_3": card_names[2],
            "card_4": card_names[3],
            "card_5": card_names[4],
            "card_6": card_names[5],
            "card_7": card_names[6],
            "card_8": card_names[7],
            "avg_elixir": avg_elixir,
            "archetype": archetype,
            "win_rate": win_rate,
            "usage_count": usage_count,
            "total_battles": total_battles
        })

    df = pd.DataFrame(decks)
    df.to_csv(OUTPUT_DIR / "decks.csv", index=False)
    print(f"✅ decks.csv created with {len(df)} decks\n")
    return df


def generate_battles_csv(cards_df: pd.DataFrame, num_battles: int = 5000):
    """Generate the battles.csv file with simulated battle records."""
    print(f"⚔️ Generating battles.csv with {num_battles} battles...")

    battles = []
    for battle_id in range(1, num_battles + 1):
        # Player 1 deck
        p1_deck = cards_df.sample(8)["name"].tolist()
        p1_avg_elixir = round(cards_df[cards_df["name"].isin(p1_deck)]["elixir_cost"].mean(), 2)
        p1_trophies = np.random.randint(2000, 7000)
        p1_crowns = np.random.randint(0, 4)

        # Player 2 deck
        p2_deck = cards_df.sample(8)["name"].tolist()
        p2_avg_elixir = round(cards_df[cards_df["name"].isin(p2_deck)]["elixir_cost"].mean(), 2)
        p2_trophies = np.random.randint(2000, 7000)
        p2_crowns = np.random.randint(0, 4)

        # Determine winner
        if p1_crowns > p2_crowns:
            winner = "player_1"
        elif p2_crowns > p1_crowns:
            winner = "player_2"
        else:
            winner = "draw"

        battles.append({
            "battle_id": battle_id,
            "player_1_deck": "|".join(p1_deck),
            "player_1_elixir": p1_avg_elixir,
            "player_1_trophies": p1_trophies,
            "player_1_crowns": p1_crowns,
            "player_2_deck": "|".join(p2_deck),
            "player_2_elixir": p2_avg_elixir,
            "player_2_trophies": p2_trophies,
            "player_2_crowns": p2_crowns,
            "winner": winner,
            "battle_duration_sec": np.random.randint(60, 300),
            "game_mode": random.choice(["Ladder", "Tournament", "Challenge", "Friendly"])
        })

    df = pd.DataFrame(battles)
    df.to_csv(OUTPUT_DIR / "battles.csv", index=False)
    print(f"✅ battles.csv created with {len(df)} battles\n")
    return df


def generate_meta_stats_csv(cards_df: pd.DataFrame):
    """Generate the meta_stats.csv file with meta trends."""
    print("📊 Generating meta_stats.csv...")

    meta_stats = []
    seasons = ["Season_45", "Season_46", "Season_47", "Season_48", "Season_49"]

    for card_name in cards_df["name"]:
        for season in seasons:
            meta_stats.append({
                "card_name": card_name,
                "season": season,
                "usage_rate": round(np.random.uniform(1, 30), 2),
                "win_rate": round(np.random.uniform(42, 60), 2),
                "ranking": np.random.randint(1, 100),
                "trend": random.choice(["Rising", "Falling", "Stable"])
            })

    df = pd.DataFrame(meta_stats)
    df.to_csv(OUTPUT_DIR / "meta_stats.csv", index=False)
    print(f"✅ meta_stats.csv created with {len(df)} records\n")
    return df


def main():
    """Main function to generate all datasets."""
    print("=" * 60)
    print("🏆 CLASH ROYALE DATASET GENERATOR")
    print("=" * 60 + "\n")

    cards_df = generate_cards_csv()
    decks_df = generate_decks_csv(cards_df)
    battles_df = generate_battles_csv(cards_df)
    meta_df = generate_meta_stats_csv(cards_df)

    print("=" * 60)
    print("🎉 ALL DATASETS GENERATED SUCCESSFULLY!")
    print("=" * 60)
    print(f"\n📁 Files saved in: {OUTPUT_DIR.absolute()}")
    print("\nFiles:")
    print(f"  ✅ cards.csv      ({len(cards_df)} rows)")
    print(f"  ✅ decks.csv      ({len(decks_df)} rows)")
    print(f"  ✅ battles.csv    ({len(battles_df)} rows)")
    print(f"  ✅ meta_stats.csv ({len(meta_df)} rows)")
    print("\n🚀 Ready for next step: Data Exploration!")


if __name__ == "__main__":
    main()