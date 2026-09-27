# 轨迹管理模块
# 记录完成某个任务的执行轨迹，记录下每一个操作为 step
# 包括每一步的输入输出和节点信息，便于形成经验

from pydantic import BaseModel, Field
from typing import Any

# 单步执行轨迹
class TrajectoryStep(BaseModel):
    step: int
    node: str
    input: dict[str, Any] = Field(default_factory=dict)
    output: dict[str, Any] = Field(default_factory=dict)


# 总的执行轨迹
class Trajectory(BaseModel):
    # 管理所有的 steps
    steps: list[TrajectoryStep] = Field(default_factory=list)

    def add_step(
        self,
        node: str,
        input: dict[str, Any] | None = None,
        output: dict[str, Any] | None = None,
    ):
        step = TrajectoryStep(
            step=len(self.steps) + 1,
            node=node,
            input=input or {},
            output=output or {},
        )

        self.steps.append(step)