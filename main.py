import time
import sys
from brain import Brain


def main():
    fast = "--fast" in sys.argv
    interval = 0.02 if fast else 1.0

    brain = Brain("Mind")
    print(f"🧠 {brain.name} 苏醒   (fast={fast})\n")

    brain.perceive("看到一段代码", salience=0.8)
    brain.perceive("想起昨天没解决的问题", salience=0.6)
    brain.perceive("肚子有点饿了", salience=0.4)

    try:
        while True:
            r = brain.tick()
            focus = r["focus"][:2]
            src = r["source"] or "?"
            ratio = (
                1 - r["cortex_calls"] / r["tick_count"]
                if r["tick_count"] else 0
            )
            print(
                f"[{r['clock']:04d}] "
                f"醒={r['wakefulness']:.2f} | "
                f"路径={src:6s} | "
                f"习惯数={r['habit_count']:2d} | "
                f"皮层={r['cortex_calls']}/{r['tick_count']} "
                f"(省 {ratio*100:.0f}%)"
            )
            for p in r.get("promoted", []):
                print(
                    f"   🌙 固化新习惯: "
                    f"sig={p['signature']} "
                    f"→ {p['action']} "
                    f"(成功 {p['success']}, 样本 {p['samples']})"
                )
            time.sleep(interval)
    except KeyboardInterrupt:
        print(
            f"\n🧠 脑子停了。"
            f"皮层总调用 {brain._cortex_calls} 次 / 总 {brain._tick_count} tick，"
            f"固化习惯 {len(brain.basal_ganglia.habits)} 个。"
        )


if __name__ == "__main__":
    main()