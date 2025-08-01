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
    export_automate_to_txt_with_functions,
    generate_config_from_automate,
)
from Simulation import simulate, plot_trace  # type: ignore
from VisuelAutomate import visualiser_automate  # type: ignore
import inspect


# === Generic function to extract function source code ===
def collect_functions(*funcs):
    """
    It builds a dictionary of function names to source code strings.
    Only includes callable functions.
    """
    function_names = [f.__name__ for f in funcs if callable(f)]
    source_map = {}
    all_items = list(globals().items())
    for name, func in all_items:
        if callable(func) and name in function_names:
            source_map[name] = inspect.getsource(func)
    return source_map


# === Continuous Dynamics ===


def flow_Q1(x, t):
    return [-x[0] + 50]


def flow_Q2(x, t):
    return [-x[0] + 80]


# === Invariants ===
def inv_Q1(x):
    return True


def inv_Q2(x):
    return True


# === Guard Conditions ===
def guard_Q1_Q2(x):
    return x[0] <= 70


def guard_Q2_Q1(x):
    return x[0] >= 75


# === Jumps ===
def reset_none(x):
    return x[:]


# === Automaton Creation ===
A = create_automate()
define_continuous_space(A, ["x"])  # Define continuous state variables

# Add discrete states
for q in ["Q1", "Q2"]:
    add_discrete_state(A, q)

set_initial_state(A, "Q1", [72.0])  # Initial state

# Assign flow functions to states
flows = {"Q1": flow_Q1, "Q2": flow_Q2}
for q, f in flows.items():
    set_flow(A, q, f)

# Assign invariants to states
Invs = {"Q1": inv_Q1, "Q2": inv_Q2}
for q, f in Invs.items():
    set_invariant(A, q, f)

# Assign guard functions to transitions
guards = {("Q1", "Q2"): guard_Q1_Q2, ("Q2", "Q1"): guard_Q2_Q1}
for (q1, q2), g in guards.items():
    set_guard(A, q1, q2, g)

# Assign jump (reset) functions
jumps = {("Q1", "Q2"): reset_none, ("Q2", "Q1"): reset_none}
for (q1, q2), j in jumps.items():
    set_jump(A, q1, q2, j)


# Declare the transitions with names of guards and resets
for q1, q2 in guards:
    g = guards.get((q1, q2))
    j = jumps.get((q1, q2))
    e = None
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
export_automate_to_txt_with_functions(A, "automate_thermostat.txt", functions)

# Visualize the automaton
visualiser_automate(A, filename="automate_hysteresis", functions=functions)

# === Simulation ===
trace = simulate(A, dt=0.01, t_max=5.0)
plot_trace(trace, A)
generate_config_from_automate(
    json_path="Thermostat_Results/automate_thermostat.txt",
    output_path="Thermostat_Results/ConfigModel.py",
    h_size=1,
)
