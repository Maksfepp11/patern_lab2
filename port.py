# port.py
from __future__ import annotations
import math
from typing import List, Dict
from containers import Container, BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer

class Port:
    def __init__(self, ID: int, latitude: float, longitude: float):
        self.ID = int(ID)
        self.latitude = float(latitude)
        self.longitude = float(longitude)
        self.containers: List[Container] = []
        self.history = []   # список кораблів, що відвідували
        self.current = []   # кораблі, що зараз у порту

    def incomingShip(self, ship) -> None:
        if ship not in self.current:
            self.current.append(ship)
        if ship not in self.history:
            self.history.append(ship)

    def outgoingShip(self, ship) -> None:
        if ship in self.current:
            self.current.remove(ship)
        if ship not in self.history:
            self.history.append(ship)

    def getDistance(self, other: "Port") -> float:
        # Haversine formula -> km
        R = 6371.0
        lat1 = math.radians(self.latitude)
        lon1 = math.radians(self.longitude)
        lat2 = math.radians(other.latitude)
        lon2 = math.radians(other.longitude)
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        return R * c

    def containers_by_type(self) -> Dict[str, list]:
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
