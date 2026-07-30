import asyncio
from src.tool_registry import ToolRegistry
from src.executor import ToolExecutor


def setup_registry():
    registry = ToolRegistry()

    @registry.register
    def add(a: int, b: int):
        return a + b

    @registry.register
    async def async_multiply(a: int, b: int):
        await asyncio.sleep(0.01)
        return a * b

    @registry.register
    def fail():
        raise ValueError("Boom")

    return registry


def test_sync_execution():
    registry = setup_registry()
    executor = ToolExecutor(registry)

    result = executor.execute({
        "name": "add",
        "arguments": {"a": 2, "b": 3}
    })

    assert result["success"] is True
    assert result["result"] == 5


def test_async_execution_sync_wrapper():
    registry = setup_registry()
    executor = ToolExecutor(registry)

    result = executor.execute({
        "name": "async_multiply",
        "arguments": {"a": 3, "b": 4}
    })

    assert result["success"] is True
    assert result["result"] == 12


def test_error_handling():
    registry = setup_registry()
    executor = ToolExecutor(registry)

    result = executor.execute({
        "name": "fail",
        "arguments": {}
    })

    assert result["success"] is False
    assert "Boom" in result["error"]
