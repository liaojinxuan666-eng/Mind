import time
import sys
import random
from brain import Brain


SCENARIOS = [
    "看到一段代码",
    "想起昨天没解决的问题",
    "用户问了一个新问题",
    "编译报错",
    "测试通过了",
    "肚子有点饿了",
    "刷到一个新概念",
    "手头任务卡住了",
]


def main():
    fast = "--fast" in sys.argv
    interval = 0.02 if fast else 1.0
    inject_every = 30   # 每 N tick 注入一个新场景

    brain = Brain("Mind")
    print(f"🧠 {brain.name} 苏醒   provider={brain.neocortex.provider.name}")
    print(f"   入口：python3 main.py [--fast]\n")

    brain.perceive("看到一段代码", salience=0.8)
    brain.perceive("想起昨天没解决的问题", salience=0.6)

    try:
        while True:
            # 定期注入新场景，让焦点真的变化
            if brain.stem.clock % inject_every == 0 and brain.stem.clock > 0:
                brain.perceive(
                    random.choice(SCENARIOS),
                    salience=random.uniform(0.3, 0.9),
                )

            r = brain.tick()
            src = r["source"] or "?"
            ratio = (
                1 - r["cortex_calls"] / r["tick_count"]
                if r["tick_count"] else 0
            )

            line = (
                f"[{r['clock']:05d}] "
                f"醒={r['wakefulness']:.2f} | "
                f"路径={src:6s} | "
                f"习惯={r['habit_count']:2d} | "
                f"皮层={r['cortex_calls']:3d} | "
                f"本次tok={r['tick_tokens']:4d} | "
                f"累计tok={r['total_tokens']:6d} | "
                f"省={ratio*100:3.0f}%"
            )
            print(line)

            for p in r.get("promoted", []):
                print(
                    f"   🌙 固化: sig={p['signature']} "
                    f"→ {p['action']} "
                    f"(成功 {p['success']}, 样本 {p['samples']})"
                )

            if r.get("last_error"):
                print(f"   ⚠️  {r['last_error'][:120]}")

            time.sleep(interval)
    except KeyboardInterrupt:
        print(
            f"\n🧠 脑子停了。"
            f"皮层调用 {brain._cortex_calls} / {brain._tick_count} tick，"
            f"累计 token {brain.neocortex.total_tokens}，"
            f"固化习惯 {len(brain.basal_ganglia.habits)} 个。"
        )


if __name__ == "__main__":
    main()