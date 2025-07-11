from graphviz import Digraph
import re

def visualiser_automate(A, filename="Hybrid_Automato", functions=None):
    """
    Visualise a hybrid automaton using Graphviz, including:
        - discrete states (nodes) with continuous dynamics,
        - transitions with guards, events, and resets.
    """
    # Graph creation
    dot = Digraph(comment="Hybrid Automaton")

    # First node for initial conditions (Invisible node q0)
    dot.node("init", label="", shape="point")
    label_vars = ", ".join(f"{var} = {val}" for var, val in zip(A["X"], A["x0"]))
    label_u = f"U = {A['U']}" if A.get("U") else ""
    init_label = f"{label_vars}\n{label_u}".strip()
    dot.edge("init", A["q0"], label=init_label)
    
    # Creation of nodes according to discreate states
    """
    For each state q in Q, we extract the flow function. Then we try to extract the return 
    value of the function in order to swap the state vectors by its labels. Once it's done, 
    we swap these informations in HTML table for each continuous variable.
    """
    for q in A["Q"]:
        flow_func = A["flow"].get(q)
        flow_name = flow_func.__name__ if callable(flow_func) else flow_func
        label_lines = [f"<TR><TD><B>{q}</B></TD></TR>"]

        # Symbolic display if possible via functions dict
        """
        If a symbolic definition is available in the function dictionary, it is used for a readable display.
        Otherwise, the dynamic range is evaluated numerically to construct the label.
        """
        if flow_name and functions and flow_name in functions:
            try:
                code = functions[flow_name]
                raw_expr = re.findall(r"return\s*\[(.*)\]", code)[0]
                expressions = [e.strip() for e in raw_expr.split(",")]
                for i, expr in enumerate(expressions):
                    for j, var in enumerate(A["X"]):
                        expr = expr.replace(f"x[{j}]", var)
                    label_lines.append(f"<TR><TD>{A['X'][i]}̇ = {expr}</TD></TR>")
            except Exception:
                try:
                    dx = flow_func([0.0] * len(A["X"]), 0.0)
                    for i, val in enumerate(dx):
                        label_lines.append(f"<TR><TD>{A['X'][i]}̇ = {val}</TD></TR>")
                except:
                    for var in A["X"]:
                        label_lines.append(f"<TR><TD>{var}̇ = ?</TD></TR>")
        else:
            try:
                dx = flow_func([0.0] * len(A["X"]), 0.0)
                for i, val in enumerate(dx):
                    label_lines.append(f"<TR><TD>{A['X'][i]}̇ = {val}</TD></TR>")
            except:
                for var in A["X"]:
                    label_lines.append(f"<TR><TD>{var}̇ = ?</TD></TR>")

        label = f"<<TABLE BORDER=\"0\" CELLBORDER=\"0\" CELLSPACING=\"0\">{''.join(label_lines)}</TABLE>>"
        dot.node(q, label=label, shape="ellipse")
    """
    For each transition, we generate a label containing:
      - the guard condition,
      - the name of the triggering event,
      - the reset function, if it actually modifies the variables.
    """
    for t in A["T"]:
        src = t["q_from"]
        dst = t["q_to"]
        guard_name = t.get("guard")
        reset_name = t.get("reset")
        event_name = t.get("event")

        guard_expr = ""
        if guard_name and functions and guard_name in functions:
            try:
                guard_code = functions[guard_name]
                body_match = re.findall(r"return (.*)", guard_code)
                if body_match:
                    guard_code = body_match[0]
                    for i, v in enumerate(A["X"]):
                        guard_code = guard_code.replace(f"x[{i}]", v)
                    guard_code = guard_code.replace("A[\"E\"].get(\"", "").replace("\", False)", "")
                    guard_code = guard_code.replace(" and ", " or ")
                    guard_expr = guard_code
            except Exception:
                guard_expr = guard_name + "(x)"
        elif guard_name:
            guard_expr = guard_name + "(x)"

        parts = []
        if guard_expr:
            parts.append(guard_expr)
        if event_name and event_name not in guard_expr:
            parts.append(event_name)
            
        """
        For the reset functions if it's useful to be shown, we follow the same approach as transitions.
        Otherwise, if we have no reset to do, you have to make exactly the same label as the following 
        exemple: 
        def identity (x) : return x[:]
        def reset_none(x): return x[:] 
        So we do not display these reset functions on the graph
        """
        
        if reset_name and functions and reset_name in functions and reset_name != "identity" and reset_name != "reset_none":
            try:
                reset_code = functions[reset_name]
                match = re.search(r"return\s*\[([^\]]+)\]", reset_code, re.DOTALL)
                if match:
                    raw_values = match.group(1)
                    reset_values = [val.strip() for val in raw_values.split(",")]
                    formatted = []
                    for i, val in enumerate(reset_values):
                        var = A["X"][i] + "′"
                        if val == f"x[{i}]":
                            formatted.append(f"{var} = {A['X'][i]}")
                        else:
                            formatted.append(f"{var} = {val}")
                    parts.append(", ".join(formatted))
                else:
                    parts.append(f"{reset_name}(x)")
            except Exception:
                parts.append(f"{reset_name}(x)")


        label = "[" + ", ".join(parts) + "]" if parts else ""
        dot.edge(src, dst, label=label)

    # Graph generation 
    dot.render("MachineRep_Results/"+filename, format="png", cleanup=True)
    print(f"Automaton Generated : {filename}.png")