import time
from brain import Brain


def main():
    brain = Brain("Mind")
    print(f"🧠 {brain.name} 苏醒\n")

    brain.perceive("看到一段代码", salience=0.8)
    brain.perceive("想起昨天没解决的问题", salience=0.6)
    brain.perceive("肚子有点饿了", salience=0.4)

    try:
        while True:
            r = brain.tick()
            focus = r["focus"][:2]
            thought = r["thought"]["thought"][:28]
            print(
                f"[{r['clock']:04d}] "
                f"醒={r['wakefulness']:.2f} | "
                f"焦点={focus} | "
                f"想={thought} | "
                f"做={r['action']} | "
                f"多巴胺={r['dopamine']:.2f}"
            )
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n🧠 脑子停了")


if __name__ == "__main__":
    main()