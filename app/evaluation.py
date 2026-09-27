# app/evaluation.py

from pydantic import BaseModel


class Evaluation(BaseModel):

    success: bool
    node_steps: int
    tool_calls: int
    errors: int


def evaluate(state) -> Evaluation:

    # --------------------------------------------------------
    # Count Tool Errors
    # --------------------------------------------------------

    errors = 0

    for step in state.trajectory.steps:

        if step.node == "tool":

            if "error" in step.output:
                errors += 1

    # --------------------------------------------------------
    # Current Success Definition
    # --------------------------------------------------------

    success = (
        state.finished
        and errors == 0
    )

    return Evaluation(
        success=success,
        node_steps=len(
            state.trajectory.steps
        ),
        tool_calls=len(
            state.tool_calls
        ),
        errors=errors,
    )