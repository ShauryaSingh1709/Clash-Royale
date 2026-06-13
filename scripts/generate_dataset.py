








import pandas as pd
import numpy as np
import random
from pathlib import Path
from real_meta_database import REAL_META_DECKS

np.random.seed(42)
random.seed(42)

OUTPUT_DIR = Path("dataset/raw")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)







CARDS_DATA = [



    ("Knight", 3, "Common", "Troop", 0, 202, 1766, "Beatdown"),
    ("Archers", 3, "Common", "Troop", 0, 112, 304, "Control"),
    ("Bomber", 2, "Common", "Troop", 2, 225, 304, "Control"),
    ("Goblins", 2, "Common", "Troop", 1, 120, 202, "Cycle"),
    ("Spear Goblins", 2, "Common", "Troop", 1, 81, 133, "Cycle"),
    ("Skeletons", 1, "Common", "Troop", 2, 81, 81, "Cycle"),
    ("Minions", 3, "Common", "Troop", 0, 107, 230, "Control"),
    ("Minion Horde", 5, "Common", "Troop", 4, 107, 230, "Control"),
    ("Barbarians", 5, "Common", "Troop", 3, 192, 670, "Beatdown"),
    ("Royal Giant", 6, "Common", "Troop", 7, 307, 3164, "Siege"),
    ("Royal Recruits", 7, "Common", "Troop", 10, 133, 787, "Beatdown"),
    ("Rascals", 5, "Common", "Troop", 11, 217, 1940, "Control"),
    ("Elite Barbarians", 6, "Common", "Troop", 9, 384, 1341, "Beatdown"),
    ("Fire Spirit", 1, "Common", "Troop", 5, 207, 230, "Cycle"),
    ("Ice Spirit", 1, "Common", "Troop", 8, 110, 230, "Cycle"),
    ("Heal Spirit", 1, "Common", "Troop", 13, 110, 230, "Cycle"),
    ("Electro Spirit", 1, "Common", "Troop", 12, 99, 230, "Cycle"),
    ("Firecracker", 3, "Common", "Troop", 12, 64, 304, "Control"),
    ("Dart Goblin", 3, "Common", "Troop", 9, 151, 261, "Cycle"),
    ("Goblin Gang", 3, "Common", "Troop", 9, 120, 202, "Cycle"),
    ("Royal Hogs", 5, "Common", "Troop", 10, 74, 837, "Beatdown"),
    ("Skeleton Barrel", 3, "Common", "Troop", 12, 145, 532, "Cycle"),
    ("Wall Breakers", 2, "Common", "Troop", 12, 350, 330, "Cycle"),
    



    ("Mini PEKKA", 4, "Rare", "Troop", 0, 755, 1390, "Control"),
    ("Musketeer", 4, "Rare", "Troop", 0, 217, 721, "Control"),
    ("Giant", 5, "Rare", "Troop", 0, 253, 4090, "Beatdown"),
    ("Valkyrie", 4, "Rare", "Troop", 1, 266, 1907, "Control"),
    ("Hog Rider", 4, "Rare", "Troop", 4, 317, 1697, "Hog Cycle"),
    ("Wizard", 5, "Rare", "Troop", 5, 281, 755, "Control"),
    ("Three Musketeers", 9, "Rare", "Troop", 7, 217, 721, "Beatdown"),
    ("Battle Ram", 4, "Rare", "Troop", 9, 286, 967, "Beatdown"),
    ("Zappies", 4, "Rare", "Troop", 11, 117, 529, "Control"),
    ("Mega Minion", 3, "Rare", "Troop", 6, 311, 837, "Control"),
    ("Flying Machine", 4, "Rare", "Troop", 6, 171, 614, "Control"),
    ("Ice Golem", 2, "Rare", "Troop", 8, 84, 1315, "Cycle"),
    ("Battle Healer", 4, "Rare", "Troop", 13, 148, 1717, "Beatdown"),
    ("Elixir Golem", 3, "Rare", "Troop", 6, 253, 1569, "Beatdown"),
    ("Berserker", 2, "Rare", "Troop", 13, 102, 896, "Cycle"),
    



    ("Witch", 5, "Epic", "Troop", 5, 135, 839, "Beatdown"),
    ("Skeleton Army", 3, "Epic", "Troop", 2, 81, 81, "Control"),
    ("Baby Dragon", 4, "Epic", "Troop", 0, 161, 1152, "Beatdown"),
    ("Prince", 5, "Epic", "Troop", 1, 391, 1920, "Beatdown"),
    ("Giant Skeleton", 6, "Epic", "Troop", 1, 276, 3617, "Beatdown"),
    ("Balloon", 5, "Epic", "Troop", 6, 640, 1679, "Beatdown"),
    ("PEKKA", 7, "Epic", "Troop", 4, 816, 3760, "Beatdown"),
    ("Dark Prince", 4, "Epic", "Troop", 1, 266, 1440, "Beatdown"),
    ("Hunter", 4, "Epic", "Troop", 11, 84, 885, "Control"),
    ("Bowler", 5, "Epic", "Troop", 10, 289, 2081, "Beatdown"),
    ("Executioner", 5, "Epic", "Troop", 11, 168, 1280, "Control"),
    ("Cannon Cart", 5, "Epic", "Troop", 12, 212, 1809, "Beatdown"),
    ("Guards", 3, "Epic", "Troop", 7, 117, 337, "Control"),
    ("Bats", 2, "Epic", "Troop", 6, 81, 81, "Cycle"),
    ("Goblin Brawler", 4, "Epic", "Troop", 14, 337, 1080, "Beatdown"),
    ("Goblin Giant", 6, "Epic", "Troop", 12, 176, 3020, "Beatdown"),
    ("Goblin Demolisher", 4, "Epic", "Troop", 14, 186, 1300, "Beatdown"),
    ("Electro Dragon", 5, "Epic", "Troop", 13, 192, 949, "Control"),
    ("Electro Giant", 7, "Epic", "Troop", 14, 163, 3855, "Beatdown"),
    ("Skeleton Dragons", 4, "Epic", "Troop", 14, 161, 560, "Beatdown"),
    ("Suspicious Bush", 2, "Epic", "Troop", 14, 0, 81, "Cycle"),
    ("Bush Goblins", 0, "Epic", "Troop", 14, 256, 304, "Cycle"),
    ("Rune Giant", 4, "Epic", "Troop", 14, 120, 2662, "Beatdown"),
    



    ("Electro Wizard", 4, "Legendary", "Troop", 11, 115, 714, "Control"),
    ("Royal Ghost", 3, "Legendary", "Troop", 7, 261, 1210, "Control"),
    ("Princess", 3, "Legendary", "Troop", 7, 168, 261, "Control"),
    ("Ice Wizard", 3, "Legendary", "Troop", 8, 89, 688, "Control"),
    ("Miner", 3, "Legendary", "Troop", 6, 194, 1210, "Cycle"),
    ("Sparky", 6, "Legendary", "Troop", 6, 1331, 1451, "Beatdown"),
    ("Lava Hound", 7, "Legendary", "Troop", 0, 53, 3581, "Beatdown"),
    ("Inferno Dragon", 4, "Legendary", "Troop", 6, 422, 1295, "Beatdown"),
    ("Lumberjack", 4, "Legendary", "Troop", 6, 256, 1282, "Beatdown"),
    ("Night Witch", 4, "Legendary", "Troop", 6, 314, 906, "Beatdown"),
    ("Bandit", 3, "Legendary", "Troop", 9, 194, 906, "Control"),
    ("Mega Knight", 7, "Legendary", "Troop", 10, 268, 3993, "Beatdown"),
    ("Magic Archer", 4, "Legendary", "Troop", 11, 143, 529, "Control"),
    ("Ram Rider", 5, "Legendary", "Troop", 12, 250, 1697, "Beatdown"),
    ("Fisherman", 3, "Legendary", "Troop", 13, 194, 870, "Control"),
    ("Mother Witch", 4, "Legendary", "Troop", 12, 133, 529, "Control"),
    ("Phoenix", 4, "Legendary", "Troop", 14, 217, 1052, "Control"),
    ("Elixir Golemite", 0, "Legendary", "Troop", 14, 128, 762, "Beatdown"),
    



    ("Royal Champion", 7, "Champion", "Troop", 0, 0, 0, "Beatdown"),
    ("Archer Queen", 5, "Champion", "Troop", 0, 225, 1000, "Control"),
    ("Skeleton King", 4, "Champion", "Troop", 0, 204, 2298, "Beatdown"),
    ("Mighty Miner", 4, "Champion", "Troop", 0, 409, 2250, "Control"),
    ("Goblinstein", 5, "Champion", "Troop", 0, 92, 721, "Beatdown"),
    ("Little Prince", 3, "Champion", "Troop", 0, 104, 698, "Control"),
    ("Monk", 5, "Champion", "Troop", 0, 422, 2214, "Beatdown"),
    ("Golden Knight", 4, "Champion", "Troop", 0, 161, 1799, "Beatdown"),
    ("Boss Bandit", 6, "Champion", "Troop", 0, 245, 2624, "Beatdown"),
    ("Spirit Empress", 6, "Champion", "Troop", 0, 307, 1244, "Control"),
    



    ("Fireball", 4, "Rare", "Spell", 0, 688, 0, "Control"),
    ("Arrows", 3, "Common", "Spell", 0, 366, 0, "Control"),
    ("Zap", 2, "Common", "Spell", 5, 192, 0, "Control"),
    ("Rocket", 6, "Rare", "Spell", 0, 1484, 0, "Siege"),
    ("Lightning", 6, "Epic", "Spell", 0, 1057, 0, "Control"),
    ("Freeze", 4, "Epic", "Spell", 0, 148, 0, "Control"),
    ("Poison", 4, "Epic", "Spell", 0, 736, 0, "Control"),
    ("Goblin Barrel", 3, "Epic", "Spell", 1, 120, 0, "Cycle"),
    ("The Log", 2, "Legendary", "Spell", 6, 268, 0, "Control"),
    ("Tornado", 3, "Epic", "Spell", 6, 84, 0, "Control"),
    ("Graveyard", 5, "Legendary", "Spell", 1, 81, 0, "Control"),
    ("Clone", 3, "Epic", "Spell", 9, 0, 0, "Beatdown"),
    ("Mirror", 1, "Epic", "Spell", 5, 0, 0, "Beatdown"),
    ("Rage", 2, "Epic", "Spell", 4, 179, 0, "Beatdown"),
    ("Earthquake", 3, "Rare", "Spell", 8, 243, 0, "Siege"),
    ("Royal Delivery", 3, "Common", "Spell", 9, 437, 0, "Control"),
    ("Giant Snowball", 2, "Common", "Spell", 13, 179, 0, "Control"),
    ("Barbarian Barrel", 2, "Epic", "Spell", 14, 230, 0, "Cycle"),
    ("Goblin Curse", 2, "Epic", "Spell", 14, 210, 0, "Control"),
    ("Vines", 3, "Epic", "Spell", 14, 306, 0, "Control"),
    ("Void", 3, "Epic", "Spell", 14, 1020, 0, "Control"),
    



    ("Bomb Tower", 4, "Rare", "Building", 2, 222, 1356, "Control"),
    ("Cannon", 3, "Common", "Building", 3, 212, 824, "Control"),
    ("Tesla", 4, "Common", "Building", 4, 220, 1152, "Control"),
    ("Inferno Tower", 5, "Rare", "Building", 4, 847, 1748, "Control"),
    ("Mortar", 4, "Common", "Building", 1, 266, 1369, "Siege"),
    ("X-Bow", 6, "Epic", "Building", 1, 43, 1600, "Siege"),
    ("Goblin Cage", 4, "Rare", "Building", 10, 0, 780, "Control"),
    



    ("Goblin Hut", 5, "Rare", "Building", 1, 32, 1180, "Control"),
    ("Furnace", 4, "Rare", "Building", 8, 179, 727, "Control"),
    ("Tombstone", 3, "Rare", "Building", 5, 0, 529, "Control"),
    ("Elixir Collector", 6, "Rare", "Building", 5, 0, 1070, "Beatdown"),
    ("Barbarian Hut", 6, "Rare", "Building", 14, 0, 1164, "Beatdown"),
    ("Goblin Drill", 4, "Epic", "Building", 14, 84, 1313, "Siege"),
    



    ("Cannoneer", 0, "Tower", "Tower Troop", 0, 320, 2616, "Tower"),
    ("Dagger Duchess", 0, "Tower", "Tower Troop", 0, 214, 2768, "Tower"),
    ("Royal Chef", 0, "Tower", "Tower Troop", 0, 109, 2703, "Tower"),
    ("Tower Princess", 0, "Tower", "Tower Troop", 0, 109, 3052, "Tower"),
]






