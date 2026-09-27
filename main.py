from app.agent import run_agent
from app.evaluation import evaluate


if __name__ == "__main__":

    task = (
        "先告诉我我的名字，然后计算 1+1，最后告诉我结果，并把结果乘以3"
    )

    state = run_agent(task)

    evaluation = evaluate(state)

    print("\n" + "=" * 60)
    print("EVALUATION")
    print("=" * 60)

    print(
        f"\nSuccess: "
        f"{evaluation.success}"
    )

    print(
        f"Node Steps: "
        f"{evaluation.node_steps}"
    )

    print(
        f"Tool Calls: "
        f"{evaluation.tool_calls}"
    )

    print(
        f"Errors: "
        f"{evaluation.errors}"
    )