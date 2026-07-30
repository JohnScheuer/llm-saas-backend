from abc import ABC, abstractmethod
from typing import List, Dict, Any


class LLMClient(ABC):
    """
    Abstract LLM client.
    """

    @abstractmethod
    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] = None,
    ) -> str:
        """
        Should return raw model output as string.
        """
        pass
