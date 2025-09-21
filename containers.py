# containers.py
from __future__ import annotations
from abc import ABC, abstractmethod

# Конфіг для масштабу споживання (можеш змінити)
CONSUMPTION_SCALE = 1.0 / 1000.0

class Container(ABC):
    def __init__(self, ID: int, weight: int) -> None:
        self.ID = ID
        self.weight = int(weight)

    @abstractmethod
    def consumption(self) -> float:
        """Повертає внесок контейнера у споживання палива на 1 км."""
        pass

    def type_name(self) -> str:
        return self.__class__.__name__

    def __repr__(self) -> str:
        return f"{self.type_name()}(ID={self.ID}, weight={self.weight})"

class BasicContainer(Container):
    RATE = 2.50

    def consumption(self) -> float:
        return self.weight * BasicContainer.RATE * CONSUMPTION_SCALE

class HeavyContainer(Container):
    RATE = 3.00

    def consumption(self) -> float:
        return self.weight * HeavyContainer.RATE * CONSUMPTION_SCALE

class RefrigeratedContainer(HeavyContainer):
    RATE = 5.00

    def consumption(self) -> float:
        return self.weight * RefrigeratedContainer.RATE * CONSUMPTION_SCALE

class LiquidContainer(HeavyContainer):
    RATE = 4.00

    def consumption(self) -> float:
        return self.weight * LiquidContainer.RATE * CONSUMPTION_SCALE