def generate_cards_csv():

    print(f"Generating cards.csv with OFFICIAL data...")
    
    cards = []
    for idx, (name, elixir, rarity, ctype, arena, dmg, hp, archetype) in enumerate(CARDS_DATA, 1):

        if ctype == "Tower Troop":
            win_rate = round(np.random.uniform(48, 55), 2)
            usage_rate = round(np.random.uniform(15, 30), 2)
        else:

            card_appearances = sum(1 for d in REAL_META_DECKS if name in d["cards"])
            
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
    print(f"cards.csv dataset with {len(df)} cards saved (including tower troops)\n")
    return df


def generate_decks_csv(cards_df: pd.DataFrame, target_count: int = 500):

    print(f"Generating decks from REAL meta templates...")

    card_dict = cards_df.set_index('name').to_dict('index')
    decks = []
    deck_id = 1

    variations_per_deck = max(1, target_count // len(REAL_META_DECKS))
    skipped = []
    
    for template in REAL_META_DECKS:
        cards = template["cards"]
        
        valid_cards = [c for c in cards if c in card_dict]
        if len(valid_cards) < 8:
            missing = [c for c in cards if c not in card_dict]
            skipped.append(f"{template['name']}: missing {missing}")
            continue
        
        avg_elixir = round(
            sum(card_dict[c]['elixir_cost'] for c in valid_cards[:8]) / 8, 2
        )
        
        for variation in range(variations_per_deck):
            base_wr = template["win_rate"]
            win_rate = round(max(35, min(70, base_wr + np.random.uniform(-1.5, 1.5))), 2)
            
            base_usage = template["usage_rate"]
            usage_count = max(0, int(base_usage * 100 + np.random.uniform(-50, 100)))
            total_battles = max(1, int(usage_count * np.random.uniform(3, 8)))
            
            decks.append({
                "deck_id": deck_id,
                "deck_name": template["name"],
                "tier": template["tier"],
                "source": template.get("source", ""),
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
    
    if skipped:
        print(f"Skipped {len(skipped)} decks (missing cards)")
    
    df = pd.DataFrame(decks)
    df.to_csv(OUTPUT_DIR / "decks.csv", index=False)
    print(f"decks.csv deck saved\n")
    return df


def generate_battles_csv(cards_df: pd.DataFrame, decks_df: pd.DataFrame, num_battles: int = 5000):

    print(f"Generating {num_battles} battles...")
    
    battles = []
    for battle_id in range(1, num_battles + 1):
        d1 = decks_df.sample(1).iloc[0]
        d2 = decks_df.sample(1).iloc[0]
        
        p1_deck = [d1[f'card_{i}'] for i in range(1, 9)]
        p2_deck = [d2[f'card_{i}'] for i in range(1, 9)]
        
        trophy_base = random.choice([4500, 5500, 6500, 7500])
        p1_trophies = trophy_base + np.random.randint(-200, 200)
        p2_trophies = trophy_base + np.random.randint(-200, 200)
        
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
    print(f"battles.csv saved\n")
    return df


def generate_meta_stats_csv(cards_df: pd.DataFrame):

    print("Generating meta_stats.csv...")
    
    seasons = ["Season_45", "Season_46", "Season_47", "Season_48", "Season_49"]
    meta_stats = []
    
    for _, row in cards_df.iterrows():
        card_name = row['name']
        base_wr = float(row['win_rate'])
        base_usage = float(row['usage_rate'])
        
        primary_trend = random.choices(
            ["Stable", "Rising", "Falling"],
            weights=[0.5, 0.25, 0.25]
        )[0]
        
        for i, season in enumerate(seasons):
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
    print(f"meta_stats.csv meta records saved\n")
    return df






def main():
    print("=" * 60)
    print("ROYALEFORGE - OFFICIAL CR DATA GENERATOR")
    print("=" * 60 + "\n")

    print(f"Loaded {len(REAL_META_DECKS)} REAL meta decks")
    print(f"Total cards in database: {len(CARDS_DATA)}\n")

    cards_df = generate_cards_csv()
    decks_df = generate_decks_csv(cards_df, target_count=500)
    battles_df = generate_battles_csv(cards_df, decks_df, num_battles=5000)
    meta_df = generate_meta_stats_csv(cards_df)

    print("=" * 60)
    print("DATASETS GENERATED!")
    print("=" * 60)

    troops = sum(1 for c in CARDS_DATA if c[3] == "Troop")
    spells = sum(1 for c in CARDS_DATA if c[3] == "Spell")
    buildings = sum(1 for c in CARDS_DATA if c[3] == "Building")
    towers = sum(1 for c in CARDS_DATA if c[3] == "Tower Troop")

    print(f"\nCard Distribution:")
    print(f"   Troops:       {troops}")
    print(f"   Spells:       {spells}")
    print(f"   Buildings:    {buildings}")
    print(f"   Tower Troops: {towers}")
    print(f"   TOTAL:        {len(CARDS_DATA)}")

    print(f"\nBy Rarity:")
    rarities = {}
    for c in CARDS_DATA:
        rarities[c[2]] = rarities.get(c[2], 0) + 1
    for r, count in sorted(rarities.items()):
        print(f"   {r}: {count}")

    print(f"\nNext Steps:")
    print(f"   1. Re-run notebook 02 (Data Cleaning)")
    print(f"   2. Re-run notebook 04 (ML Training)")
    print(f"   3. Re-run notebook 05 (Recommendations)")
    print(f"   4. Restart Flask server")


if __name__ == "__main__":
    main()