import torch
from typing import List, Dict, Any, Optional

from transformers import AutoModelForCausalLM, AutoTokenizer
from ..llm_client import LLMClient


class HuggingFaceClient(LLMClient):

    def __init__(
        self,
        model_name: str,
        device: Optional[str] = None,
        max_new_tokens: int = 128,
        temperature: float = 0.0,
    ):
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature

        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True,
        )

        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True,
        )

        if self.device != "cuda":
            self.model.to(self.device)

        self.model.eval()

    def generate(
        self,
        messages: List[Dict[str, str]],
        tools: List[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:

        input_text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,
        )

        inputs = self.tokenizer(
            input_text,
            return_tensors="pt"
        ).to(self.device)

        input_ids = inputs["input_ids"]
        prompt_tokens = input_ids.shape[-1]

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=self.max_new_tokens,
                do_sample=False,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.eos_token_id,
            )

        generated_ids = outputs[0][input_ids.shape[-1]:]
        completion_tokens = generated_ids.shape[-1]

        response = self.tokenizer.decode(
            generated_ids,
            skip_special_tokens=True
        ).strip()

        return {
            "text": response,
            "usage": {
                "prompt_tokens": int(prompt_tokens),
                "completion_tokens": int(completion_tokens),
                "total_tokens": int(prompt_tokens + completion_tokens),
            }
        }
