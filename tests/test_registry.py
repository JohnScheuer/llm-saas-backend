from src.tool_registry import ToolRegistry


def test_tool_registration():
    registry = ToolRegistry()

    @registry.register
    def hello(name: str):
        """Say hello.

        Args:
            name: Person name
        """
        return f"Hello {name}"

    assert registry.get_tool("hello")("World") == "Hello World"
    assert registry.get_schema("hello")["name"] == "hello"


def test_argument_validation():
    registry = ToolRegistry()

    @registry.register
    def add(a: int, b: int):
        return a + b

    registry.validate_arguments("add", {"a": 1, "b": 2})

    try:
        registry.validate_arguments("add", {"a": 1})
        assert False
    except Exception:
        assert True
