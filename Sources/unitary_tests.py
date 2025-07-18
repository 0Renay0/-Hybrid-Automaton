import unittest
from HybridAutomaton import *
import json
import tempfile
import os

class TestHybridAutomaton(unittest.TestCase):
    
    def test_create_automate(self):
        automaton = create_automate()
        self.assertIsInstance(automaton,dict)
        self.assertEqual(automaton["Q"],[])
        self.assertEqual(automaton["X"],[])
        self.assertEqual(automaton["E"],{})
        self.assertEqual(automaton["U"],[])
        self.assertEqual(automaton["T"],[])
        self.assertEqual(automaton["q0"],None)
        self.assertEqual(automaton["x0"],[])
        self.assertEqual(automaton["flow"],{})
        self.assertEqual(automaton["Inv"],{})
        self.assertEqual(automaton["Guard"],{})
        self.assertEqual(automaton["Jump"],{})
        print("Test creation automaton OK")
        
    def test_add_discreate_state(self):
        automaton = create_automate()
        add_discrete_state(automaton,"IDLE")
        self.assertIn("IDLE", automaton["Q"])
        add_discrete_state(automaton,"IDLE") # No duplicate allowed
        self.assertEqual(len(automaton["Q"]),1)
        print("Test add discreate state OK")
        
    def test_define_continuous_space(self):
        automaton = create_automate()
        define_continuous_space(automaton,["X1","X2"])        
        self.assertEqual(automaton["X"],["X1","X2"])
        print("Test define continuous space OK")
        
    