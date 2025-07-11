import matplotlib.pyplot as plt

def simulate(A, dt=0.01, t_max=10.0, event_schedule=None):
    """
    This functions simulate the evolution of a hybrid automaton over time. 

    Parameters: 
        A(dict) : The hybrid automaton structure 
        dt(float) : Time step for numerical integration 
        t_max : Maximum simulation time 
        event_schedule: Tuple of (time,event,value(TRUE/FALSE)) which represent a list of timed events

    Returns:
        list of tuples (time, discreate_state, continuous_state)
    """
    t = 0.0
    q = A["q"]
    x = A["x"][:]
    trace = [(t, q, x[:])]

    event_schedule = sorted(event_schedule or [], key=lambda e: e[0])
    current_event_index = 0

    while t < t_max:
        # Apply programmed events
        while current_event_index < len(event_schedule) and t >= event_schedule[current_event_index][0]:
            _, name, value = event_schedule[current_event_index]
            A["E"][name] = value
            current_event_index += 1

        # Flow
        dx = A["flow"][q](x, t)
        x = [x[i] + dx[i] * dt for i in range(len(x))]

        # Try to activate transition
        transitioned = False
        if q in A["Guard"]:
            for q2 in A["Guard"][q]:
                guard = A["Guard"][q].get(q2)
                jump = A["Jump"].get(q, {}).get(q2, lambda x: x)  
                event = A.get("Event", {}).get(q, {}).get(q2, None)

                # Verification of firing conditions
                guard_true = guard(x) if callable(guard) else False
                event_true = A["E"].get(event, False) if event else False

                if guard_true or event_true:
                    x = jump(x)  # Apply reset (jumps)
                    q = q2
                    A["q"] = q
                    A["x"] = x[:]
                    transitioned = True
                    break

        # Time 
        t += dt
        trace.append((t, q, x[:]))

    return trace


def plot_trace(trace, A):
    """
    Plots the evolution of continuous and discrete states over time.

    Parameters:
        - trace (list): The trace returned by `simulate`.
        - A (dict): The hybrid automaton structure, used to label variables.
    """
    times = [t for t, _, _ in trace]
    states = [q for _, q, _ in trace]
    state_set = sorted(set(states))
    q_dict = {state: i for i, state in enumerate(state_set)}
    
    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

    # Plot continuous variables 
    var_names = A["X"]
    n_vars = len(var_names)
    for i in range(n_vars):
        values = [x[i] for _, _, x in trace]
        axs[0].plot(times, values, label=var_names[i])
    axs[0].set_ylabel("Variables continues")
    axs[0].legend()

    # Plot discrete states as step transitions
    q_vals = [q_dict[q] for q in states]
    axs[1].step(times, q_vals, where='post')
    axs[1].set_yticks(list(q_dict.values()))
    axs[1].set_yticklabels(list(q_dict.keys()))
    axs[1].set_ylabel("État discret")
    axs[1].set_xlabel("Temps")

    plt.tight_layout()
    plt.show()