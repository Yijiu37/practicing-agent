import json
import os

from dotenv import load_dotenv
from openai import OpenAI


# =========================
# 1. 加载环境变量
# =========================

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found.")

if not base_url:
    raise ValueError("OPENAI_BASE_URL not found.")


# =========================
# 2. 创建 LLM Client
# =========================

client = OpenAI(
    api_key=api_key,
    base_url=base_url,
)


# =========================
# 3. Tool
# =========================

def calculator(
    a: float,
    b: float,
    operation: str,
) -> float:

    if operation == "add":
        return a + b

    if operation == "subtract":
        return a - b

    if operation == "multiply":
        return a * b

    if operation == "divide":
        return a / b

    raise ValueError(
        f"Unknown operation: {operation}"
    )


# =========================
# 4. Tool Registry
# =========================

tool_registry = {
    "calculator": calculator,
}


# =========================
# 5. Tool Schema
# =========================

tools = [
    {
        "type": "function",
        "name": "calculator",
        "description": "执行基本数学计算。",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "第一个数字",
                },
                "b": {
                    "type": "number",
                    "description": "第二个数字",
                },
                "operation": {
                    "type": "string",
                    "enum": [
                        "add",
                        "subtract",
                        "multiply",
                        "divide",
                    ],
                    "description": "计算操作",
                },
            },
            "required": [
                "a",
                "b",
                "operation",
            ],
        },
    }
]


# =========================
# 6. 初始任务
# =========================

input_items = [
    {
        "role": "system",
        "content": """
你是一个计算 Agent。

所有数学计算都必须使用 calculator 工具完成，
不能直接在语言模型内部计算。

如果一个任务包含多个计算步骤，
必须按照步骤逐步调用 calculator，
并将前一步的结果作为后一步的输入。
""",
    },
    {
        "role": "user",
        "content": "请计算 12345 + 6789，然后把结果乘以2。",
    }
]


# =========================
# 7. Agent Loop
# =========================

response = client.responses.create(
    model="gpt-5",
    input=input_items,
    tools=tools,
)

while True:

    print("\n--- Processing Response ---")

    tool_outputs = []

    for item in response.output:

        if item.type == "function_call":

            print("Tool Call:", item.name)
            print("Arguments:", item.arguments)

            tool_name = item.name

            arguments = json.loads(item.arguments)

            # 找到 Python Function
            tool = tool_registry[tool_name]

            # 执行 Tool
            result = tool(**arguments)

            print("Tool Result:", result)

            # 构造 Tool Result，返回结果到 LLM
            tool_outputs.append(
                {
                    "type": "function_call_output",
                    # 对应这次 Tool Call 的 call_id
                    "call_id": item.call_id,
                    "output": str(result),
                }
            )

    # =========================
    # 没有 Tool Call
    # =========================

    if not tool_outputs:

        print("\nFinal Answer:")
        print(response.output_text)

        break

    # =========================
    # 把 Tool Result
    # 交给下一轮 LLM
    # =========================

    response = client.responses.create(
        model="gpt-5",
        # 上一轮response，用于继续处理
        previous_response_id=response.id,
        input=tool_outputs,
        tools=tools,
    )