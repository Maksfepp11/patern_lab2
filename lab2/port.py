from __future__ import annotations
import math
from typing import List, Dict
from lab2.containers import Container, BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer

class Port:
    def __init__(self, ID: int, latitude: float, longitude: float):
        self.ID = int(ID)                     # Унікальний ідентифікатор порту
        self.latitude = float(latitude)       # Географічна широта
        self.longitude = float(longitude)     # Географічна довгота
        self.containers: List[Container] = [] # Контейнери, що знаходяться у порту
        self.history = []                     # Список кораблів, що коли-небудь відвідували порт
        self.current = []                     # Кораблі, що зараз у порту

    def incomingShip(self, ship) -> None:
        """Додає корабель до поточного списку та історії (якщо його там ще немає)."""
        if ship not in self.current:
            self.current.append(ship)
        if ship not in self.history:
            self.history.append(ship)

    def outgoingShip(self, ship) -> None:
        """Видаляє корабель з поточного списку та додає його в історію (якщо раніше не був там)."""
        if ship in self.current:
            self.current.remove(ship)
        if ship not in self.history:
            self.history.append(ship)

    def getDistance(self, other: "Port") -> float:
        # формула гаверсина
        R = 6371  # радіус Землі в км
        lat1, lon1 = math.radians(self.latitude), math.radians(self.longitude)
        lat2, lon2 = math.radians(other.latitude), math.radians(other.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c

    def containers_by_type(self) -> Dict[str, list]:
        """Повертає словник зі списками ID контейнерів, відсортованих за типом."""
        types = {
            "basic_container": [],
            "heavy_container": [],
            "refrigerated_container": [],
            "liquid_container": []
        }
        for c in self.containers:
            if isinstance(c, BasicContainer):
                types["basic_container"].append(c.ID)
            elif isinstance(c, RefrigeratedContainer):
                types["refrigerated_container"].append(c.ID)
            elif isinstance(c, LiquidContainer):
                types["liquid_container"].append(c.ID)
            elif isinstance(c, HeavyContainer):
                types["heavy_container"].append(c.ID)
        for k in types:
            types[k].sort()
        return types

    def __repr__(self) -> str:
        return f"Port(ID={self.ID}, lat={self.latitude}, lon={self.longitude})"
