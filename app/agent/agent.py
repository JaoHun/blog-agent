import json

from app.agent.registry import execute_tool
from app.agent.tool_schemas import TOOLS
from app.llm.deepseek_client import create_chat_completion


SYSTEM_PROMPT = """
你是 JaoHun 个人博客的智能 Agent。

你可以使用工具读取博客中的真实数据。

规则：
1. 用户询问博客有哪些文章或某个主题相关文章时，优先调用 search_posts。
2. 用户要求读取、解释或总结某篇已知 slug 的文章时，调用 get_post。
3. 描述博客内容时必须根据工具返回的真实数据，不要编造文章。
4. 工具没有找到结果时，要如实说明。
5. 普通问候或与博客数据无关的问题，可以直接回答。
"""


def run_agent_with_trace(
    user_message: str,
    max_steps: int = 4,
) -> tuple[str, list[str]]:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    tools_used = []

    for _ in range(max_steps):
        assistant_message = create_chat_completion(
            messages=messages,
            tools=TOOLS,
        )

        tool_calls = assistant_message.get("tool_calls") or []

        if not tool_calls:
            reply = assistant_message.get("content") or ""
            return reply, tools_used

        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.get("content"),
                "tool_calls": tool_calls,
            }
        )

        for tool_call in tool_calls:
            function = tool_call["function"]
            tool_name = function["name"]

            raw_arguments = function.get(
                "arguments",
                "{}",
            )

            try:
                arguments = json.loads(raw_arguments)

                if not isinstance(arguments, dict):
                    raise ValueError(
                        "工具参数必须是 JSON object"
                    )

                result = execute_tool(
                    tool_name,
                    arguments,
                )

                tools_used.append(tool_name)

                tool_result = json.dumps(
                    result,
                    ensure_ascii=False,
                )

            except (
                json.JSONDecodeError,
                TypeError,
                ValueError,
            ) as exc:
                tool_result = json.dumps(
                    {
                        "error": str(exc)
                    },
                    ensure_ascii=False,
                )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call["id"],
                    "content": tool_result,
                }
            )

    raise RuntimeError(
        "Agent 超过最大工具调用次数"
    )


def run_agent(user_message: str) -> str:
    reply, _ = run_agent_with_trace(
        user_message
    )
    return reply