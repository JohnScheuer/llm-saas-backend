import inspect
import typing
from typing import get_origin, get_args


PYTHON_TO_JSON_TYPES = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    dict: "object",
    list: "array",
}


def _resolve_type(annotation):
    """Resolve Python type hints to JSON schema type."""
    origin = get_origin(annotation)
    args = get_args(annotation)

    if annotation in PYTHON_TO_JSON_TYPES:
        return {"type": PYTHON_TO_JSON_TYPES[annotation]}

    if origin is list or origin is typing.List:
        item_type = args[0] if args else str
        return {
            "type": "array",
            "items": _resolve_type(item_type),
        }

    if origin is dict or origin is typing.Dict:
        return {"type": "object"}

    if origin is typing.Union:
        # Optional[X] -> Union[X, NoneType]
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return _resolve_type(non_none[0])
        return {"type": "string"}

    return {"type": "string"}  # fallback


def _parse_docstring(docstring: str):
    """
    Parse docstring into:
    - description (top section)
    - param_descriptions (Args: section)
    """
    if not docstring:
        return "", {}

    lines = docstring.strip().split("\n")
    description_lines = []
    param_descriptions = {}

    mode = "desc"

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("Args:"):
            mode = "args"
            continue

        if mode == "desc":
            description_lines.append(stripped)
        elif mode == "args":
            if ":" in stripped:
                name, desc = stripped.split(":", 1)
                param_descriptions[name.strip()] = desc.strip()

    description = " ".join(description_lines).strip()
    return description, param_descriptions


def generate_schema(func):
    """Generate OpenAI-compatible function calling schema."""
    sig = inspect.signature(func)
    doc = inspect.getdoc(func)

    description, param_docs = _parse_docstring(doc)

    properties = {}
    required = []

    for name, param in sig.parameters.items():
        annotation = param.annotation if param.annotation != inspect._empty else str
        schema = _resolve_type(annotation)

        if name in param_docs:
            schema["description"] = param_docs[name]

        properties[name] = schema

        if param.default == inspect._empty:
            required.append(name)

    return {
        "name": func.__name__,
        "description": description,
        "parameters": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
    }
