from dataclasses import dataclass, field
from typing import Optional
from collections import Counter
from backend.models.card import Card
from backend.config.settings import Config
@dataclass
class Deck:
    cards: list[Card] = field(default_factory=list)
    deck_id: Optional[int] = None
    win_rate: float = 0.0
    usage_count: int = 0

    def __post_init__(self) -> None:

        if self.cards and len(self.cards) != Config.DECK_SIZE:
            raise ValueError(
                f"Deck must contain exactly {Config.DECK_SIZE} cards "
                f"(got {len(self.cards)})"
            )
    @property
    def average_elixir(self) -> float:

        if not self.cards:
            return 0.0
        return round(sum(c.elixir_cost for c in self.cards) / len(self.cards), 2)

    @property
    def total_elixir(self) -> int:

        return sum(c.elixir_cost for c in self.cards)

    @property
    def average_damage(self) -> float:

        if not self.cards:
            return 0.0
        return round(sum(c.damage for c in self.cards) / len(self.cards), 2)

    @property
    def average_hp(self) -> float:

        if not self.cards:
            return 0.0
        return round(sum(c.hitpoints for c in self.cards) / len(self.cards), 2)

    @property
    def average_card_win_rate(self) -> float:

        if not self.cards:
            return 0.0
        return round(sum(c.win_rate for c in self.cards) / len(self.cards), 2)

    @property
    def average_card_usage(self) -> float:

        if not self.cards:
            return 0.0
        return round(sum(c.usage_rate for c in self.cards) / len(self.cards), 2)
    @property
    def num_troops(self) -> int:

        return sum(1 for c in self.cards if c.is_troop)

    @property
    def num_spells(self) -> int:

        return sum(1 for c in self.cards if c.is_spell)

    @property
    def num_buildings(self) -> int:

        return sum(1 for c in self.cards if c.is_building)

    @property
    def num_legendary(self) -> int:

        return sum(1 for c in self.cards if c.rarity == "Legendary")

    @property
    def num_epic(self) -> int:

        return sum(1 for c in self.cards if c.rarity == "Epic")

    @property
    def num_rare(self) -> int:

        return sum(1 for c in self.cards if c.rarity == "Rare")

    @property
    def num_common(self) -> int:

        return sum(1 for c in self.cards if c.rarity == "Common")
    @property
    def primary_archetype(self) -> str:

        if not self.cards:
            return "Unknown"
        archetypes = [c.archetype for c in self.cards if c.archetype != "Unknown"]
        if not archetypes:
            return "Mixed"
        return Counter(archetypes).most_common(1)[0][0]

    @property
    def card_names(self) -> list[str]:

        return [c.name for c in self.cards]

    @property
    def is_cheap_cycle(self) -> bool:

        return self.average_elixir <= 3.0

    @property
    def is_heavy_beatdown(self) -> bool:

        return self.average_elixir >= 4.5

    @property
    def has_win_condition(self) -> bool:

        win_conditions = {
            "Hog Rider", "Giant", "Golem", "Royal Giant", "Balloon",
            "Mega Knight", "Goblin Barrel", "Miner", "Graveyard",
            "X-Bow", "Mortar", "Lava Hound", "Three Musketeers",
            "Royal Hogs", "Ram Rider", "Battle Ram", "Wall Breakers",
            "Sparky", "Elixir Golem", "Skeleton Barrel", "PEKKA"
        }
        return bool(set(self.card_names) & win_conditions)
    def contains_card(self, card_name: str) -> bool:

        return card_name in self.card_names

    def get_card(self, card_name: str) -> Optional[Card]:

        for card in self.cards:
            if card.name == card_name:
                return card
        return None

    def get_weakest_card(self) -> Optional[Card]:

        if not self.cards:
            return None
        return min(self.cards, key=lambda c: c.win_rate)

    def get_strongest_card(self) -> Optional[Card]:

        if not self.cards:
            return None
        return max(self.cards, key=lambda c: c.win_rate)

    def to_dict(self) -> dict:

        return {
            "deck_id": self.deck_id,
            "cards": [c.to_dict() for c in self.cards],
            "card_names": self.card_names,
            "stats": {
                "average_elixir": self.average_elixir,
                "total_elixir": self.total_elixir,
                "average_damage": self.average_damage,
                "average_hp": self.average_hp,
                "average_card_win_rate": self.average_card_win_rate,
                "average_card_usage": self.average_card_usage,
            },
            "composition": {
                "troops": self.num_troops,
                "spells": self.num_spells,
                "buildings": self.num_buildings,
                "legendary": self.num_legendary,
                "epic": self.num_epic,
                "rare": self.num_rare,
                "common": self.num_common,
            },
            "analysis": {
                "primary_archetype": self.primary_archetype,
                "is_cheap_cycle": self.is_cheap_cycle,
                "is_heavy_beatdown": self.is_heavy_beatdown,
                "has_win_condition": self.has_win_condition,
            },
            "win_rate": self.win_rate,
            "usage_count": self.usage_count,
        }

    def to_ml_features(self) -> dict:
        return {
            "avg_elixir": self.average_elixir,
            "total_elixir": self.total_elixir,
            "avg_damage": self.average_damage,
            "avg_hp": self.average_hp,
            "avg_card_win_rate": self.average_card_win_rate,
            "avg_card_usage": self.average_card_usage,
            "num_legendary": self.num_legendary,
            "num_epic": self.num_epic,
            "num_rare": self.num_rare,
            "num_common": self.num_common,
            "num_troops": self.num_troops,
            "num_spells": self.num_spells,
            "num_buildings": self.num_buildings,
        }

    @classmethod
    def from_card_names(cls, card_names: list[str], card_lookup: dict) -> "Deck":
        cards = []
        for name in card_names:
            if name in card_lookup:
                data = card_lookup[name].copy()
                data["name"] = name
                cards.append(Card.from_dict(data))
            else:

                cards.append(Card(
                    name=name, elixir_cost=0, rarity="Unknown",
                    card_type="Unknown"
                ))
        return cls(cards=cards)
    def __str__(self) -> str:

        header = f"Deck ({self.primary_archetype} | {self.average_elixir})"
        cards_str = "\n".join(f"   {i+1}. {c}" for i, c in enumerate(self.cards))
        return f"{header}\n{cards_str}"

    def __repr__(self) -> str:

        return f"Deck(cards={len(self.cards)}, avg_elixir={self.average_elixir})"

    def __len__(self) -> int:

        return len(self.cards)

    def __contains__(self, card_name: str) -> bool:

        return self.contains_card(card_name)

    def __iter__(self):

        return iter(self.cards)