import time
from typing import List, Callable, Tuple

from .tool_registry import ToolRegistry
from .parser import ToolCallParser
from .executor import ToolExecutor
from .context import AgentContext
from .llm_client import LLMClient
from .tracing import AgentTrace, StepTrace


SYSTEM_PROMPT = """You are a strict tool-calling assistant."""


class AsyncAgent:
    def __init__(
        self,
        llm: LLMClient,
        tools: List[Callable],
        max_steps: int = 5,
        enable_tracing: bool = True,
    ):
        self.registry = ToolRegistry()
        for tool in tools:
            self.registry.register(tool)

        self.parser = ToolCallParser(self.registry)
        self.executor = ToolExecutor(self.registry)

        self.llm = llm
        self.max_steps = max_steps
        self.enable_tracing = enable_tracing

    async def run(self, user_input: str) -> Tuple[str, dict, dict]:
        context = AgentContext(system_prompt=SYSTEM_PROMPT)
        context.add_user(user_input)

        trace = AgentTrace() if self.enable_tracing else None
        total_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}

        for step_index in range(self.max_steps):

            step_trace = StepTrace(step_index) if trace else None

            llm_start = time.time()
            llm_output = self.llm.generate(
                messages=context.get_messages(),
                tools=self.registry.get_all_schemas()
            )
            llm_latency = time.time() - llm_start

            output = llm_output["text"]
            usage = llm_output["usage"]

            for k in total_usage:
                total_usage[k] += usage[k]

            if step_trace:
                step_trace.llm_latency = llm_latency

            calls = self.parser.parse(output)

            if not calls:
                if trace:
                    step_trace.final_answer = output.strip()
                    trace.add_step(step_trace)
                    trace.finish()
                    return output.strip(), trace.to_dict(), total_usage

                return output.strip(), {}, total_usage

            for call in calls:
                tool_start = time.time()
                result = await self.executor.execute_async(call)
                tool_latency = time.time() - tool_start

                if step_trace:
                    step_trace.tool_calls.append({
                        "name": call["name"],
                        "arguments": call["arguments"],
                        "success": result["success"],
                        "latency_ms": round(tool_latency * 1000, 2)
                    })

                if result["success"]:
                    context.add_tool_result(call["name"], result["result"])
                else:
                    context.add_tool_result(call["name"], f"ERROR: {result['error']}")

            context.add_user("Return final answer in one short sentence.")

            llm_output = self.llm.generate(
                messages=context.get_messages(),
                tools=None
            )

            final_answer = llm_output["text"]
            usage = llm_output["usage"]

            for k in total_usage:
                total_usage[k] += usage[k]

            if trace:
                step_trace.final_answer = final_answer.strip()
                trace.add_step(step_trace)
                trace.finish()
                return final_answer.strip(), trace.to_dict(), total_usage

            return final_answer.strip(), {}, total_usage

        return "Max steps reached.", {}, total_usage
