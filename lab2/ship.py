from __future__ import annotations
from typing import List, Dict, Optional
from lab2.specs import ShipSpecs
from lab2.containers import Container, HeavyContainer, RefrigeratedContainer, LiquidContainer
from lab2.port import Port

CONSUMPTION_SCALE = 1.0 / 1000.0

class Ship:

    def __init__(self, ID: int, initial_port: Optional[Port], specs: ShipSpecs, fuel: float = 0.0):
       
        self.ID = int(ID)  # Ідентифікатор корабля
        self.fuel = float(fuel)  # Залишок палива
        self.currentPort: Optional[Port] = initial_port  # Поточний порт (None якщо корабель в морі)
        if initial_port is not None:
            initial_port.incomingShip(self)  # Додаємо корабель до порту
        self.specs = specs # Специфікації корабля (макс. вага, кількість контейнерів, витрата палива)
        self._containers: List[Container] = []  # Список контейнерів на кораблі

    def _counts(self):
        """
        Повертає словник з поточними кількостями контейнерів:
        загальна, важкі, холодильні, рідкі, а також сумарна вага.
        Використовується для перевірки перед завантаженням нового контейнера.
        """
        total = len(self._containers)
        heavy = sum(1 for c in self._containers if isinstance(c, HeavyContainer))
        refrigerated = sum(1 for c in self._containers if isinstance(c, RefrigeratedContainer))
        liquid = sum(1 for c in self._containers if isinstance(c, LiquidContainer))
        weight_sum = sum(c.weight for c in self._containers)
        return {
            "total": total,
            "heavy": heavy,
            "refrigerated": refrigerated,
            "liquid": liquid,
            "weight_sum": weight_sum
        }

    def load(self, cont: Container) -> bool:
        if self.currentPort is None:
            return False

        if cont not in self.currentPort.containers:
            return False

        counts = self._counts()

    # Перевірка сумарної ваги
        if counts["weight_sum"] + cont.weight > self.specs.totalWeightCapacity:
            return False

    # Перевірка загальної кількості контейнерів
        if self.specs.maxNumberOfAllContainers != 0 and counts["total"] + 1 > self.specs.maxNumberOfAllContainers:
            return False

    # Перевірка лімітів по типу контейнера
        if isinstance(cont, RefrigeratedContainer):
            if self.specs.maxNumberOfRefrigeratedContainers != 0 and counts["refrigerated"] + 1 > self.specs.maxNumberOfRefrigeratedContainers:
                return False
        elif isinstance(cont, LiquidContainer):
            if self.specs.maxNumberOfLiquidContainers != 0 and counts["liquid"] + 1 > self.specs.maxNumberOfLiquidContainers:
                return False
        elif isinstance(cont, HeavyContainer):
            if self.specs.maxNumberOfHeavyContainers != 0 and counts["heavy"] + 1 > self.specs.maxNumberOfHeavyContainers:
                return False

    # Всі перевірки пройдено – переміщаємо контейнер з порту на корабель
        self.currentPort.containers.remove(cont)
        self._containers.append(cont)
        return True



    def unLoad(self, cont: Container) -> bool:
        """
        Розвантажує контейнер у поточний порт.
        """
        if cont not in self._containers:
            return False
        if self.currentPort is None:
            return False
        self._containers.remove(cont)
        self.currentPort.containers.append(cont)
        return True

    def reFuel(self, amount: float) -> None:
        """
        Додає пальне до корабля. Не можна заправляти негативним значенням.
        """
        if amount < 0:
            raise ValueError("Негативне пальне")
        self.fuel += amount

    def _containers_consumption_per_km(self) -> float:
        """
        Обчислює сумарний внесок всіх контейнерів у витрату палива на 1 км.
        """
        return sum(c.consumption() for c in self._containers)

    def sailTo(self, destination_port):
        # Обчислюємо відстань до нового порту
        distance = self.currentPort.getDistance(destination_port)

        # Витрата палива = дистанція * коефіцієнт витрати * CONSUMPTION_SCALE
        required_fuel = distance * self.specs.fuelConsumptionPerKM * CONSUMPTION_SCALE

        # Перевірка пального
        if self.fuel < required_fuel:
            return False

        # Використовуємо паливо
        self.fuel -= required_fuel

        # Видаляємо корабель з поточного порту
        self.currentPort.outgoingShip(self)

        # Переносимо всі контейнери у новий порт
        for c in list(self._containers):  # тут треба self._containers
            destination_port.containers.append(c)
            self._containers.remove(c)

        # Додаємо корабель у новий порт
        self.currentPort = destination_port
        destination_port.incomingShip(self)

        return True




        # Повертає словник із списками ID контейнерів на кораблі за типами.
    def containers_by_type(self) -> Dict[str, list]:
        types = {
            "basic_container": [],
            "heavy_container": [],
            "refrigerated_container": [],
            "liquid_container": []
        }
        for c in self._containers:
            types_key = None
            if type(c).__name__ == "BasicContainer":
                types_key = "basic_container"
            elif type(c).__name__ == "RefrigeratedContainer":
                types_key = "refrigerated_container"
            elif type(c).__name__ == "LiquidContainer":
                types_key = "liquid_container"
            elif type(c).__name__ == "HeavyContainer":
                types_key = "heavy_container"
            if types_key:
                types[types_key].append(c.ID)
        for k in types:
            types[k].sort()
        return types

    def __repr__(self) -> str:
        return f"Ship(ID={self.ID}, fuel={self.fuel:.2f}, port={self.currentPort.ID if self.currentPort else None})"
