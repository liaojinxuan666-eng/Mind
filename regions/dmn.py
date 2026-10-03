import json
import hashlib
from collections import defaultdict


class DefaultModeNetwork:
    def __init__(self):
        self.narrative = []
        self.self_model = {"identity": "初生的脑子", "goals": []}
        self.promotion_log = []   # 历次固化的记录

    def reflect(self, recent_episodes):
        for ep in recent_episodes[:3]:
            self.narrative.append(f"我经历了：{ep[2]} → {ep[4]}")
        return self.narrative[-3:]

    def _signature_from_focus(self, focus_json):
        """从 episode 的 focus 字段重建签名，必须与基底核 _signature 一致"""
        try:
            items = json.loads(focus_json or "[]")
        except Exception:
            items = []
        key = "|".join(sorted(items))
        return hashlib.md5(key.encode()).hexdigest()[:12]

    def self_improve(self, hippocampus, basal_ganglia, min_repeat=3, min_success=0.8):
        """
        静息态自我改进：
        1. 回放近期情景
        2. 找出反复出现的 (情境, 动作) 组合
        3. 成功率够高就固化成基底核习惯
        返回本次固化的列表
        """
        episodes = hippocampus.replay(200)
        if len(episodes) < min_repeat:
            return []

        # 统计 (signature, action) 的出现与成功率
        # episode 格式: (id, ts, focus, goal, action, result, valence, salience)
        stats = defaultdict(list)
        for ep in episodes:
            sig = self._signature_from_focus(ep[2])
            action = ep[4]
            result = ep[5]
            stats[(sig, action)].append(result)

        promoted = []
        for (sig, action), results in stats.items():
            if len(results) < min_repeat:
                continue
            success = sum(1 for r in results if r and "空转" not in r) / len(results)
            if success < min_success:
                continue

            # 已固化过就不重复
            existing = basal_ganglia.habits.get(sig)
            if existing and existing["action"] == action and existing["confidence"] >= success:
                continue

            basal_ganglia.habits[sig] = {
                "action": action,
                "confidence": success,
                "count": len(results),
            }
            promoted.append({
                "signature": sig,
                "action": action,
                "success": round(success, 2),
                "samples": len(results),
            })
            self.promotion_log.append(promoted[-1])

        return promoted