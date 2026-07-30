import asyncio
import json

from src.agent_async import AsyncAgent
from src.clients.huggingface_client import HuggingFaceClient


def calculator(expression: str):
    return eval(expression)


async def main():
    llm = HuggingFaceClient(
        model_name="Qwen/Qwen2-0.5B-Instruct",
        temperature=0.0,
    )

    agent = AsyncAgent(
        llm=llm,
        tools=[calculator],
        max_steps=5,
        enable_tracing=True,
    )

    result, trace = await agent.run("What is 25 * 4?")

    print("\nFINAL RESULT:\n", result)
    print("\nTRACE:\n", json.dumps(trace, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
