from typing_extensions import TypedDict

# from langgraph.errors import NodeInterrupt   # ❌ deprecated
from langgraph.graph import START, END, StateGraph
from langgraph.types import interrupt          # ✅ NEW replacement

# Define state type
class State(TypedDict):
    input: str

# Step 1
def step_1(state: State) -> State:
    print("---Step 1---")
    return state

# Step 2 with interrupt
def step_2(state: State) -> State:
    if len(state["input"]) > 5:
        # ❌ OLD (deprecated):
        # raise NodeInterrupt(f"Received input that is longer than 5 characters: {state['input']}")

        # ✅ NEW: must return, not raise
        return interrupt(
            f"Received input that is longer than 5 characters: {state['input']}"
        )
    print("---Step 2---")
    return state

# Step 3
def step_3(state: State) -> State:
    print("---Step 3---")
    return state

# Build the graph
builder = StateGraph(State)
builder.add_node("step_1", step_1)
builder.add_node("step_2", step_2)
builder.add_node("step_3", step_3)
builder.add_edge(START, "step_1")
builder.add_edge("step_1", "step_2")
builder.add_edge("step_2", "step_3")
builder.add_edge("step_3", END)

# Compile the graph
graph = builder.compile()