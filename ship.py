# ship.py
from __future__ import annotations
from typing import List, Dict, Optional
from specs import ShipSpecs
from containers import Container, HeavyContainer, RefrigeratedContainer, LiquidContainer
from port import Port

class Ship:
    def __init__(self, ID: int, initial_port: Optional[Port], specs: ShipSpecs, fuel: float = 0.0):
        self.ID = int(ID)
        self.fuel = float(fuel)
        self.currentPort: Optional[Port] = initial_port
        if initial_port is not None:
            initial_port.incomingShip(self)
        self.specs = specs
        self._containers: List[Container] = []

    def _counts(self):
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
        if counts["weight_sum"] + cont.weight > self.specs.totalWeightCapacity:
            return False
        if self.specs.maxNumberOfAllContainers != 0 and counts["total"] + 1 > self.specs.maxNumberOfAllContainers:
            return False
        if isinstance(cont, HeavyContainer):
            if self.specs.maxNumberOfHeavyContainers != 0 and counts["heavy"] + 1 > self.specs.maxNumberOfHeavyContainers:
                return False
            if isinstance(cont, RefrigeratedContainer):
                if self.specs.maxNumberOfRefrigeratedContainers != 0 and counts["refrigerated"] + 1 > self.specs.maxNumberOfRefrigeratedContainers:
                    return False
            if isinstance(cont, LiquidContainer):
                if self.specs.maxNumberOfLiquidContainers != 0 and counts["liquid"] + 1 > self.specs.maxNumberOfLiquidContainers:
                    return False
        # перевести контейнер з порту на корабель
        self.currentPort.containers.remove(cont)
        self._containers.append(cont)
        return True

    def unLoad(self, cont: Container) -> bool:
        if cont not in self._containers:
            return False
        if self.currentPort is None:
            return False
        self._containers.remove(cont)
        self.currentPort.containers.append(cont)
        return True

    def reFuel(self, amount: float) -> None:
        if amount < 0:
            raise ValueError("Негативне пальне")
        self.fuel += amount

    def _containers_consumption_per_km(self) -> float:
        return sum(c.consumption() for c in self._containers)

    def sailTo(self, dest: Port) -> bool:
        if self.currentPort is None:
            return False
        distance = self.currentPort.getDistance(dest)
        per_km = self.specs.fuelConsumptionPerKM + self._containers_consumption_per_km()
        fuel_needed = distance * per_km
        if self.fuel + 1e-9 >= fuel_needed:
            self.fuel -= fuel_needed
            self.currentPort.outgoingShip(self)
            prev = self.currentPort
            self.currentPort = dest
            dest.incomingShip(self)
            return True
        else:
            return False

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
