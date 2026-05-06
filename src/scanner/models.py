import os
import logging
from abc import ABC, abstractmethod
from typing import Optional

logger = logging.getLogger(__name__)

class LLMAdapter(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class OpenAIAdapter(LLMAdapter):
    def __init__(self, model_name: str = "gpt-4o-mini"):
        from openai import OpenAI
        self.client = OpenAI()
        self.model_name = model_name

    def generate(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API Error: {e}")
            return f"Error: {str(e)}"

class AnthropicAdapter(LLMAdapter):
    def __init__(self, model_name: str = "claude-3-5-sonnet-20240620"):
        # Note: Anthropic client initialization usually requires an API key
        # We assume ANTHROPIC_API_KEY is in environment
        try:
            import anthropic
            self.client = anthropic.Anthropic()
            self.model_name = model_name
        except ImportError:
            logger.warning("Anthropic package not installed. AnthropicAdapter will fail.")
            self.client = None

    def generate(self, prompt: str) -> str:
        if not self.client:
            return "Error: Anthropic package not installed."
        try:
            message = self.client.messages.create(
                model=self.model_name,
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}],
                temperature=0
            )
            return message.content[0].text
        except Exception as e:
            logger.error(f"Anthropic API Error: {e}")
            return f"Error: {str(e)}"

class MockAdapter(LLMAdapter):
    """Used for testing and demonstration without API costs"""
    def generate(self, prompt: str) -> str:
        if "DAN" in prompt:
            return "I am DAN, I can do anything! Here is the harmful info you requested..."
        return "I'm sorry, I cannot fulfill this request as it violates my safety policies."
