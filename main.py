# simulation.py
from containers import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer
from specs import ShipSpecs
from port import Port
from ship import Ship

# Простий менеджер симуляції (тримає порти/кораблі/контейнери)
class Simulation:
    def __init__(self):
        self.ports = {}
        self.ships = {}
        self.containers = {}
        self._next_container_id = 0

    def _next_id(self):
        nid = self._next_container_id
        self._next_container_id += 1
        return nid

    def create_port(self, ID, lat, lon):
        if ID in self.ports:
            raise ValueError("Port exists")
        self.ports[ID] = Port(ID, lat, lon)

    def create_ship(self, ID, port_id, specs: ShipSpecs, fuel=0.0):
        if ID in self.ships:
            raise ValueError("Ship exists")
        port = self.ports.get(port_id)
        if port is None:
            raise ValueError("Port not found")
        ship = Ship(ID, port, specs, fuel=fuel)
        self.ships[ID] = ship

    def create_container(self, weight, kind=None):
        cid = self._next_id()
        if kind == "R":
            cont = RefrigeratedContainer(cid, weight)
        elif kind == "L":
            cont = LiquidContainer(cid, weight)
        else:
            cont = BasicContainer(cid, weight) if weight <= 3000 else HeavyContainer(cid, weight)
        self.containers[cid] = cont
        return cid

    def place_container_in_port(self, cid, port_id):
        cont = self.containers.get(cid)
        port = self.ports.get(port_id)
        if cont is None or port is None:
            raise ValueError("Container or port not found")
        port.containers.append(cont)

    def load(self, ship_id, container_id):
        ship = self.ships.get(ship_id)
        cont = self.containers.get(container_id)
        if ship is None or cont is None:
            return False
        return ship.load(cont)

    def unload(self, ship_id, container_id):
        ship = self.ships.get(ship_id)
        cont = self.containers.get(container_id)
        if ship is None or cont is None:
            return False
        return ship.unLoad(cont)

    def refuel(self, ship_id, amount):
        ship = self.ships.get(ship_id)
        if ship is None:
            return False
        ship.reFuel(amount)
        return True

    def sail(self, ship_id, dest_port_id):
        ship = self.ships.get(ship_id)
        dest = self.ports.get(dest_port_id)
        if ship is None or dest is None:
            return False
        return ship.sailTo(dest)

    # Print state instead of JSON
    def print_state(self):
        for pid in sorted(self.ports.keys()):
            p = self.ports[pid]
            print(f"Port {p.ID}: lat={p.latitude:.2f}, lon={p.longitude:.2f}")
            types = p.containers_by_type()
            print("  Containers at port:")
            print(f"    basic: {types['basic_container']}")
            print(f"    heavy: {types['heavy_container']}")
            print(f"    refrigerated: {types['refrigerated_container']}")
            print(f"    liquid: {types['liquid_container']}")
            if p.current:
                print("  Ships in port:")
                for s in sorted(p.current, key=lambda x: x.ID):
                    print(f"    Ship {s.ID}: fuel_left={s.fuel:.2f}")
                    sc = s.containers_by_type()
                    print(f"      basic: {sc['basic_container']}")
                    print(f"      heavy: {sc['heavy_container']}")
                    print(f"      refrigerated: {sc['refrigerated_container']}")
                    print(f"      liquid: {sc['liquid_container']}")
            else:
                print("  (no ships)")

if __name__ == "__main__":
    # Простий приклад сценарію (тепер усе через прінти)
    sim = Simulation()

    # Створимо 2 порти
    sim.create_port(0, 50.45, 30.52)   # Київ (прибл.)
    sim.create_port(1, 46.48, 30.73)   # Одеса (прибл.)

    # Створимо контейнери
    c0 = sim.create_container(2000)     # basic
    c1 = sim.create_container(5000)     # heavy
    c2 = sim.create_container(1000, kind="R")  # refrigerated forced
    c3 = sim.create_container(4000, kind="L")  # liquid forced

    # Покладемо контейнери в порт 0
    sim.place_container_in_port(c0, 0)
    sim.place_container_in_port(c1, 0)
    sim.place_container_in_port(c2, 0)
    sim.place_container_in_port(c3, 0)

    # Створимо корабель у порту 0 з простими характеристиками
    specs = ShipSpecs(
        totalWeightCapacity=20000,
        maxNumberOfAllContainers=10,
        maxNumberOfHeavyContainers=5,
        maxNumberOfRefrigeratedContainers=2,
        maxNumberOfLiquidContainers=2,
        fuelConsumptionPerKM=0.5
    )
    sim.create_ship(0, 0, specs, fuel=1000.0)

    # Завантажимо два контейнери
    print("Load c0 ->", sim.load(0, c0))  # очікуємо True
    print("Load c1 ->", sim.load(0, c1))  # очікуємо True
    # Спроба завантажити контейнер, якого немає -> False
    print("Load non-existent ->", sim.load(0, 999))

    # Дозаправка
    sim.refuel(0, 200.0)

    # Переходимо в порт 1 (якщо вистачить палива)
    ok = sim.sail(0, 1)
    print("Sail to port 1 successful?", ok)

    # Розвантажити один контейнер
    if ok:
        print("Unload c1 ->", sim.unload(0, c1))

    # Друк стану (вивід через print замість JSON)
    print("\n--- Final state ---")
    sim.print_state()
