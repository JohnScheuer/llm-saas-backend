import time
from typing import List, Dict, Any


class StepTrace:
    def __init__(self, step_id: int):
        self.step_id = step_id
        self.llm_latency = 0.0
        self.tool_calls: List[Dict[str, Any]] = []
        self.final_answer = None

    def to_dict(self):
        return {
            "step_id": self.step_id,
            "llm_latency_ms": round(self.llm_latency * 1000, 2),
            "tool_calls": self.tool_calls,
            "final_answer": self.final_answer,
        }


class AgentTrace:
    def __init__(self):
        self.start_time = time.time()
        self.steps: List[StepTrace] = []
        self.total_time = 0.0

    def add_step(self, step: StepTrace):
        self.steps.append(step)

    def finish(self):
        self.total_time = time.time() - self.start_time

    def to_dict(self):
        return {
            "total_time_ms": round(self.total_time * 1000, 2),
            "steps": [s.to_dict() for s in self.steps],
        }
