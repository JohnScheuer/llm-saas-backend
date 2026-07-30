from typing import List, Dict, Any


class AgentContext:
    def __init__(self, system_prompt: str = None):
        self.messages: List[Dict[str, Any]] = []

        if system_prompt:
            self.messages.append({
                "role": "system",
                "content": system_prompt
            })

    def add_user(self, content: str):
        self.messages.append({
            "role": "user",
            "content": content
        })

    def add_assistant(self, content: str):
        self.messages.append({
            "role": "assistant",
            "content": content
        })

    def add_tool_result(self, tool_name: str, result: str):
        self.messages.append({
            "role": "tool",
            "name": tool_name,
            "content": str(result)
        })

    def get_messages(self):
        return self.messages
