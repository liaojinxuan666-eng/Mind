import time
from .state import Item, BrainState
from .bus import WhiteMatter
from .neuromod import Neuromodulators
from .stem import Brainstem
from .workspace import GlobalWorkspace
from .regions.thalamus import Thalamus
from .regions.neocortex import Neocortex
from .regions.prefrontal import PrefrontalCortex
from .regions.hippocampus import Hippocampus
from .regions.entorhinal import EntorhinalCortex
from .regions.amygdala import Amygdala
from .regions.basal_ganglia import BasalGanglia
from .regions.cerebellum import Cerebellum
from .regions.hypothalamus import Hypothalamus
from .regions.acc import AnteriorCingulate
from .regions.insula import Insula
from .regions.dmn import DefaultModeNetwork

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

    def perceive(self, content, salience=0.5):
        self.sensory_queue.append(
            Item(id=str(time.time()), content=content, salience=salience)
        )

    def _execute(self, action):
        if action == "idle":
            return "空转"
        return f"执行了 {action}"

    def tick(self):
        wakefulness = self.stem.tick()
        self.state.clock = self.stem.clock
        self.state.wakefulness = wakefulness

        # 丘脑门控
        gated = self.thalamus.gate(self.sensory_queue, self.prefrontal.current_goal())
        self.sensory_queue = []

        # 全局工作空间
        self.workspace.bind(gated, list(self.prefrontal.working_memory),
                            self.prefrontal.current_goal())

        # 皮层推理
        thought = self.neocortex.reason(self.workspace.compile())

        # 情绪评估
        valence = self.amygdala.appraise(self.workspace)

        # 候选动作 + 时序预测
        candidates = self.basal_ganglia.propose(self.workspace)
        self.cerebellum.predict(thought.get("action"))

        # 冲突监测
        conflict = self.acc.monitor(candidates, abs(valence))

        # 动作选择
        chosen = self.basal_ganglia.select(candidates, exploration=self.neuromod.dopamine)
        action = chosen["action"] if chosen else "idle"
        result = self._execute(action)

        # 小脑校正
        actual = 1.0 if result and result != "空转" else 0.0
        error = self.cerebellum.correct(actual)

        # 神经调质更新
        self.neuromod.update(td_error=error, novelty=0.1, threat=max(0.0, -valence))
        self.state.neuromod = self.neuromod.broadcast()

        # 海马体编码
        if self.workspace.spotlight:
            self.hippocampus.encode(
                self.workspace, action, result, valence,
                sum(i.salience for i in self.workspace.spotlight),
            )

        # 前额叶维持
        self.prefrontal.maintain(self.workspace.spotlight)

        # 内驱力
        self.hypothalamus.update(self.stem.clock)
        self.state.drives = dict(self.hypothalamus.drives)

        # 静息态
        if wakefulness < 0.3:
            self.dmn.reflect(self.hippocampus.replay(10))

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
        }