import json
import re
from typing import List, Dict, Any

from .tool_registry import ToolRegistry, ToolValidationError
from .formats.openai_format import parse_openai_format
from .formats.qwen_format import parse_qwen_format
from .formats.react_format import parse_react_format


class ToolCallParseError(Exception):
    pass


class ToolCallParser:
    """
    Unified parser that tries multiple formats.
    Returns list of:
    {
        "name": str,
        "arguments": dict
    }
    """

    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def parse(self, text: str) -> List[Dict[str, Any]]:
        parsers = [
            parse_openai_format,
            parse_qwen_format,
            parse_react_format,
        ]

        for parser in parsers:
            calls = parser(text)
            if calls:
                self._validate_calls(calls)
                return calls

        return []

    def _validate_calls(self, calls: List[Dict[str, Any]]):
        for call in calls:
            name = call["name"]
            arguments = call.get("arguments", {})

            if isinstance(arguments, str):
                try:
                    arguments = json.loads(arguments)
                except Exception:
                    raise ToolCallParseError(
                        f"Invalid JSON arguments for tool '{name}'."
                    )

            self.registry.validate_arguments(name, arguments)
            call["arguments"] = arguments
