





















from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Card:

















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





    @property
    def is_cheap(self) -> bool:

        return self.elixir_cost <= 2

    @property
    def is_expensive(self) -> bool:

        return self.elixir_cost >= 6

    @property
    def cost_category(self) -> str:

        if self.elixir_cost <= 2:
            return "Cheap"
        elif self.elixir_cost <= 4:
            return "Medium"
        elif self.elixir_cost <= 6:
            return "Expensive"
        return "Heavy"

    @property
    def damage_per_elixir(self) -> float:

        if self.elixir_cost == 0:
            return 0.0
        return round(self.damage / self.elixir_cost, 2)

    @property
    def hp_per_elixir(self) -> float:

        if self.elixir_cost == 0:
            return 0.0
        return round(self.hitpoints / self.elixir_cost, 2)

    @property
    def is_legendary(self) -> bool:

        return self.rarity in ("Legendary", "Champion")

    @property
    def is_troop(self) -> bool:

        return self.card_type == "Troop"

    @property
    def is_spell(self) -> bool:

        return self.card_type == "Spell"

    @property
    def is_building(self) -> bool:

        return self.card_type == "Building"





    def to_dict(self) -> dict:






        data = asdict(self)

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





    def __str__(self) -> str:

        return f"🃏 {self.name} (⚡{self.elixir_cost} | {self.rarity} | {self.card_type})"

    def __repr__(self) -> str:

        return f"Card(name='{self.name}', elixir={self.elixir_cost}, rarity='{self.rarity}')"

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, Card):
            return False
        return self.name == other.name

    def __hash__(self) -> int:

        return hash(self.name)