import sys

sys.path.append("Sources")  # Add the parent path to access modules
from HybridAutomaton import (
    create_automate,
    define_continuous_space,
    add_discrete_state,  # type: ignore
    set_initial_state,
    set_flow,
    set_invariant,
    set_guard,
    set_jump,
    add_transition,
    set_event,
    define_event_set,
    collect_functions,
    export_automate_to_txt_with_functions,
    generate_config_from_automate,
)
from Simulation import simulate, plot_trace  # type: ignore
from VisuelAutomate import visualiser_automate  # type: ignore
import numpy as np


# === Continuous Dynamics ===
def flow_Q1(x, t):
    return [0.0, 0.0]  # No dynamics (system is idle)


def flow_Q2(x, t):
    return [2.5, 1.0]  # Constant evolution of x and tau


def flow_Q3(x, t):
    return [0.0, 0.0]  # No dynamics (machine is down)


# === Invariants ===
def inv_Q1(x):
    return True  # No constraint in state Q1 <=> X = 0


def inv_Q2(x):
    return x[1] < 3.0  # tau must remain less than 3 in Q2


def inv_Q3(x):
    return True  # No constraint in state Q3 <=> X = 0


# === Guard Conditions ===
# Deactivation of machine
def guard_Q2_Q1(x):
    return x[0] >= 10.0


# Timeout occurred
def guard_Q2_Q3(x):
    return x[1] >= 3.0


# === Jumps ===


# No reset
def identity(x):
    return np.array([x[0], x[1]])  # First way to define no reset


def reset_none(x):
    return np.array([x[0], x[1]])  # Second way to define no reset


# Reset both x and tau to 0
def reset_all(x):
    x = np.zeros(2)
    x[0] = 0
    x[1] = 0
    return x


# === Automaton Creation ===
A = create_automate()
define_continuous_space(A, ["x", "tau"])  # Define continuous state variables

# Add discrete states (Q1: IDLE, Q2: BUSY, Q3: DOWN)
for q in ["Q1", "Q2", "Q3"]:
    add_discrete_state(A, q)


define_event_set(A, ["alpha", "beta", "gamma"])  # Define the event set
set_initial_state(A, "Q1", [0.0, 0.0])  # Initial state: Q1 with x=0, tau=0

# Assign flow functions to states
flows = {"Q1": flow_Q1, "Q2": flow_Q2, "Q3": flow_Q3}
for q, f in flows.items():
    set_flow(A, q, f)

# Assign invariants to states
Invs = {"Q1": inv_Q1, "Q2": inv_Q2, "Q3": inv_Q3}
for q, f in Invs.items():
    set_invariant(A, q, f)

# Assign guard functions to transitions
guards = {
    ("Q1", "Q2"): None,
    ("Q2", "Q1"): guard_Q2_Q1,
    ("Q2", "Q3"): guard_Q2_Q3,
    ("Q3", "Q1"): None,
}
for (q1, q2), g in guards.items():
    set_guard(A, q1, q2, g)

# Assign jump (reset) functions
jumps = {
    ("Q1", "Q2"): identity,
    ("Q2", "Q1"): reset_all,
    ("Q2", "Q3"): reset_all,
    ("Q3", "Q1"): identity,
}
for (q1, q2), j in jumps.items():
    set_jump(A, q1, q2, j)

# Assign events to transitions
events = {
    ("Q1", "Q2"): "alpha",  # Activation machine
    ("Q2", "Q1"): "beta",  # Turn off machine
    ("Q2", "Q3"): None,
    ("Q3", "Q1"): "gamma",  # Repair completed
}
for (q1, q2), e in events.items():
    set_event(A, q1, q2, e)

# Declare the transitions with names of guards and resets
for q1, q2 in guards:
    g = guards.get((q1, q2))
    j = jumps.get((q1, q2))
    e = events.get((q1, q2))
    add_transition(
        A,
        q1,
        q2,
        event=e,
        guard=g.__name__ if g else None,
        reset=j.__name__ if j else None,
    )


# === Function Dictionary Generation ===
# Extract source code of all functions used in this automaton
functions = collect_functions(
    *flows.values(), *guards.values(), *jumps.values(), *Invs.values()
)

# Export the automaton and its functions to a text file
export_automate_to_txt_with_functions(A, "automate_machine.txt", functions)

# Visualize the automaton
visualiser_automate(A, filename="automate_machine", functions=functions)

# === Event Scheduling ===
"""
Once an event is activated, it must be deactivated shortly after.
Otherwise, the guard condition depending on it will stay True indefinitely.
This schedule controls when to toggle events.
"""
event_schedule = [
    (1.0, "alpha", True),
    (1.01, "alpha", False),
    (2.0, "beta", True),
    (2.1, "beta", False),
    (5.0, "alpha", True),
    (5.01, "alpha", False),
    (11.0, "gamma", True),
    (11.01, "gamma", False),
]

# === Simulation ===
trace = simulate(A, dt=0.001, t_max=20, event_schedule=event_schedule)
plot_trace(trace, A)
generate_config_from_automate(
    json_path="MachineRep_Results/automate_machine.txt",
    output_path="MachineRep_Results/ConfigModel.py",
    h_size=1,
)
