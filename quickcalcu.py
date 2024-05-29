import streamlit as st
from collections import deque

def shortest_path_to_range(A, B, C):
    queue = deque([(A, 0, [])])
    visited = set()
    operations = list(range(1, 10))
    max_limit = 30000  # Adjusted limit to 30000

    while queue:
        current, steps, path = queue.popleft()
        
        if B <= current <= C:
            return steps, path
        
        if abs(current) > max_limit:
            continue
        
        for op in operations:
            next_steps = [
                (current + op, f"{current} + {op} = {current + op}"),
                (current - op, f"{current} - {op} = {current - op}"),
                (current * op, f"{current} * {op} = {current * op}"),
                (current // op if op != 0 else None, f"{current} // {op} = {current // op}" if op != 0 else None)
            ]
            for result, desc in next_steps:
                if result is not None and result not in visited and abs(result) <= max_limit:
                    visited.add(result)
                    queue.append((result, steps + 1, path + [desc]))
    
    return -1, []

# Initialize session state variables if not already initialized
if 'A' not in st.session_state:
    st.session_state.A = ""
if 'B' not in st.session_state:
    st.session_state.B = ""
if 'C' not in st.session_state:
    st.session_state.C = ""
if 'result' not in st.session_state:
    st.session_state.result = ""

# Input fields
A = st.text_input("Enter the initial value A: ", value=st.session_state.A)
B = st.text_input("Enter the lower bound B: ", value=st.session_state.B)
C = st.text_input("Enter the upper bound C: ", value=st.session_state.C)

# Update session state with input values
st.session_state.A = A
st.session_state.B = B
st.session_state.C = C

# Clear button
if st.button("Clear"):
    st.session_state.A = ""
    st.session_state.B = ""
    st.session_state.C = ""
    st.session_state.result = ""

# If inputs are valid integers, perform the calculation
if A and B and C:
    try:
        A = int(A)
        B = int(B)
        C = int(C)

        steps, path = shortest_path_to_range(A, B, C)
        if steps != -1:
            result = f"The shortest path from {A} to the range [{B}, {C}] takes {steps} steps.\n\n"
            result += "The steps are as follows:\n\n" + "\n\n".join(path)
            st.session_state.result = result
        else:
            st.session_state.result = f"No path found from {A} to the range [{B}, {C}]."
    except ValueError:
        st.session_state.result = "Please enter valid integer values for A, B, and C."

# Display result
st.write(st.session_state.result)
