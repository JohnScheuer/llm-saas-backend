from src.schema_generator import generate_schema


def test_simple_schema():
    def calculator(expression: str) -> float:
        """Evaluate math expression.

        Args:
            expression: Math expression like "2+2"
        """
        return eval(expression)

    schema = generate_schema(calculator)

    assert schema["name"] == "calculator"
    assert schema["parameters"]["properties"]["expression"]["type"] == "string"
    assert "expression" in schema["parameters"]["required"]
