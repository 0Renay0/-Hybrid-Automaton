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
        
    def test_set_initial_state_success(self):
        automaton = create_automate()
        add_discrete_state(automaton,"Q1")
        define_continuous_space(automaton,["x1"])
        set_initial_state(automaton,"Q1",[0.0])
        self.assertEqual(automaton["q0"],"Q1")
        self.assertEqual(automaton["x0"],[0.0])
        print("Test set initial state OK")
        
    def test_set_initial_state_invalid_state(self):
        automaton = create_automate()
        # add_discrete_state(automaton,"Q1")
        define_continuous_space(automaton,["x1"])
        with self.assertRaises(ValueError):
            set_initial_state(automaton,"UNKNOWN",[0.0])
        print("Test set invalid initial discreate state OK")
        
    def test_set_initial_state_invalid_x0(self):
        automaton = create_automate()
        add_discrete_state(automaton,"Q1")
        define_continuous_space(automaton,["x1","x2"])
        with self.assertRaises(ValueError):
            set_initial_state(automaton,"Q1",[0.0]) # len(x0) = 2 not 1 so Error
        print("Test set invalid initial continuous state OK")
        
    def test_set_event_valid(self):
        automaton = create_automate()
        add_discrete_state(automaton,"Q1")
        add_discrete_state(automaton,"Q2")
        set_event(automaton,"Q1","Q2","alpha")
        self.assertIn("Event",automaton)
        self.assertIn("Q1",automaton["Event"])
        self.assertIn("Q2",automaton["Event"]["Q1"])
        # self.assertIn("alpha",automaton)
        self.assertEqual(automaton["Event"]["Q1"]["Q2"],"alpha")
        print("Test set valid event OK")
        
    def test_set_event_invalid_state(self):
        automaton = create_automate()
        add_discrete_state(automaton,"Q1")
        with self.assertRaises(ValueError):
            set_event(automaton,"Q1","Q2","event_invalid")
        print("Test set invalid event OK")