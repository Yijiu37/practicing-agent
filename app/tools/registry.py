from typing import Any

from app.tools.calculator import calculator
from app.tools.user import get_user_name


# ============================================================
# Tool Registry
# ============================================================

tool_registry: dict[str, Any] = {
    "calculator": calculator,
    "get_user_name": get_user_name,
}


# ============================================================
# Tool Schemas
# ============================================================

tool_schemas = [
    {
        "type": "function",
        "name": "calculator",
        "description": "执行基本数学计算。",
        "parameters": {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "第一个数字。",
                },
                "b": {
                    "type": "number",
                    "description": "第二个数字。",
                },
                "operation": {
                    "type": "string",
                    "enum": [
                        "add",
                        "subtract",
                        "multiply",
                        "divide",
                    ],
                    "description": "计算操作。",
                },
            },
            "required": [
                "a",
                "b",
                "operation",
            ],
        },
    },
    {
        "type": "function",
        "name": "get_user_name",
        "description": "获取当前用户的名字。",
        "parameters": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
]