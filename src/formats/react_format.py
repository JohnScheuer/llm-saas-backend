import re


ACTION_PATTERN = re.compile(
    r"Action:\s*(?P<name>.+?)\s*Action Input:\s*(?P<input>.+)",
    re.DOTALL
)


def parse_react_format(text: str):
    """
    Format:
    Action: calculator
    Action Input: 2+2
    """

    match = ACTION_PATTERN.search(text)
    if not match:
        return []

    name = match.group("name").strip()
    raw_input = match.group("input").strip()

    # Try JSON first
    try:
        import json
        arguments = json.loads(raw_input)
        if not isinstance(arguments, dict):
            arguments = {"input": arguments}
    except Exception:
        arguments = {"input": raw_input}

    return [{
        "name": name,
        "arguments": arguments
    }]
