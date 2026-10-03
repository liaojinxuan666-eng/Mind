import time
from state import Item, BrainState
from bus import WhiteMatter
from neuromod import Neuromodulators
from stem import Brainstem
from workspace import GlobalWorkspace
from regions.thalamus import Thalamus
from regions.neocortex import Neocortex
from regions.prefrontal import PrefrontalCortex
from regions.hippocampus import Hippocampus
from regions.entorhinal import EntorhinalCortex
from regions.amygdala import Amygdala
from regions.basal_ganglia import BasalGanglia
from regions.cerebellum import Cerebellum
from regions.hypothalamus import Hypothalamus
from regions.acc import AnteriorCingulate
from regions.insula import Insula
from regions.dmn import DefaultModeNetwork


class Brain:
    def __init__(self, name="Mind", db_path="mind.db"):
        self.name = name
        self.stem = Brainstem(hz=2)
        self.bus = WhiteMatter()
        self.neuromod = Neuromodulators()
        self.workspace = GlobalWorkspace()
        self.thalamus = Thalamus()
        self.neocortex = Neocortex()
        self.prefrontal = PrefrontalCortex()
        self.hippocampus = Hippocampus(db_path=db_path)
        self.entorhinal = EntorhinalCortex()
        self.amygdala = Amygdala()
        self.basal_ganglia = BasalGanglia()
        self.cerebellum = Cerebellum()
        self.hypothalamus = Hypothalamus()
        self.acc = AnteriorCingulate()
        self.insula = Insula()
        self.dmn = DefaultModeNetwork()
        self.state = BrainState()
        self.sensory_queue = []

        # 统计
        self._cortex_calls = 0
        self._tick_count = 0
        self._last_focus = set()

    def perceive(self, content, salience=0.5):
        self.sensory_queue.append(
            Item(id=str(time.time()), content=content, salience=salience)
        )

    def _execute(self, action):
        if action == "idle":
            return "空转"
        return f"执行了 {action}"

    def _cortex_needed(self, workspace, conflict, novelty=0.0):
        """判断是否需要唤醒皮层（LLM）"""
        if not workspace.spotlight:
            return False
        if conflict > 0.5:
            return True
        if novelty > 0.7:
            return True
        current = {i.content for i in workspace.spotlight}
        if current - self._last_focus:
            self._last_focus = current
            return True
        self._last_focus = current
        return False

    def tick(self):
        wakefulness = self.stem.tick()
        self.state.clock = self.stem.clock
        self.state.wakefulness = wakefulness

        # 丘脑门控
        gated = self.thalamus.gate(
            self.sensory_queue, self.prefrontal.current_goal()
        )
        self.sensory_queue = []

        # 全局工作空间
        self.workspace.bind(
            gated,
            self.prefrontal.snapshot(),
            self.prefrontal.current_goal(),
        )

        # 情绪价
        valence = self.amygdala.appraise(self.workspace)

        # 候选动作 + 冲突监测
        candidates = self.basal_ganglia.propose(self.workspace)
        conflict = self.acc.monitor(candidates, abs(valence))

        # 暂用情绪强度当新奇度
        novelty = abs(valence)

        # ===== 三级处理：习惯 → 回忆 → 皮层 =====
        thought = None
        source = None
        tick_tokens = 0

        # 1. 基底核习惯
        habit_action = self.basal_ganglia.try_habit(self.workspace)
        if habit_action:
            thought = {"thought": f"（习惯）{habit_action}", "action": habit_action}
            source = "habit"

        # 2. 海马体回忆
        if thought is None and self.workspace.spotlight:
            cue = self.workspace.spotlight[0].content
            recalled = self.hippocampus.recall_first(cue)
            if recalled:
                thought = {"thought": f"（回忆）{recalled}", "action": "recall"}
                source = "recall"

        # 3. 判断是否唤醒皮层
        if thought is None:
            if self._cortex_needed(self.workspace, conflict, novelty):
                thought = self.neocortex.reason(self.workspace.compile())
                source = "cortex"
                self._cortex_calls += 1
                tick_tokens = thought.get("tokens", 0)
            else:
                thought = {"thought": "（自动）维持现状", "action": "idle"}
                source = "auto"

        self._tick_count += 1

        # 时序预测
        self.cerebellum.predict(thought.get("action"))

        # 动作选择
        chosen = self.basal_ganglia.select(
            candidates, exploration=self.neuromod.dopamine
        )
        action = chosen["action"] if chosen else "idle"
        result = self._execute(action)

        # 小脑校正
        actual = 1.0 if result and result != "空转" else 0.0
        error = self.cerebellum.correct(actual)

        # 神经调质更新
        self.neuromod.update(
            td_error=error, novelty=0.1, threat=max(0.0, -valence)
        )
        self.state.neuromod = self.neuromod.broadcast()

        # 强化习惯
        reward = 1.0 if error > 0 else -0.5
        self.basal_ganglia.reinforce_habit(self.workspace, action, reward)

        # 海马体编码
        if self.workspace.spotlight:
            self.hippocampus.encode(
                self.workspace,
                action,
                result,
                valence,
                sum(i.salience for i in self.workspace.spotlight),
            )

        # 工作记忆：先衰减，再维持
        self.prefrontal.decay_all(rate=0.05)
        self.prefrontal.maintain(self.workspace.spotlight)

        # 内驱力
        self.hypothalamus.update(self.stem.clock)
        self.state.drives = dict(self.hypothalamus.drives)

        # 静息态：反思 + 自我改进
        promoted = []
        if wakefulness < 0.3:
            self.dmn.reflect(self.hippocampus.replay(10))
            promoted = self.dmn.self_improve(
                self.hippocampus, self.basal_ganglia
            )

        # 内感受
        self.insula.sense(self.state)

        return {
            "clock": self.state.clock,
            "wakefulness": wakefulness,
            "focus": [i.content for i in self.workspace.spotlight],
            "thought": thought,
            "action": action,
            "result": result,
            "valence": valence,
            "conflict": conflict,
            "dopamine": self.neuromod.dopamine,
            "source": source,
            "cortex_calls": self._cortex_calls,
            "tick_count": self._tick_count,
            "promoted": promoted,
            "habit_count": len(self.basal_ganglia.habits),
            "tick_tokens": tick_tokens,
            "total_tokens": self.neocortex.total_tokens,
            "provider": self.neocortex.provider.name,
            "last_error": self.neocortex.last_error,
        }