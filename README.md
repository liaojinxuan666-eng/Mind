# Mind

一个按脑区结构组织的"人工脑"。

思考交给大模型（新皮层），记忆、注意、情绪、选择、巩固、内驱力由本项目实现。

## 运行

    python3 main.py

零依赖，clone 即可跑。

## 结构

- `main.py`          入口
- `brain.py`         脑子本体，主循环
- `stem.py`          脑干，心跳节律
- `workspace.py`     全局工作空间（意识）
- `neuromod.py`      神经调质
- `bus.py`           白质，消息总线
- `regions/`         各脑区

## 规范

- 所有 import 使用绝对路径，不用 `from .xxx`
- clone 后直接 `python3 main.py`，无需任何额外操作

## 许可

MIT