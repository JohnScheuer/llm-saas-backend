from src.agent import Agent
from src.llm_client import LLMClient


class MockLLM(LLMClient):
    def __init__(self):
        self.step = 0

    def generate(self, messages, tools=None):
        self.step += 1

        # Step 1 → call calculator
        if self.step == 1:
            return '''
            {
              "tool_calls": [
                {"name": "calculator", "arguments": {"expression": "2+3"}}
              ]
            }
            '''

        # Step 2 → final answer
        return "The result is 5."


def calculator(expression: str):
    return eval(expression)


def test_agent_multi_step():
    llm = MockLLM()

    agent = Agent(
        llm=llm,
        tools=[calculator],
        max_steps=3
    )

    result = agent.run("What is 2+3?")

    assert "5" in result
