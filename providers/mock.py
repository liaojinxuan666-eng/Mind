from providers.base import CortexProvider, CortexResponse


class MockProvider(CortexProvider):
    name = "mock"

    def reason(self, context):
        focus = context.get("focus", [])
        goal = context.get("goal", "")
        if not focus:
            return CortexResponse("（静默）", "idle")
        return CortexResponse(
            thought=f"关于「{focus[0]}」，我在想：{goal or '继续观察'}",
            action="reflect" if goal else "explore",
        )