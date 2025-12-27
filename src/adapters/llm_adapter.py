
from typing import List

class LLMAdapter:
    """Abstract interface for different LLM backends"""
    def __init__(self, model_name: str, base_url: str):
        self.model_name = model_name
        self.base_url = base_url
        
    def generate_text(self, prompt: str, **kwargs) -> str:
        """Abstract method - implement for each LLM backend"""
        raise NotImplementedError
        
    def batch_generate(self, prompts: List[str], **kwargs) -> List[str]:
        """Batch text generation"""
        # A basic implementation could just loop over generate_text
        return [self.generate_text(prompt, **kwargs) for prompt in prompts]
