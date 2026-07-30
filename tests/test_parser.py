from src.tool_registry import ToolRegistry
from src.parser import ToolCallParser


def setup_registry():
    registry = ToolRegistry()

    @registry.register
    def calculator(expression: str):
        return eval(expression)

    return registry


def test_openai_format():
    registry = setup_registry()
    parser = ToolCallParser(registry)

    text = '''
    {
      "tool_calls": [
        {"name": "calculator", "arguments": {"expression": "2+2"}}
      ]
    }
    '''

    calls = parser.parse(text)
    assert calls[0]["name"] == "calculator"
    assert calls[0]["arguments"]["expression"] == "2+2"


def test_qwen_format():
    registry = setup_registry()
    parser = ToolCallParser(registry)

    text = '<tool_call>{"name":"calculator","arguments":{"expression":"3*3"}}</tool_call>'
    calls = parser.parse(text)

    assert calls[0]["arguments"]["expression"] == "3*3"


def test_react_format():
    registry = setup_registry()
    parser = ToolCallParser(registry)

    text = '''
    Action: calculator
    Action Input: {"expression": "5+5"}
    '''

    calls = parser.parse(text)
    assert calls[0]["arguments"]["expression"] == "5+5"
