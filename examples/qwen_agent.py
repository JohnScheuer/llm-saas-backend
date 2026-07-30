from src.agent import Agent
from src.clients.huggingface_client import HuggingFaceClient


def calculator(expression: str):
    """Evaluate math expression.

    Args:
        expression: Math expression like "2+2"
    """
    return eval(expression)


if __name__ == "__main__":
    llm = HuggingFaceClient(
        model_name="Qwen/Qwen2-0.5B-Instruct",
        temperature=0.0,
    )

    agent = Agent(
        llm=llm,
        tools=[calculator],
        max_steps=5
    )

    result = agent.run("What is 12 * 7?")
    print("\nFINAL RESULT:\n", result)
