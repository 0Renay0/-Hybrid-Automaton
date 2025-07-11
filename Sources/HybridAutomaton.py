import json
import sys
import os
from graphviz import Digraph
import matplotlib.pyplot as plt

"""
Initializes the structure of a hybrid automaton.
Returns:
    dict: Empty initialized automaton structure.
"""

def create_automate():
    return {
        "Q": [],        # Discrete states
        "X": [],        # Continuous variables
        "E": {},        # Event set
        "U": [],        # Input space
        "T": [],        # Transitions
        "q0": None,     # Initial discrete state
        "x0": [],       # Initial continuous state
        "q": None,      # Current discrete state
        "x": [],        # Current continuous state
        "t": 0.0,       # Simulation time
        "flow": {},     # Flow functions for each state
        "Inv": {},      # Invariant functions for each state
        "Guard": {},    # Guard conditions for transitions
        "Jump": {}      # Reset (jump) functions
    }
    
# --- Component definitions ---

def add_discrete_state(automate, q_name): 
    """Add a discrete state to the automaton"""
    if q_name not in automate["Q"]:
        automate["Q"].append(q_name)
        
def define_continuous_space(automate, variable_names):
    """Defines the names of the continuous variables"""
    automate["X"] = variable_names[:]
    
def define_input_space(automate, inputs):
    """Defines the input space U (set of admissible inputs)"""
    automate["U"] = inputs[:]
    
def define_event_set(automate, events): 
    """Defines the set of observable events"""
    automate["E"] = {e: False for e in events}
    
def set_initial_state(automate, q0, x0): 
    """Sets the initial discrete and continuous states"""
    if q0 not in automate["Q"]:
        raise ValueError(f"The initial state '{q0}' does not exist.")
    if len(x0) != len(automate["X"]):
        raise ValueError("x0 must have the same dimension as X.")
    automate["q0"] = q0
    automate["x0"] = x0[:]
    automate["q"] = q0
    automate["x"] = x0[:]
    
def set_flow(automate, q_name, dynamique):
    """Sets the flow function for a given state q in Q"""
    if q_name not in automate["Q"]:
        raise ValueError(f"The discreate state '{q_name}' does not exist.")
    automate["flow"][q_name] = dynamique
    
    