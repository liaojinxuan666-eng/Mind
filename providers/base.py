import json
from dataclasses import dataclass


@dataclass
class CortexResponse:
    thought: str
    action: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    error: str = ""

    @property
    def total_tokens(self):
        return self.prompt_tokens + self.completion_tokens


class CortexProvider:
    name = "base"

    def reason(self, context: dict) -> CortexResponse:
        raise NotImplementedError


def parse_json_safe(text):
    """从 LLM 输出里抠 JSON，失败就退回纯文本。"""
    raw = (text or "").strip()

    # 去掉 ```json ... ``` 包裹
    if raw.startswith("```"):
        lines = raw.split("\n")
        if len(lines) >= 2:
            raw = "\n".join(lines[1:-1]).strip()
        raw = raw.strip("`").strip()
        if raw.startswith("json"):
            raw = raw[4:].strip()

    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            return {
                "thought": str(obj.get("thought", "")),
                "action": str(obj.get("action", "idle")),
            }
    except Exception:
        pass

    return {"thought": raw[:300] or "（空）", "action": "idle"}