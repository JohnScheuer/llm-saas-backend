import json
import re


TOOL_CALL_PATTERN = re.compile(r"<tool_call>(.*?)</tool_call>", re.DOTALL)


def parse_qwen_format(text: str):
    """
    Format:
    <tool_call>{"name": "...", "arguments": {...}}</tool_call>
    """

    matches = TOOL_CALL_PATTERN.findall(text)
    calls = []

    for match in matches:
        try:
            data = json.loads(match.strip())
            calls.append({
                "name": data["name"],
                "arguments": data.get("arguments", {})
            })
        except Exception:
            continue

    return calls
