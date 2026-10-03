from providers import get_provider


class Neocortex:
    """皮层：LLM 接口。只负责调用 provider，累加 token。"""

    def __init__(self, provider=None):
        self.provider = provider or get_provider()
        self.temperature = 0.7
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.last_error = ""

    @property
    def total_tokens(self):
        return self.total_prompt_tokens + self.total_completion_tokens

    def reason(self, ctx):
        resp = self.provider.reason(ctx)

        self.total_prompt_tokens += resp.prompt_tokens
        self.total_completion_tokens += resp.completion_tokens
        if resp.error:
            self.last_error = resp.error

        return {
            "thought": resp.thought,
            "action": resp.action,
            "tokens": resp.total_tokens,
            "prompt_tokens": resp.prompt_tokens,
            "completion_tokens": resp.completion_tokens,
            "error": resp.error,
        }