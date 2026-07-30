from typing import List, Callable, Any

from .tool_registry import ToolRegistry
from .parser import ToolCallParser
from .executor import ToolExecutor
from .context import AgentContext
from .llm_client import LLMClient


DEFAULT_SYSTEM_PROMPT = """You are a strict tool-calling AI assistant.

When calling a tool:
- Respond ONLY with valid JSON
- Do NOT include explanation
- Do NOT include markdown
- Format:

{
  "tool_calls": [
    {"name": "tool_name", "arguments": {...}}
  ]
}

If no tool is required:
- Respond with the final answer directly.
"""


class Agent:
    def __init__(
        self,
        llm: LLMClient,
        tools: List[Callable],
        max_steps: int = 5,
        system_prompt: str = None,
        force_json: bool = True,
    ):
        self.registry = ToolRegistry()
        for tool in tools:
            self.registry.register(tool)

        self.parser = ToolCallParser(self.registry)
        self.executor = ToolExecutor(self.registry)

        self.llm = llm
        self.max_steps = max_steps
        self.system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.force_json = force_json

    def run(self, user_input: str) -> str:
        context = AgentContext(system_prompt=self.system_prompt)
        context.add_user(user_input)

        for step in range(self.max_steps):
            output = self.llm.generate(
                messages=context.get_messages(),
                tools=self.registry.get_all_schemas()
            )

            calls = self.parser.parse(output)

            if not calls:
                context.add_assistant(output)
                return output

            for call in calls:
                result = self.executor.execute(call)

                if result["success"]:
                    context.add_tool_result(
                        call["name"],
                        result["result"]
                    )
                else:
                    context.add_tool_result(
                        call["name"],
                        f"ERROR: {result['error']}"
                    )

        return "Max steps reached without final answer."
