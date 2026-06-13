"""
==========================================================================
🏆 RoyaleForge - Real Meta Dataset Generator
==========================================================================

Uses REAL Clash Royale meta decks from real_meta_database.py
Combined with full cards data for complete dataset generation.
"""

import pandas as pd
import numpy as np
import random
from pathlib import Path
from real_meta_database import REAL_META_DECKS

np.random.seed(42)
random.seed(42)

OUTPUT_DIR = Path("dataset/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# 🃏 ALL CARDS DATA (Complete - 97 cards)
# ============================================================================

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
    
    # Additional cards used in REAL_META_DECKS
    ("Bats", 2, "Epic", "Troop", 6, 67, 67, "Cycle"),
]


# ============================================================================
# 📦 GENERATE FUNCTIONS
# ============================================================================

def generate_cards_csv():
    """Generate cards.csv with realistic statistics."""
    print("📦 Generating cards.csv...")
    
    cards = []
    for idx, (name, elixir, rarity, ctype, arena, dmg, hp, archetype) in enumerate(CARDS_DATA, 1):
        # Determine win/usage based on how often card appears in real meta
        card_appearances = sum(1 for d in REAL_META_DECKS if name in d["cards"])
        
        # More popular cards = higher usage and slightly better win rate
        if card_appearances >= 10:
            win_rate = round(np.random.uniform(52, 58), 2)
            usage_rate = round(np.random.uniform(15, 25), 2)
        elif card_appearances >= 5:
            win_rate = round(np.random.uniform(50, 55), 2)
            usage_rate = round(np.random.uniform(8, 18), 2)
        elif card_appearances >= 2:
            win_rate = round(np.random.uniform(48, 53), 2)
            usage_rate = round(np.random.uniform(3, 10), 2)
        else:
            win_rate = round(np.random.uniform(45, 51), 2)
            usage_rate = round(np.random.uniform(1, 5), 2)
        
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
    print(f"✅ {len(df)} cards saved\n")
    return df


