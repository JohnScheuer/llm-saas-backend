import torch
from transformers import LogitsProcessor


class JSONLogitsProcessor(LogitsProcessor):
    """
    Restrict generation to JSON-safe characters.
    This prevents markdown, explanations, etc.
    """

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

        # Allowed characters for JSON tool calling
        allowed_chars = set(
            '{}[]":,.-_0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ \n'
        )

        vocab = tokenizer.get_vocab()
        self.allowed_token_ids = []

        for token, token_id in vocab.items():
            decoded = tokenizer.decode([token_id])

            if all(char in allowed_chars for char in decoded):
                self.allowed_token_ids.append(token_id)

        self.allowed_token_ids = set(self.allowed_token_ids)

    def __call__(self, input_ids, scores):
        mask = torch.full_like(scores, float("-inf"))

        allowed = list(self.allowed_token_ids)
        mask[:, allowed] = scores[:, allowed]

        return mask
