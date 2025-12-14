from dataclasses import dataclass

@dataclass
class ShipSpecs:
    totalWeightCapacity: int                   # Загальна максимальна вага всіх контейнерів на кораблі
    maxNumberOfAllContainers: int             # Максимальна кількість контейнерів будь-якого типу
    maxNumberOfHeavyContainers: int           # Максимальна кількість важких контейнерів (Heavy, Refrigerated, Liquid)
    maxNumberOfRefrigeratedContainers: int    # Максимальна кількість холодильних контейнерів
    maxNumberOfLiquidContainers: int          # Максимальна кількість рідких контейнерів
    fuelConsumptionPerKM: float               # Базова витрата палива корабля на км без урахування контейнерів
