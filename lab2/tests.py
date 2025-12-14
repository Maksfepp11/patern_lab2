import unittest
from lab2.containers import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer, CONSUMPTION_SCALE
from lab2.specs import ShipSpecs
from lab2.main import Simulation

class SimpleTests(unittest.TestCase):
    # Тестуємо правильність розрахунку споживання палива контейнерами
    def test_container_consumptions(self):
        b = BasicContainer(0, 1000)
        h = HeavyContainer(1, 1000)
        r = RefrigeratedContainer(2, 1000)
        l = LiquidContainer(3, 1000)
        # Перевіряємо, що формула weight * RATE * CONSUMPTION_SCALE працює правильно
        self.assertAlmostEqual(b.consumption(), 1000 * 2.5 * CONSUMPTION_SCALE)
        self.assertAlmostEqual(h.consumption(), 1000 * 3.0 * CONSUMPTION_SCALE)
        self.assertAlmostEqual(r.consumption(), 1000 * 5.0 * CONSUMPTION_SCALE)
        self.assertAlmostEqual(l.consumption(), 1000 * 4.0 * CONSUMPTION_SCALE)

    # Тестуємо завантаження, розвантаження контейнерів і плавання корабля між портами
    def test_load_unload_and_sail(self):
        sim = Simulation()
        # Створюємо два порти
        sim.create_port(0, 0.0, 0.0)
        sim.create_port(1, 0.1, 0.1)
        # Створюємо контейнер і кладемо його в порт 0
        cid = sim.create_container(1000)
        sim.place_container_in_port(cid, 0)
        # Створюємо корабель з характеристиками
        specs = ShipSpecs(10000, 10, 10, 10, 10, 0.1)
        sim.create_ship(0, 0, specs, fuel=1000.0)
        # Завантажуємо контейнер на корабель
        self.assertTrue(sim.load(0, cid))
        # Перевіряємо, що корабель може поплисти в порт 1
        ok = sim.sail(0, 1)
        self.assertTrue(ok)
        # Розвантажуємо контейнер у порті 1
        self.assertTrue(sim.unload(0, cid))
        # Перевіряємо, що контейнер тепер знаходиться в порті 1
        self.assertIn(sim.containers[cid], sim.ports[1].containers)

if __name__ == "__main__":
    unittest.main()
