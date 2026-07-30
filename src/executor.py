import asyncio
import inspect
from typing import Any, Dict

from .tool_registry import ToolRegistry


class ToolExecutor:
    def __init__(self, registry: ToolRegistry, timeout: float = 10.0):
        self.registry = registry
        self.timeout = timeout

    def execute(self, call: Dict[str, Any]) -> Dict[str, Any]:

        name = call["name"]
        arguments = call.get("arguments", {})

        # ✅ Resolve tool + normalize arguments
        resolved = self.registry.validate_arguments(name, arguments)
        resolved_name = resolved["resolved_name"]
        normalized_args = resolved["arguments"]

        tool_name, tool = self.registry.resolve_tool(resolved_name)

        try:
            if inspect.iscoroutinefunction(tool):
                result = asyncio.run(self._execute_async(tool, normalized_args))
            else:
                result = tool(**normalized_args)

            return {
                "success": True,
                "result": result,
                "tool_name": tool_name
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool_name": tool_name
            }

    async def execute_async(self, call: Dict[str, Any]) -> Dict[str, Any]:

        name = call["name"]
        arguments = call.get("arguments", {})

        resolved = self.registry.validate_arguments(name, arguments)
        resolved_name = resolved["resolved_name"]
        normalized_args = resolved["arguments"]

        tool_name, tool = self.registry.resolve_tool(resolved_name)

        try:
            if inspect.iscoroutinefunction(tool):
                result = await asyncio.wait_for(
                    tool(**normalized_args),
                    timeout=self.timeout
                )
            else:
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None,
                    lambda: tool(**normalized_args)
                )

            return {
                "success": True,
                "result": result,
                "tool_name": tool_name
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "tool_name": tool_name
            }
