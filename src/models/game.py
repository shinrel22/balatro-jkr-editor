from src.bases.models import BaseModel


class RandomRates(BaseModel):
    joker: float = 20
    tarot: float = 4
    planet: float = 4
    spectral: float = 0
    hand_card: float = 0
    rental: float = 3
    edition: float = 1

