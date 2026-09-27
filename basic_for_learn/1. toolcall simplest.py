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
# 3. 定义 Tool
# =========================

def calculator(a: float, b: float) -> float:
    """计算两个数字的和。"""
    return a + b


# =========================
# 4. Tool Registry
# =========================

tool_registry = {
    "calculator": calculator,
}


# =========================
# 5. 告诉 LLM 有哪些 Tool
# =========================

tools = [
    {
        "type": "function",
        "name": "calculator",
        "description": "计算两个数字的和。",
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
            },
            "required": ["a", "b"],
        },
    }
]


# =========================
# 6. 第一次调用 LLM
# =========================

input_items = [
    {
        "role": "user",
        "content": "请计算 12345 + 6789",
    }
]

response = client.responses.create(
    model="gpt-5",
    input=input_items,
    tools=tools,
)


# =========================
# 7. 执行 LLM 请求的 Tool
# =========================

tool_outputs = []

for item in response.output:

    if item.type == "function_call":

        # Tool 名称
        tool_name = item.name

        # Tool 参数
        arguments = json.loads(item.arguments)

        # 从 Registry 中找到真正的 Python 函数
        tool = tool_registry[tool_name]

        # 执行 Tool
        result = tool(**arguments)

        print("Tool:", tool_name)
        print("Arguments:", arguments)
        print("Result:", result)

        # =========================
        # 8. 把 Tool 结果包装起来
        # =========================

        tool_outputs.append(
            {
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": str(result),
            }
        )


# =========================
# 9. 把 Tool 结果重新交给 LLM
# =========================

response = client.responses.create(
    model="gpt-5",
    # “请基于刚才那一次模型响应继续处理，而不是从零开始。”
    previous_response_id=response.id,
    input=tool_outputs,
    tools=tools,
)


# =========================
# 10. 输出 LLM 最终回答
# =========================

print("Final Answer:", response.output_text)