import torch
from transformers import StoppingCriteria


class RepetitionStoppingCriteria(StoppingCriteria):
    """
    Stop generation when suspicious repetition pattern appears.
    """

    def __init__(self, tokenizer, max_tail_repeats: int = 3):
        self.tokenizer = tokenizer
        self.max_tail_repeats = max_tail_repeats

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor, **kwargs) -> bool:
        decoded = self.tokenizer.decode(input_ids[0], skip_special_tokens=True)

        # Stop if repeated phrase appears too many times
        phrase = 'The tool calls "calculator"'
        if decoded.count(phrase) >= self.max_tail_repeats:
            return True

        # Stop if polite loop detected
        if decoded.count("How may I assist you") >= self.max_tail_repeats:
            return True

        return False
