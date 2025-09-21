# tests.py
import unittest
from containers import BasicContainer, HeavyContainer, RefrigeratedContainer, LiquidContainer, CONSUMPTION_SCALE
from specs import ShipSpecs
from main import Simulation

class SimpleTests(unittest.TestCase):
    def test_container_consumptions(self):
        b = BasicContainer(0, 1000)
        h = HeavyContainer(1, 1000)
        r = RefrigeratedContainer(2, 1000)
        l = LiquidContainer(3, 1000)
        self.assertAlmostEqual(b.consumption(), 1000 * 2.5 * CONSUMPTION_SCALE)
        self.assertAlmostEqual(h.consumption(), 1000 * 3.0 * CONSUMPTION_SCALE)
        self.assertAlmostEqual(r.consumption(), 1000 * 5.0 * CONSUMPTION_SCALE)
        self.assertAlmostEqual(l.consumption(), 1000 * 4.0 * CONSUMPTION_SCALE)

    def test_load_unload_and_sail(self):
        sim = Simulation()
        sim.create_port(0, 0.0, 0.0)
        sim.create_port(1, 0.1, 0.1)
        cid = sim.create_container(1000)
        sim.place_container_in_port(cid, 0)
        specs = ShipSpecs(10000, 10, 10, 10, 10, 0.1)
        sim.create_ship(0, 0, specs, fuel=1000.0)
        self.assertTrue(sim.load(0, cid))
        # ship has one container now
        ship = sim.ships[0]
        # sail should succeed with plenty of fuel
        ok = sim.sail(0, 1)
        self.assertTrue(ok)
        # after sail, container still on ship; unload in port 1
        self.assertTrue(sim.unload(0, cid))
        # now the port 1 must have container
        self.assertIn(sim.containers[cid], sim.ports[1].containers)

if __name__ == "__main__":
    unittest.main()
