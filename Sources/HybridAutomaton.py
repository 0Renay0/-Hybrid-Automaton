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
    
def set_invariant(automate, q_name, invariant_func):
    """Sets the invariant condition for a given state q in Q"""
    if q_name not in automate["Q"]:
        raise ValueError(f"The discreate state '{q_name}' does not exist.")
    automate["Inv"][q_name] = invariant_func
    
def set_guard(automate, q_from, q_to, guard_func):
    """Sets the guard function for a transition from q_from to q_to"""
    if q_from not in automate["Q"] or q_to not in automate["Q"]:
        raise ValueError(f"The couple ({q_from}, {q_to}) is not valid in Q × Q.")
    if q_from not in automate["Guard"]:
        automate["Guard"][q_from] = {}
    automate["Guard"][q_from][q_to] = guard_func
    
    
def set_jump(automate, q_from, q_to, reset_func):
    """Sets the reset (jump) function for a transition from q_from to q_to"""
    if q_from not in automate["Q"] or q_to not in automate["Q"]:
        raise ValueError(f"The couple ({q_from}, {q_to}) is not valid in Q × Q.")
    if q_from not in automate["Jump"]:
        automate["Jump"][q_from] = {}
    automate["Jump"][q_from][q_to] = reset_func
    
def set_event(automate, q_from, q_to, event_name):
    """
    Sets the event associated with a transition from q_from to q_to.
    """
    if q_from not in automate["Q"] or q_to not in automate["Q"]:
        raise ValueError(f"The Couple ({q_from}, {q_to}) is not valid in Q × Q.")
    if "Event" not in automate:
        automate["Event"] = {}  # Creation of the Event dictionary if it does not exist
    if q_from not in automate["Event"]:
        automate["Event"][q_from] = {}
    automate["Event"][q_from][q_to] = event_name
    
def add_transition(automate, q_from, q_to, event=None, guard=None, reset=None): 
    """
    Adds a transition to the automaton with optional guard and reset.
    Parameters:
        q_from (str): Origin state.
        q_to (str): Destination state.
        event (str): Event label.
        guard (str): Guard function name.
        reset (str): Reset function name.
    """
    automate["T"].append({
        "q_from": q_from,
        "q_to": q_to,
        "event": event,
        "guard": guard,
        "reset": reset
    })
    
# --- Export utility ---

def export_automate_to_txt_with_functions(automate, filename, functions_dict):
    """
    Exports the automate and associated function source codes to a JSON-formatted .txt file.
    Parameters:
        automate (dict): The automaton structure.
        filename (str): Output file name.
        functions_dict (dict): Dictionary mapping function names to their source code.
    """
    def get_func_name(f):
        return f.__name__ if callable(f) else None

    data = {
        "Q": automate["Q"],
        "X": automate["X"],
        "U": automate["U"],
        "E": automate["E"],
        "q0": automate["q0"],
        "x0": automate["x0"],
        "flow": {q: get_func_name(automate["flow"].get(q)) for q in automate["Q"]},
        "Inv": {q: get_func_name(automate["Inv"].get(q)) for q in automate["Q"]},
        "Guard": {
            q1: {q2: get_func_name(automate["Guard"][q1][q2])
                 for q2 in automate["Guard"][q1]}
            for q1 in automate["Guard"]
        },
        "Jump": {
            q1: {q2: get_func_name(automate["Jump"][q1][q2])
                 for q2 in automate["Jump"][q1]}
            for q1 in automate["Jump"]
        },
        "T": automate["T"],
        "functions": functions_dict
    }
    # Path to the directory Convert_HA_to_HtPN for conversion
    full_path = os.path.join("../Convert_HA_to_HtPN", filename)
    # Write the data to a JSON file
    with open(full_path, "w") as f:
        f.write(json.dumps(data, indent=4))
        


# --- Generation of HtPN configuration ---

def generate_config_from_automate(json_path="automate_machine.txt", output_path="Convert_HA_to_HtPN/ConfigModel.py", h_size=1):
    """
    Generates an initial configuration file (ConfigModel.py) for the HtPN model.
    Defines the initial marking, initial continuous state, timer, and command inputs.
    
    Parameters:
    - json_path: Path to the JSON file of the hybrid automaton.
    - output_path: Full path to the output file to be generated.
    - h_size: Size of the H0 vector.
    """
    with open(json_path, "r") as f:
        data = json.load(f)

    q0 = data.get("q0", "UNKNOWN")
    x0 = data.get("x0", [])
    uc0 = data.get("UC0", [0.0])

    code = f'''"""
Auto-generated configuration for HtPN model
"""

import numpy as np

M0 = ["{q0}"]
T0 = 0
X0 = {x0}
H0 = {[0] * h_size}
UC0 = {uc0}
'''

    # Création du dossier si nécessaire
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        f.write(code)

    print(f"Configuration written to '{output_path}'")