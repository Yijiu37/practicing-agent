import os

from dotenv import load_dotenv
from openai import OpenAI

from app.state import AgentState
from app.tools.registry import tool_schemas


load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL"),
)


def llm_node(state: AgentState) -> AgentState:

    print("LLM Node")

    # ========================================================
    # Prepare Input
    # ========================================================

    if state.last_response_id is None:

        input_items = [
            {
                "role": "user",
                "content": state.task,
            }
        ]

        response = client.responses.create(
            model="gpt-5",
            input=input_items,
            tools=tool_schemas,
        )

    else:

        input_items = state.pending_tool_outputs

        response = client.responses.create(
            model="gpt-5",
            previous_response_id=state.last_response_id,
            input=input_items,
            tools=tool_schemas,
        )

    # ========================================================
    # Update Response State
    # ========================================================

    state.last_response_id = response.id

    # 当前轮重新生成 Tool Calls
    state.pending_tool_calls.clear()

    # ========================================================
    # Extract Tool Calls
    # ========================================================

    for item in response.output:

        if item.type != "function_call":
            continue

        tool_call = {
            "name": item.name,
            "arguments": item.arguments,
            "call_id": item.call_id,
        }

        # 当前轮 Tool Calls
        state.pending_tool_calls.append(
            tool_call
        )

        # 整个 Agent 生命周期中的 Tool Calls
        state.tool_calls.append(
            tool_call
        )

    # ========================================================
    # Final Answer
    # ========================================================

    if not state.pending_tool_calls:

        state.finished = True
        state.final_answer = response.output_text

    # ========================================================
    # Trajectory
    # ========================================================

    state.trajectory.add_step(
        node="llm",
        input={
            "task": state.task,
        },
        output={
            "tool_calls": state.pending_tool_calls.copy(),
            "final_answer": state.final_answer,
        },
    )

    return state