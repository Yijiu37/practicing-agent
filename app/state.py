# app/state.py

from pydantic import BaseModel, Field

from app.trajectory import Trajectory


class AgentState(BaseModel):
    """Agent 在整个执行过程中的统一状态。"""

    # Original task
    task: str

    # Execution history
    trajectory: Trajectory = Field(
        default_factory=Trajectory
    )

    # Runtime state
    iteration: int = 0
    finished: bool = False

    # Tool history
    tool_calls: list = Field(
        default_factory=list
    )

    tool_results: list = Field(
        default_factory=list
    )

    # LLM context
    last_response_id: str | None = None

    # Current pending actions
    pending_tool_calls: list = Field(
        default_factory=list
    )

    pending_tool_outputs: list = Field(
        default_factory=list
    )

    # Final answer
    final_answer: str | None = None