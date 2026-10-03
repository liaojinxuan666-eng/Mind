import os
import json
import urllib.request
import urllib.error
from providers.base import CortexProvider, CortexResponse, parse_json_safe


SYSTEM_PROMPT = (
    "你是一个人工脑的皮层模块。给你当前焦点、目标和情绪状态，"
    "用一句话说出你在想什么，再给一个简短的动作名。"
    "只返回 JSON，不要别的：{\"thought\": \"...\", \"action\": \"...\"}"
)


class AnthropicProvider(CortexProvider):
    name = "anthropic"

    def __init__(self, api_key=None, model=None, base_url=None,
                 system_prompt=None, max_tokens=512, timeout=60):
        self.api_key = (
            api_key
            or os.environ.get("MIND_API_KEY")
            or os.environ.get("ANTHROPIC_API_KEY")
            or ""
        )
        self.model = model or os.environ.get(
            "MIND_MODEL", "claude-3-5-sonnet-latest"
        )
        self.base_url = (
            base_url
            or os.environ.get("MIND_BASE_URL", "https://api.anthropic.com")
        ).rstrip("/")
        self.system_prompt = system_prompt or SYSTEM_PROMPT
        self.max_tokens = max_tokens
        self.timeout = timeout

    def reason(self, context):
        if not self.api_key:
            return CortexResponse(
                "（没有 API key）", "idle", error="missing_api_key"
            )

        payload = {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "system": self.system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": json.dumps(context, ensure_ascii=False),
                }
            ],
        }

        req = urllib.request.Request(
            f"{self.base_url}/v1/messages",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
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

        blocks = data.get("content", []) or []
        text = "".join(b.get("text", "") for b in blocks if b.get("type") == "text")
        usage = data.get("usage", {}) or {}
        parsed = parse_json_safe(text)

        return CortexResponse(
            thought=parsed["thought"],
            action=parsed["action"],
            prompt_tokens=usage.get("input_tokens", 0) or 0,
            completion_tokens=usage.get("output_tokens", 0) or 0,
        )