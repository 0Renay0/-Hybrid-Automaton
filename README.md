# Hybrid Automaton (HA)

This project provides a modular framework to **model**, **simulate**, and **visualize** a hybrid automata. A hybrid automaton is a formalism that combines **continuous dynamics** and **discreate events**.

## Project structure
  -  `HybridAutomaton.py` defines and builds the hybrid autoamton structure.
  -  `Simulation.py` simulate the model of HA.
  -  `VisuelAutomate.py` generates the representation and the trace of simulation of HA.

## Installation 
Required packages:
```bash
pip install graphviz matplotlib
pip install pandas
```
## Main functions

### Construction of HA (`HybridAutomaton.py`)
  - `create_automate()`  initializes a new automaton structure.
  - Utility functions: `add_discrete_state`, `define_continuous_space`, `set_flow`, `set_guard`, `set_jump`,... are provided to build your model.
  - `export_automate_to_txt_with_functions(...)` saves the automaton and associated Python functions as JSON for conversion into another formalsims.

### Simulation (`Simulation.py`)
  - `simulate(A, dt, t_max, event_schedule=None)` simulates the time evolution of the automaton with optional event scheduling depending on your model if it contains event or not.
  - `plot_trace(trace, A)` plots the evolution of continuous variables and discrete states.

### Visualization (`VisuelAutomate.py`)
  - `visualiser_automate(A, filename, functions)` generates a `.png` diagram showing the representation of HA.

## Output 

# HA representation
Hybrid automata describing a thermostat:
<p align="center">
  <img src="Thermostat_Results/automate_hysteresis.png" alt="Example of the thermostat's HA representation " width="400"/>
</p>

# HA Simulation
Simulation of this hybrid system:
<p align="center">
  <img src="Thermostat_Results/SimulationThermostat.png" alt="Example of the thermostat's HA simulation " width="400"/>
</p>

# Json Structure for the conversion of the HA to HtPN
{
  "Q": ["Q1", "Q2"],
  "X": ["x", "tau"],
  "q0": "Q1",
  "x0": [72.0, 0.0],
  "U": [0.0, 1.0],
  "flow": {
    "Q1": "flow_Q1",
    "Q2": "flow_Q2"
  }
}


## Author 
Developped by **HAMADI Rayen** as part of research and academic projects involving hybrid systems.

