import json


def parse_openai_format(text: str):
    """
    Expected format:
    {
      "tool_calls": [
        {"name": "...", "arguments": {...}}
      ]
    }
    """

    try:
        data = json.loads(text)
    except Exception:
        return []

    if not isinstance(data, dict):
        return []

    if "tool_calls" not in data:
        return []

    calls = []

    for call in data["tool_calls"]:
        if "name" in call:
            calls.append({
                "name": call["name"],
                "arguments": call.get("arguments", {})
            })

    return calls
