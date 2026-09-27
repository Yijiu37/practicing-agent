from app.state import AgentState


class MiniGraph:

    def __init__(self):

        self.nodes = {}

        self.edges = {}

        self.conditional_edges = {}

        self.start_node = None

    # ========================================================
    # Add Node
    # ========================================================

    def add_node(
        self,
        name,
        node,
    ):

        self.nodes[name] = node

    # ========================================================
    # Add Normal Edge
    # ========================================================

    def add_edge(
        self,
        from_node,
        to_node,
    ):

        self.edges[from_node] = to_node

    # ========================================================
    # Add Conditional Edge
    # ========================================================

    def add_conditional_edges(
        self,
        node_name,
        router,
    ):

        self.conditional_edges[
            node_name
        ] = router

    # ========================================================
    # Set Entry Point
    # ========================================================

    def set_entry_point(
        self,
        node_name,
    ):

        self.start_node = node_name

    # ========================================================
    # Run
    # ========================================================

    def run(
        self,
        state: AgentState,
    ):

        current_node = self.start_node

        while current_node is not None:

            state.iteration += 1

            print(
                f"\n--- Iteration "
                f"{state.iteration} ---"
            )

            # ------------------------------------------------
            # Safety Limit
            # ------------------------------------------------

            if state.iteration > 10:

                raise RuntimeError(
                    "Graph exceeded maximum iterations."
                )

            # ------------------------------------------------
            # Execute Node
            # ------------------------------------------------

            node = self.nodes[
                current_node
            ]

            state = node(state)

            # ------------------------------------------------
            # Conditional Edge
            # ------------------------------------------------

            if (
                current_node
                in self.conditional_edges
            ):

                router = (
                    self.conditional_edges[
                        current_node
                    ]
                )

                current_node = router(state)

                if current_node == "end":
                    break

                continue

            # ------------------------------------------------
            # Normal Edge
            # ------------------------------------------------

            if (
                current_node
                in self.edges
            ):

                current_node = (
                    self.edges[
                        current_node
                    ]
                )

                continue

            # ------------------------------------------------
            # No Edge
            # ------------------------------------------------

            break

        return state