def generate_decks_csv(cards_df: pd.DataFrame, target_count: int = 500):
    """Generate decks from REAL meta templates with variations."""
    print(f"🃏 Generating {target_count} decks from REAL meta templates...")

    card_dict = cards_df.set_index('name').to_dict('index')
    decks = []
    deck_id = 1

    # Calculate how many variations per template to reach target
    multiplier = max(1, target_count // len(REAL_META_DECKS))
    
    for template in REAL_META_DECKS:
        for variation in range(multiplier):
            cards = template["cards"]
            
            # Validate all cards exist in our database
            valid_cards = [c for c in cards if c in card_dict]
            if len(valid_cards) < 8:
                print(f"⚠️  Skipping '{template['name']}' - missing cards: {[c for c in cards if c not in card_dict]}")
                continue
            
            # Calculate REAL average elixir from card data
            avg_elixir = round(
                sum(card_dict[c]['elixir_cost'] for c in valid_cards[:8]) / 8, 2
            )
            
            # Win rate with small variation around base
            base_wr = template["win_rate"]
            win_rate = round(max(35, min(70, base_wr + np.random.uniform(-1.5, 1.5))), 2)
            
            # Usage with variation
            base_usage = template["usage_rate"]
            usage_count = max(0, int(base_usage * 100 + np.random.uniform(-50, 100)))
            total_battles = max(1, int(usage_count * np.random.uniform(3, 8)))
            
            decks.append({
                "deck_id": deck_id,
                "card_1": valid_cards[0],
                "card_2": valid_cards[1],
                "card_3": valid_cards[2],
                "card_4": valid_cards[3],
                "card_5": valid_cards[4],
                "card_6": valid_cards[5],
                "card_7": valid_cards[6],
                "card_8": valid_cards[7],
                "avg_elixir": avg_elixir,
                "archetype": template["archetype"],
                "win_rate": win_rate,
                "usage_count": usage_count,
                "total_battles": total_battles
            })
            deck_id += 1
            
            if len(decks) >= target_count:
                break
        if len(decks) >= target_count:
            break
    
    df = pd.DataFrame(decks)
    df.to_csv(OUTPUT_DIR / "decks.csv", index=False)
    print(f"✅ {len(df)} REAL meta decks saved\n")
    return df


def generate_battles_csv(cards_df: pd.DataFrame, decks_df: pd.DataFrame, num_battles: int = 5000):
    """Generate realistic battles using real decks."""
    print(f"⚔️ Generating {num_battles} battles from real decks...")
    
    battles = []
    for battle_id in range(1, num_battles + 1):
        # Pick two real decks
        d1 = decks_df.sample(1).iloc[0]
        d2 = decks_df.sample(1).iloc[0]
        
        p1_deck = [d1[f'card_{i}'] for i in range(1, 9)]
        p2_deck = [d2[f'card_{i}'] for i in range(1, 9)]
        
        # Realistic trophy ranges
        trophy_base = random.choice([4500, 5500, 6500, 7500])
        p1_trophies = trophy_base + np.random.randint(-200, 200)
        p2_trophies = trophy_base + np.random.randint(-200, 200)
        
        # Crowns based on actual win rate difference
        wr_diff = d1['win_rate'] - d2['win_rate']
        if wr_diff > 4:
            p1_crowns = np.random.choice([2, 3], p=[0.3, 0.7])
            p2_crowns = np.random.choice([0, 1], p=[0.6, 0.4])
        elif wr_diff < -4:
            p1_crowns = np.random.choice([0, 1], p=[0.6, 0.4])
            p2_crowns = np.random.choice([2, 3], p=[0.3, 0.7])
        else:
            p1_crowns = np.random.randint(0, 4)
            p2_crowns = np.random.randint(0, 4)
        
        if p1_crowns > p2_crowns:
            winner = "player_1"
        elif p2_crowns > p1_crowns:
            winner = "player_2"
        else:
            winner = "draw"
        
        battles.append({
            "battle_id": battle_id,
            "player_1_deck": "|".join(p1_deck),
            "player_1_elixir": d1['avg_elixir'],
            "player_1_trophies": p1_trophies,
            "player_1_crowns": p1_crowns,
            "player_2_deck": "|".join(p2_deck),
            "player_2_elixir": d2['avg_elixir'],
            "player_2_trophies": p2_trophies,
            "player_2_crowns": p2_crowns,
            "winner": winner,
            "battle_duration_sec": np.random.randint(60, 300),
            "game_mode": random.choice(["Ladder", "Tournament", "Challenge", "Friendly"])
        })
    
    df = pd.DataFrame(battles)
    df.to_csv(OUTPUT_DIR / "battles.csv", index=False)
    print(f"✅ {len(df)} battles saved\n")
    return df


def generate_meta_stats_csv(cards_df: pd.DataFrame):
    """Generate meta stats with realistic patterns."""
    print("📊 Generating meta_stats.csv...")
    
    seasons = ["Season_45", "Season_46", "Season_47", "Season_48", "Season_49"]
    meta_stats = []
    
    for _, row in cards_df.iterrows():
        card_name = row['name']
        base_wr = float(row['win_rate'])
        base_usage = float(row['usage_rate'])
        
        # Trend pattern: most cards stable, some rising/falling
        primary_trend = random.choices(
            ["Stable", "Rising", "Falling"],
            weights=[0.5, 0.25, 0.25]
        )[0]
        
        for i, season in enumerate(seasons):
            # Apply trend over time
            if primary_trend == "Rising":
                wr_adj = i * 0.5
                usage_adj = i * 0.8
            elif primary_trend == "Falling":
                wr_adj = -i * 0.5
                usage_adj = -i * 0.8
            else:
                wr_adj = 0
                usage_adj = 0
            
            meta_stats.append({
                "card_name": card_name,
                "season": season,
                "usage_rate": round(max(0.1, base_usage + usage_adj + np.random.uniform(-1, 1)), 2),
                "win_rate": round(max(35, min(65, base_wr + wr_adj + np.random.uniform(-1, 1))), 2),
                "ranking": np.random.randint(1, 100),
                "trend": primary_trend
            })
    
    df = pd.DataFrame(meta_stats)
    df.to_csv(OUTPUT_DIR / "meta_stats.csv", index=False)
    print(f"✅ {len(df)} meta records saved\n")
    return df


# ============================================================================
# 🚀 MAIN
# ============================================================================

def main():
    print("=" * 60)
    print("🏆 ROYALEFORGE - REAL META DATA GENERATOR")
    print("=" * 60 + "\n")
    
    print(f"📚 Loaded {len(REAL_META_DECKS)} REAL meta decks from database\n")
    
    # Generate all datasets
    cards_df = generate_cards_csv()
    decks_df = generate_decks_csv(cards_df, target_count=500)
    battles_df = generate_battles_csv(cards_df, decks_df, num_battles=5000)
    meta_df = generate_meta_stats_csv(cards_df)
    
    # Summary
    print("=" * 60)
    print("🎉 DATASETS GENERATED WITH REAL META DECKS!")
    print("=" * 60)
    print(f"\n📁 Files saved in: {OUTPUT_DIR.absolute()}\n")
    print("✨ Real Meta Source:")
    print(f"   • {len(REAL_META_DECKS)} curated competitive decks")
    print(f"   • 4 tiers (S, A, B, C)")
    print(f"   • 4 archetypes (Beatdown, Control, Cycle, Siege)")
    print(f"\n📊 Generated:")
    print(f"   • {len(cards_df)} cards")
    print(f"   • {len(decks_df)} decks (from real templates)")
    print(f"   • {len(battles_df)} battles")
    print(f"   • {len(meta_df)} meta records")
    print(f"\n🚀 Next Steps:")
    print(f"   1. Re-run notebook 02 (Data Cleaning)")
    print(f"   2. Re-run notebook 04 (ML Training)")
    print(f"   3. Re-run notebook 05 (Recommendations)")
    print(f"   4. Restart Flask server")
    print(f"   5. Check dashboard → REAL meta decks!")


if __name__ == "__main__":
    main()