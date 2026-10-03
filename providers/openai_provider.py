import os
import json
import urllib.request
import urllib.error
from providers.base import CortexProvider, CortexResponse, parse_json_safe


SYSTEM_PROMPT = (
    "你是一个人工脑的皮层模块。给你当前焦点、目标和情绪状态，"
    "用一句话说出你在想什么，再给一个简短的动作名。"
    "严格返回 JSON：{\"thought\": \"...\", \"action\": \"...\"}"
)


class OpenAIProvider(CortexProvider):
    """兼容 OpenAI Chat Completions 协议的所有端点：
    OpenAI / DeepSeek / 硅基流动 / Moonshot / 本地 vLLM / Ollama ...
    """
    name = "openai"

    def __init__(self, api_key=None, model=None, base_url=None,
                 system_prompt=None, temperature=0.7, timeout=60):
        self.api_key = (
            api_key
            or os.environ.get("MIND_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or ""
        )
        self.model = model or os.environ.get("MIND_MODEL", "gpt-4o-mini")
        self.base_url = (
            base_url
            or os.environ.get("MIND_BASE_URL", "https://api.openai.com/v1")
        ).rstrip("/")
        self.system_prompt = system_prompt or SYSTEM_PROMPT
        self.temperature = temperature
        self.timeout = timeout

    def reason(self, context):
        if not self.api_key:
            return CortexResponse(
                "（没有 API key）", "idle", error="missing_api_key"
            )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {
                    "role": "user",
                    "content": json.dumps(context, ensure_ascii=False),
                },
            ],
            "temperature": self.temperature,
        }

        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as r:
                data = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="ignore")[:200]
            return CortexResponse(
                f"（HTTP {e.code}）", "idle", error=body
            )
        except Exception as e:
            return CortexResponse(f"（{type(e).__name__}）", "idle", error=str(e))

        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage", {}) or {}
        parsed = parse_json_safe(content)

        return CortexResponse(
            thought=parsed["thought"],
            action=parsed["action"],
            prompt_tokens=usage.get("prompt_tokens", 0) or 0,
            completion_tokens=usage.get("completion_tokens", 0) or 0,
        )