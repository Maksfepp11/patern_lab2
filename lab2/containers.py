from __future__ import annotations
from abc import ABC, abstractmethod

CONSUMPTION_SCALE = 1.0 / 1000.0

# Абстрактний клас контейнера – базовий для всіх типів контейнерів
class Container(ABC):
    def __init__(self, ID: int, weight: int) -> None:
        self.ID = ID               # унікальний ідентифікатор контейнера
        self.weight = int(weight)  # вага контейнера 

    @abstractmethod
    def consumption(self) -> float:
        """Метод для обчислення внеску контейнера у споживання палива на 1 км."""
        pass

    def type_name(self) -> str:
        """Повертає назву класу контейнера як рядок (наприклад, 'BasicContainer')"""
        return self.__class__.__name__

    def __repr__(self) -> str:
        """Друк контейнера"""
        return f"{self.type_name()}(ID={self.ID}, weight={self.weight})"

# Легкий контейнер (вага <= 3000 кг)
class BasicContainer(Container):
    RATE = 2.50  # коефіцієнт витрати палива на одиницю ваги

    def consumption(self) -> float:
        # Витрати палива = вага * RATE * масштаб
        return self.weight * BasicContainer.RATE * CONSUMPTION_SCALE

# Важкий контейнер
class HeavyContainer(Container):
    RATE = 3.00  # більший коефіцієнт витрати палива, ніж у BasicContainer

    def consumption(self) -> float:
        return self.weight * HeavyContainer.RATE * CONSUMPTION_SCALE

# Охолоджений контейнер – спеціальний тип важкого контейнера
class RefrigeratedContainer(HeavyContainer):
    RATE = 5.00  # ще більші витрати палива через холодильне обладнання

    def consumption(self) -> float:
        return self.weight * RefrigeratedContainer.RATE * CONSUMPTION_SCALE

# Рідинний контейнер – спец тип важкого контейнера
class LiquidContainer(HeavyContainer):
    RATE = 4.00  

    def consumption(self) -> float:
        return self.weight * LiquidContainer.RATE * CONSUMPTION_SCALE
