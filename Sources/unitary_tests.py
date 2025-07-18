import unittest
from HybridAutomaton import *
import json
import tempfile
import os

class TestHybridAutomaton(unittest.TestCase):
    
    def test_create_automate(self):
        """
        Initializes the structure of a hybrid automaton.
        Returns:
            dict: Empty initialized automaton structure.
        """
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