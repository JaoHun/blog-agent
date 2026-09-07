import os

import requests


API_URL = "https://api.deepseek.com/chat/completions"
MODEL = "deepseek-v4-flash"


def create_chat_completion(
    messages: list[dict],
    tools: list[dict] | None = None,
) -> dict:
    api_key = os.environ.get("DEEPSEEK_API_KEY")

    if not api_key:
        raise RuntimeError("DEEPSEEK_API_KEY 未配置")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "thinking": {
            "type": "disabled"
        },
        "stream": False,
    }

    if tools:
        payload["tools"] = tools
        payload["tool_choice"] = "auto"

    response = requests.post(
        API_URL,
        headers=headers,
        json=payload,
        timeout=60,
    )

    response.raise_for_status()

    data = response.json()

    choices = data.get("choices")

    if not choices:
        raise RuntimeError("DeepSeek API 未返回 choices")

    return choices[0]["message"]


def chat_with_deepseek(message: str) -> str:
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant.",
        },
        {
            "role": "user",
            "content": message,
        },
    ]

    result = create_chat_completion(messages)

    return result.get("content") or ""