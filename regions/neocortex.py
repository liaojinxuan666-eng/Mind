import random

class Neocortex:
    """LLM 接口。先用 mock，之后替换 model_fn 即可接任意模型。"""
    def __init__(self, model_fn=None):
        self.model_fn = model_fn or self._mock
        self.temperature = 0.7

    def reason(self, ctx):
        return self.model_fn(ctx)

    def _mock(self, ctx):
        focus = ctx.get("focus", [])
        goal = ctx.get("goal", "")
        if not focus:
            return {"thought": "（静默）", "action": "idle"}
        return {
            "thought": f"关于「{focus[0]}」，我在想：{goal or '继续观察'}",
            "action": "reflect" if goal else "explore",
        }