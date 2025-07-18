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
        
        
    def test_add_transition_basic(self):
        automaton = create_automate()
        add_discrete_state(automaton,"Q1")
        add_discrete_state(automaton,"Q2")
        add_transition(automaton,"Q1","Q2")
        self.assertEqual(len(automaton["T"]),1)
        t = automaton["T"][0]
        self.assertEqual(t["q_from"],"Q1")
        self.assertEqual(t["q_to"],"Q2")
        self.assertIsNone(t["event"])
        self.assertIsNone(t["guard"])
        self.assertIsNone(t["reset"])
        print("Test add basic transition OK")
        
        
    def test_add_transition_completed(self):
        automaton = create_automate()
        add_discrete_state(automaton,"Q1")
        add_discrete_state(automaton,"Q2")
        add_transition(automaton,"Q1","Q2",event="alpha",guard="G_func",reset="R_func")
        t = automaton["T"][0]
        self.assertEqual(t["q_from"],"Q1")
        self.assertEqual(t["q_to"],"Q2")
        self.assertEqual(t["event"],"alpha")
        self.assertEqual(t["guard"],"G_func")
        self.assertEqual(t["reset"],"R_func")
        print("Test add complete transition OK")
        
    
    def test_set_flow_valid(self):
        automaton = create_automate()
        add_discrete_state(automaton,"Q1")
        
        def flow(x,u,t):
            return [1.0]
        
        set_flow(automaton,"Q1",flow)
        self.assertIn("Q1",automaton["flow"])
        self.assertEqual(automaton["flow"]["Q1"].__name__,"flow")
        print("Test set flow OK")
        
        
    def test_set_flow_invalid(self):
        automaton = create_automate()
        with self.assertRaises(ValueError):
            set_flow(automaton,"Unkown",lambda x,u,t:[0.0])
        print("Test set flow with invalid state OK")
        
    
    def test_set_invariant_valid(self):
        automaton = create_automate()
        add_discrete_state(automaton,"Q1")
        
        def Inv(x):
            return x[0] <= 1.0
        
        set_invariant(automaton,"Q1",Inv)
        self.assertIn("Q1",automaton["Inv"])
        self.assertEqual(automaton["Inv"]["Q1"].__name__,"Inv")
        print("Test set invariant OK")
        
    def test_set_jump_valid(self):
        automaton = create_automate()
        add_discrete_state(automaton,"Q1")
        add_discrete_state(automaton,"Q2")
        
        def jump(x):
            return x[0] >= 75.0
        
        set_jump(automaton,"Q1","Q2",jump)
        self.assertIn("Q1",automaton["Jump"])
        self.assertIn("Q2",automaton["Jump"]["Q1"])
        self.assertEqual(automaton["Jump"]["Q1"]["Q2"].__name__,"jump")
        print("Test set jump OK")
        
    
    def test_set_jump_invalid_state(self):
        automaton = create_automate()
        add_discrete_state(automaton,"Q1")
        with self.assertRaises(ValueError):
            set_jump(automaton,"Q1","Q5", lambda x: x)
        print("Test set jump with invalid state OK")
        
        

class TestExport(unittest.TestCase):
    
    def test_export_automate_to_txt(self):
        # Automaton Creation 
        automaton = create_automate()
        add_discrete_state(automaton,"Q1")
        add_discrete_state(automaton,"Q2")
        define_continuous_space(automaton,["x"])
        set_initial_state(automaton,"Q1",[0.0])
        
        # Dynamic functions
        def flow(x,u,t): return [1.0]
        def inv(x): return x[0] <= 15
        def jump(x): return [0.0]

        set_flow(automaton,"Q1",flow)
        set_invariant(automaton,"Q1",inv)
        set_jump(automaton,"Q1","Q2",jump)
        
        # Dict of functions 
        functions = {
            "flow": "def flow(x,u,t): return [1.0]",
            "inv" : "def inv(x): return x[0] <= 15",
            "jump": "def jump(x): return [0.0]"
        }

        # Creation of temporary file 
        with tempfile.NamedTemporaryFile(delete=False,suffix=".txt") as tmpfile:
            export_automate_to_txt_with_functions(automaton, tmpfile.name, functions)
            
        with open(tmpfile.name, "r") as f:
            data = json.load(f)
            
        # Verification of the contenent of the file
        self.assertIn("Q",data)
        self.assertIn("flow",data)
        self.assertEqual(data["flow"]["Q1"], "flow")
        self.assertEqual(data["Inv"]["Q1"], "inv")
        self.assertEqual(data["Jump"]["Q1"]["Q2"], "jump")
        self.assertIn("functions",data)
        self.assertIn("flow",data["functions"])        
        self.assertIn("inv",data["functions"])
        self.assertIn("jump",data["functions"])
        
        print("Test exportation structure OK")
        
        #Removing file 
        os.remove(tmpfile.name)