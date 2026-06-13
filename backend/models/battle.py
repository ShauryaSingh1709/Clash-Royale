



















from dataclasses import dataclass, field
from typing import Optional
from backend.models.deck import Deck


@dataclass
class Battle:















    battle_id: Optional[int] = None
    player_1_deck: Optional[Deck] = None
    player_2_deck: Optional[Deck] = None
    player_1_crowns: int = 0
    player_2_crowns: int = 0
    player_1_trophies: int = 0
    player_2_trophies: int = 0
    duration_sec: int = 0
    game_mode: str = "Ladder"





    @property
    def winner(self) -> str:

        if self.player_1_crowns > self.player_2_crowns:
            return "player_1"
        elif self.player_2_crowns > self.player_1_crowns:
            return "player_2"
        return "draw"

    @property
    def is_draw(self) -> bool:

        return self.winner == "draw"

    @property
    def crown_difference(self) -> int:

        return abs(self.player_1_crowns - self.player_2_crowns)

    @property
    def is_dominant_win(self) -> bool:

        return self.crown_difference >= 2

    @property
    def trophy_difference(self) -> int:

        return abs(self.player_1_trophies - self.player_2_trophies)

    @property
    def match_type(self) -> str:

        diff = self.trophy_difference
        if diff < 100:
            return "Balanced"
        elif diff < 500:
            return "Slight Mismatch"
        return "Heavy Mismatch"

    @property
    def battle_intensity(self) -> int:

        return self.player_1_crowns + self.player_2_crowns

    @property
    def duration_minutes(self) -> float:

        return round(self.duration_sec / 60, 2)





    def get_winner_deck(self) -> Optional[Deck]:

        if self.winner == "player_1":
            return self.player_1_deck
        elif self.winner == "player_2":
            return self.player_2_deck
        return None

    def get_loser_deck(self) -> Optional[Deck]:

        if self.winner == "player_1":
            return self.player_2_deck
        elif self.winner == "player_2":
            return self.player_1_deck
        return None

    def to_dict(self) -> dict:

        return {
            "battle_id": self.battle_id,
            "player_1": {
                "deck": self.player_1_deck.to_dict() if self.player_1_deck else None,
                "crowns": self.player_1_crowns,
                "trophies": self.player_1_trophies,
            },
            "player_2": {
                "deck": self.player_2_deck.to_dict() if self.player_2_deck else None,
                "crowns": self.player_2_crowns,
                "trophies": self.player_2_trophies,
            },
            "result": {
                "winner": self.winner,
                "is_draw": self.is_draw,
                "crown_difference": self.crown_difference,
                "is_dominant_win": self.is_dominant_win,
            },
            "stats": {
                "duration_seconds": self.duration_sec,
                "duration_minutes": self.duration_minutes,
                "trophy_difference": self.trophy_difference,
                "match_type": self.match_type,
                "battle_intensity": self.battle_intensity,
            },
            "game_mode": self.game_mode,
        }





    def __str__(self) -> str:

        result_emoji = "🤝" if self.is_draw else "🏆"
        return (
            f"{result_emoji} Battle
            f"P1({self.player_1_crowns}) vs P2({self.player_2_crowns}) | "
            f"Winner: {self.winner.upper()} | Mode: {self.game_mode}"
        )

    def __repr__(self) -> str:

        return (
            f"Battle(id={self.battle_id}, winner='{self.winner}', "
            f"crowns={self.player_1_crowns}-{self.player_2_crowns})"
        )