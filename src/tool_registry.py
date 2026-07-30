import inspect
from typing import Callable, Dict, Any, Tuple


class ToolValidationError(Exception):
    pass


class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: Dict[str, Dict[str, Any]] = {}

    def register(self, func: Callable):
        name = func.__name__

        if name in self._tools:
            raise ValueError(f"Tool '{name}' already registered.")

        self._tools[name] = func
        from .schema_generator import generate_schema
        self._schemas[name] = generate_schema(func)

        return func

    # ✅ Return resolved name + function
    def resolve_tool(self, name: str) -> Tuple[str, Callable]:

        if name in self._tools:
            return name, self._tools[name]

        if len(self._tools) == 1:
            actual_name = next(iter(self._tools.keys()))
            return actual_name, self._tools[actual_name]

        raise ToolValidationError(f"Tool '{name}' not registered.")

    def get_schema(self, name: str) -> Dict[str, Any]:
        return self._schemas.get(name)

    def get_all_schemas(self):
        return list(self._schemas.values())

    def validate_arguments(self, name: str, arguments: Any) -> Dict[str, Any]:

        resolved_name, func = self.resolve_tool(name)

        sig = inspect.signature(func)
        expected_params = list(sig.parameters.keys())

        normalized = self._normalize_arguments(arguments, expected_params)

        for param_name, param in sig.parameters.items():
            if param.default == inspect._empty and param_name not in normalized:
                raise ToolValidationError(
                    f"Missing required argument '{param_name}' for tool '{resolved_name}'."
                )

        return {
            "resolved_name": resolved_name,
            "arguments": normalized
        }

    # ------------------------------------------------

    def _normalize_arguments(self, arguments: Any, expected_params):

        if isinstance(arguments, dict):
            return arguments

        if isinstance(arguments, list):
            if len(expected_params) == 1:
                return {expected_params[0]: self._build_expression(arguments)}
            return {}

        if isinstance(arguments, str):
            if len(expected_params) == 1:
                return {expected_params[0]: arguments}
            return {}

        if isinstance(arguments, (int, float)):
            if len(expected_params) == 1:
                return {expected_params[0]: str(arguments)}
            return {}

        return {}

    def _build_expression(self, values):
        if len(values) == 2:
            return f"{values[0]} * {values[1]}"
        return str(values)
