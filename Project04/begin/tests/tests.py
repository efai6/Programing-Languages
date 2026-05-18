import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Position import Position
from World import World
from Organisms.Lynx import Lynx
from Organisms.Antelope import Antelope
from Organisms.Sheep import Sheep
from ActionEnum import ActionEnum

try:
    from Main import getConcreteOrganisms
    from Organisms.Organism import Organism
except ImportError:
    pass

class TestSimulationFeatures(unittest.TestCase):
    def setUp(self):
        self.world = World(10, 10)

    # LYNX TESTS

    def test_lynx_initialization(self):
        pos = Position(xPosition=0, yPosition=0)
        lynx = Lynx(position=pos, world=self.world)
        self.assertEqual(lynx.power, 6, "Lynx power should be 6")
        self.assertEqual(lynx.initiative, 5, "Lynx initiative should be 5")
        self.assertEqual(lynx.liveLength, 18, "Lynx live length should be 18")
        self.assertEqual(lynx.sign, 'R', "Lynx sign should be 'R'")

    # ANTELOPE TESTS

    def test_antelope_initialization(self):
        pos = Position(xPosition=0, yPosition=0)
        antelope = Antelope(position=pos, world=self.world)
        self.assertEqual(antelope.power, 4, "Antelope power should be 4")
        self.assertEqual(antelope.initiative, 3, "Antelope initiative should be 3")
        self.assertEqual(antelope.liveLength, 11, "Antelope live length should be 11")
        self.assertEqual(antelope.sign, 'A', "Antelope sign should be 'A'")

    def test_antelope_sense_predator(self):
        # Check if Antelope correctly senses a Lynx nearby
        antelope_pos = Position(xPosition=5, yPosition=5)
        lynx_pos = Position(xPosition=5, yPosition=4) 
        
        antelope = Antelope(position=antelope_pos, world=self.world)
        lynx = Lynx(position=lynx_pos, world=self.world)
        
        self.world.addOrganism(antelope)
        self.world.addOrganism(lynx)

        predator_pos = antelope.senseOfPredator(antelope.position)
        self.assertIsNotNone(predator_pos, "Antelope should have sensed the predator")
        self.assertEqual(predator_pos.x, 5)
        self.assertEqual(predator_pos.y, 4)

    def test_antelope_escape_move(self):
        # Check escape logic
        antelope_pos = Position(xPosition=5, yPosition=5)
        lynx_pos = Position(xPosition=5, yPosition=4) 
        
        antelope = Antelope(position=antelope_pos, world=self.world)
        lynx = Lynx(position=lynx_pos, world=self.world)
        
        self.world.addOrganism(antelope)
        self.world.addOrganism(lynx)

        actions = antelope.move()
        self.assertTrue(len(actions) > 0, "Antelope should return an action")
        
        action = actions[0]
        self.assertEqual(action.action, ActionEnum.A_MOVE)
        
        # Expected position: vector to predator (0, -1). 
        # Antelope multiplies by -2 -> (0, 2).
        # Current position (5, 5) + (0, 2) = (5, 7)
        self.assertEqual(action.position.x, 5)
        self.assertEqual(action.position.y, 7, "Antelope should jump 2 cells down")

    # PLAGUE TESTS
   
    def test_plague_activation(self):
        self.world.Plague()
        self.assertEqual(self.world.plagueCounter, 2, "Plague should last exactly 2 turns")

    def test_plague_effect_on_life(self):
        pos = Position(xPosition=1, yPosition=1)
        sheep = Sheep(position=pos, world=self.world)
        
        # Set specific life length for test accuracy
        sheep.liveLength = 11 
        self.world.addOrganism(sheep)
        
        self.world.Plague() # Activate the plague
        
        # Make a game turn
        self.world.makeTurn()
        
        # World.py logic: 
        # 1. Life decreases by 1 (aging) -> 11 - 1 = 10
        # 2. Plague halves the remaining life -> 10 // 2 = 5
        self.assertEqual(sheep.liveLength, 5, "Sheep's life after one turn during plague should be 5")
        self.assertEqual(self.world.plagueCounter, 1, "Plague counter should have decreased by 1")

    # SPAWN ORGANISMS (MENU) TESTS

    def test_spawning_validation(self):
        # Testing World.py functions used in Main.py for spawn validation
        pos_valid = Position(xPosition=5, yPosition=5)
        pos_invalid = Position(xPosition=15, yPosition=15) # Out of bounds
        
        # 1. Check board boundaries
        self.assertTrue(self.world.positionOnBoard(pos_valid))
        self.assertFalse(self.world.positionOnBoard(pos_invalid))
        
        # 2. Check cell occupancy
        sheep = Sheep(position=pos_valid, world=self.world)
        self.world.addOrganism(sheep)
        
        # Cell (5, 5) is now occupied
        occupying_org = self.world.getOrganismFromPosition(pos_valid)
        self.assertIsNotNone(occupying_org, "There should be an organism at this position")
        self.assertEqual(occupying_org.__class__.__name__, "Sheep")
        
        # Cell (4, 4) is free
        free_pos = Position(xPosition=4, yPosition=4)
        self.assertIsNone(self.world.getOrganismFromPosition(free_pos), "This position should be free")

    def test_get_concrete_organisms(self):
        # If the function was imported from Main.py
        if 'getConcreteOrganisms' in globals() and 'Organism' in globals():
            classes = getConcreteOrganisms(Organism)
            class_names = [cls.__name__ for cls in classes]
            
            # The list should contain final animals, but not base classes
            self.assertIn("Lynx", class_names)
            self.assertIn("Antelope", class_names)
            self.assertIn("Sheep", class_names)
            self.assertNotIn("Animal", class_names, "Base class Animal should not be in the list")
            self.assertNotIn("Organism", class_names, "Base class Organism should not be in the list")

if __name__ == '__main__':
    unittest.main()
