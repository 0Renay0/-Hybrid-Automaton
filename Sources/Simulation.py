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