import json

from app.state import AgentState
from app.tools.registry import tool_registry


def record_tool_result(
    state: AgentState,
    tool_name: str,
    arguments: dict,
    call_id: str,
    result: object | None = None,
    error: str | None = None,
):
    """
    统一记录 Tool 执行结果。
    """

    # ========================================================
    # Success
    # ========================================================

    if error is None:

        state.tool_results.append(
            {
                "call_id": call_id,
                "tool": tool_name,
                "result": result,
            }
        )

        state.trajectory.add_step(
            node="tool",
            input={
                "tool": tool_name,
                "arguments": arguments,
            },
            output={
                "result": result,
            },
        )

        state.pending_tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": call_id,
                "output": str(result),
            }
        )

        return

    # ========================================================
    # Error
    # ========================================================

    state.tool_results.append(
        {
            "call_id": call_id,
            "tool": tool_name,
            "error": error,
        }
    )

    state.trajectory.add_step(
        node="tool",
        input={
            "tool": tool_name,
            "arguments": arguments,
        },
        output={
            "error": error,
        },
    )

    state.pending_tool_outputs.append(
        {
            "type": "function_call_output",
            "call_id": call_id,
            "output": (
                f"Tool execution failed: {error}"
            ),
        }
    )


def tool_node(state: AgentState) -> AgentState:

    print("Tool Node")

    # ========================================================
    # Clear Previous Outputs
    # ========================================================

    state.pending_tool_outputs.clear()

    # ========================================================
    # Execute Tool Calls
    # ========================================================

    for tool_call in state.pending_tool_calls:

        tool_name = tool_call["name"]

        arguments = json.loads(
            tool_call["arguments"]
        )

        call_id = tool_call["call_id"]

        print(
            f"Tool Call: {tool_name}"
        )

        print(
            f"Arguments: {arguments}"
        )

        # ====================================================
        # Find Tool
        # ====================================================

        tool = tool_registry.get(
            tool_name
        )

        if tool is None:

            error_message = (
                f"Unknown tool: {tool_name}"
            )

            print(
                f"Tool Error: {error_message}"
            )

            record_tool_result(
                state=state,
                tool_name=tool_name,
                arguments=arguments,
                call_id=call_id,
                error=error_message,
            )

            continue

        # ====================================================
        # Execute Tool
        # ====================================================

        try:

            result = tool(**arguments)

            print(
                f"Tool Result: {result}"
            )

            record_tool_result(
                state=state,
                tool_name=tool_name,
                arguments=arguments,
                call_id=call_id,
                result=result,
            )

        except Exception as e:

            error_message = str(e)

            print(
                f"Tool Error: {error_message}"
            )

            record_tool_result(
                state=state,
                tool_name=tool_name,
                arguments=arguments,
                call_id=call_id,
                error=error_message,
            )

    return state