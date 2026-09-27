from app.graph.mini_graph import MiniGraph
from app.nodes.llm import llm_node
from app.nodes.tool import tool_node
from app.state import AgentState


# ============================================================
# Router
# ============================================================

def route_after_llm(
    state: AgentState,
) -> str:

    if state.finished:
        return "end"

    if state.pending_tool_calls:
        return "tool"

    return "end"


# ============================================================
# Build Graph
# ============================================================

def build_graph():

    graph = MiniGraph()

    # --------------------------------------------------------
    # Nodes
    # --------------------------------------------------------

    graph.add_node(
        "llm",
        llm_node,
    )

    graph.add_node(
        "tool",
        tool_node,
    )

    # --------------------------------------------------------
    # Entry Point
    # --------------------------------------------------------

    graph.set_entry_point(
        "llm"
    )

    # --------------------------------------------------------
    # tool → llm
    # --------------------------------------------------------

    graph.add_edge(
        "tool",
        "llm",
    )

    # --------------------------------------------------------
    # llm → tool / end
    # --------------------------------------------------------

    graph.add_conditional_edges(
        "llm",
        route_after_llm,
    )

    return graph


# ============================================================
# Run Agent
# ============================================================

def run_agent(
    task: str,
):

    state = AgentState(
        task=task
    )

    graph = build_graph()

    return graph.run(state)