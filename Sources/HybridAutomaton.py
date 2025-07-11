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