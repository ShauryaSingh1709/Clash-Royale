"""
==========================================================================
🏆 CLASH ROYALE DECK ANALYZER - Card Model
==========================================================================

OOP representation of a single Clash Royale card.

Usage:
    from backend.models.card import Card

    card = Card(
        name="Hog Rider",
        elixir_cost=4,
        rarity="Rare",
        card_type="Troop",
        damage=264,
        hitpoints=776
    )
    print(card)
    print(card.is_cheap)
"""

from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Card:
    """
    Represents a single Clash Royale card.

    Attributes:
        name (str):            Card name (e.g., "Hog Rider")
        elixir_cost (int):     Elixir cost (1-9)
        rarity (str):          Common, Rare, Epic, Legendary, Champion
        card_type (str):       Troop, Spell, or Building
        damage (float):        Damage value
        hitpoints (float):     Hit points
        archetype (str):       Beatdown, Control, Cycle, Siege, Hog Cycle
        win_rate (float):      Win rate percentage (0-100)
        usage_rate (float):    Usage rate percentage (0-100)
        arena_unlocked (int):  Arena where card unlocks
        card_id (Optional):    Optional unique ID
    """

    name: str
    elixir_cost: int
    rarity: str
    card_type: str
    damage: float = 0.0
    hitpoints: float = 0.0
    archetype: str = "Unknown"
    win_rate: float = 0.0
    usage_rate: float = 0.0
    arena_unlocked: int = 0
    card_id: Optional[int] = None

    # ========================================================================
    # 🎯 COMPUTED PROPERTIES
    # ========================================================================

    @property
    def is_cheap(self) -> bool:
        """Returns True if card costs 2 elixir or less."""
        return self.elixir_cost <= 2

    @property
    def is_expensive(self) -> bool:
        """Returns True if card costs 6 elixir or more."""
        return self.elixir_cost >= 6

    @property
    def cost_category(self) -> str:
        """Returns elixir cost category."""
        if self.elixir_cost <= 2:
            return "Cheap"
        elif self.elixir_cost <= 4:
            return "Medium"
        elif self.elixir_cost <= 6:
            return "Expensive"
        return "Heavy"

    @property
    def damage_per_elixir(self) -> float:
        """Returns damage per elixir efficiency."""
        if self.elixir_cost == 0:
            return 0.0
        return round(self.damage / self.elixir_cost, 2)

    @property
    def hp_per_elixir(self) -> float:
        """Returns HP per elixir efficiency."""
        if self.elixir_cost == 0:
            return 0.0
        return round(self.hitpoints / self.elixir_cost, 2)

    @property
    def is_legendary(self) -> bool:
        """Returns True if card is legendary or champion."""
        return self.rarity in ("Legendary", "Champion")

    @property
    def is_troop(self) -> bool:
        """Returns True if card is a troop."""
        return self.card_type == "Troop"

    @property
    def is_spell(self) -> bool:
        """Returns True if card is a spell."""
        return self.card_type == "Spell"

    @property
    def is_building(self) -> bool:
        """Returns True if card is a building."""
        return self.card_type == "Building"

    # ========================================================================
    # 🛠️ METHODS
    # ========================================================================

    def to_dict(self) -> dict:
        """
        Convert Card to dictionary (for JSON API responses).

        Returns:
            dict: Card data as dictionary
        """
        data = asdict(self)
        # Add computed properties
        data.update({
            "is_cheap": self.is_cheap,
            "is_expensive": self.is_expensive,
            "cost_category": self.cost_category,
            "damage_per_elixir": self.damage_per_elixir,
            "hp_per_elixir": self.hp_per_elixir,
        })
        return data

    @classmethod
    def from_dict(cls, data: dict) -> "Card":
        """
        Create Card from dictionary (e.g., from pandas row).

        Args:
            data: Dictionary with card attributes

        Returns:
            Card: New Card instance
        """
        return cls(
            name=data.get("name", "Unknown"),
            elixir_cost=int(data.get("elixir_cost", 0)),
            rarity=data.get("rarity", "Common"),
            card_type=data.get("type", "Troop"),
            damage=float(data.get("damage", 0)),
            hitpoints=float(data.get("hitpoints", 0)),
            archetype=data.get("archetype", "Unknown"),
            win_rate=float(data.get("win_rate", 0)),
            usage_rate=float(data.get("usage_rate", 0)),
            arena_unlocked=int(data.get("arena_unlocked", 0)),
            card_id=data.get("card_id"),
        )

    # ========================================================================
    # 🎨 MAGIC METHODS
    # ========================================================================

    def __str__(self) -> str:
        """Pretty print representation."""
        return f"🃏 {self.name} (⚡{self.elixir_cost} | {self.rarity} | {self.card_type})"

    def __repr__(self) -> str:
        """Developer representation."""
        return f"Card(name='{self.name}', elixir={self.elixir_cost}, rarity='{self.rarity}')"

    def __eq__(self, other: object) -> bool:
        """Two cards are equal if names match."""
        if not isinstance(other, Card):
            return False
        return self.name == other.name

    def __hash__(self) -> int:
        """Make Card hashable (so we can use it in sets)."""
        return hash(self.name)