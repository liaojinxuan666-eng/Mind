import os
from providers.base import CortexProvider, CortexResponse
from providers.mock import MockProvider
from providers.openai_provider import OpenAIProvider
from providers.anthropic_provider import AnthropicProvider


def get_provider(name=None, **kwargs):
    name = (name or os.environ.get("MIND_PROVIDER", "mock")).lower()

    if name in ("mock", "", "none"):
        return MockProvider()

    if name in ("openai",):
        return OpenAIProvider(**kwargs)

    if name in ("deepseek",):
        kwargs.setdefault("base_url", "https://api.deepseek.com/v1")
        kwargs.setdefault("model", "deepseek-chat")
        return OpenAIProvider(**kwargs)

    if name in ("anthropic", "claude"):
        return AnthropicProvider(**kwargs)

    if name in ("ollama",):
        kwargs.setdefault("base_url", "http://localhost:11434/v1")
        kwargs.setdefault("api_key", "ollama")
        kwargs.setdefault("model", os.environ.get("MIND_MODEL", "llama3.1"))
        return OpenAIProvider(**kwargs)

    raise ValueError(f"未知的 provider: {name}")