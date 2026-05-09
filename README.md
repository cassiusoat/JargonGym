# Jargon Gym 黑话健身房

[English](README.en.md) | 中文

![Dogfooding comic in Chinese](docs/assets/dogfooding-comic-zh.png)

**一个不太严肃、但真的能帮你背工程黑话的本地网页应用。**

Jargon Gym 会把 Claude Code 风格的黑话词典变成一个背诵训练器：先主动回忆，再揭晓答案，再用 Leitner 间隔重复和即时小测把“刚刚还会、转头就忘”的词重新捞回来。

如果你曾经在别人说 `yak shaving`、`dogfooding`、`bus factor`、`shadow traffic` 的时候认真点头，但心里想的是“我是不是应该早就知道这个词是什么意思”，那这里就是你的黑话训练台。

## 为什么做这个

工程黑话有时真的有用，但它们听起来也很像一个群聊被强行晋升成了架构评审：

- `dogfooding` / 吃自家狗粮：不是宠物食品测评，而是团队自己先用自家产品，先被自己产品咬一口，再发现痛点。
- `yak shaving` / 剃牦牛：你只是想合并一个 PR，结果先修工具链，再修工具链的工具链。
- `bikeshedding` / 自行车棚效应：没人质疑反应堆设计，大家为自行车棚颜色吵到天亮。
- `bus factor` / 公交车系数：一个项目风险指标，但语气像城市交通事故模拟器。
- `footgun` / 坑脚枪：一个 API 贴心到会帮你自己开事故单。
- `spaghetti code` / `lasagna code`：软件架构，主打碳水化合物。
- `heisenbug` / 海森堡 bug：你一看它就消失，调试从此带上哲学意味。
- `nuke` / 核平：技术语境里的“删了吧，先自信，后后悔”。

这个项目的气质是轻松搞笑的，但背诵流程是认真设计过的：

1. 选择一个黑话词库。
2. 先看题面，尝试主动回忆。
3. 揭晓答案，并给自己的回忆质量打分。
4. 忘记或模糊的卡片进入即时四选一小测。
5. 通过小测强化后的卡片，再按 Leitner 间隔重复安排复习。

## 功能

- **Markdown 词典驱动**：题库从 `docs/claude-code-jargon-glossary.md` 自动解析。
- **词库选择**：可以只背测试、调试、部署、Claude Code/Git 等某一类黑话。
- **主动回忆优先**：答案默认遮盖，不先偷看。
- **救援模式**：完全想不起来时，可以直接进入小测。
- **Leitner 间隔重复**：根据记忆质量推进五箱制复习。
- **即时强化小测**：`完全忘了` 和 `有点眼熟` 的卡片会进入四选一测试。
- **本地 JSON 进度**：不用数据库、不用账号、不依赖云端。
- **浅色搞笑 UI**：更像办公室黑话健身房，而不是严肃企业后台。

## 学习流程

```text
选择词库
  -> 主动回忆
  -> 揭晓答案
  -> 评价记忆
  -> 弱项小测
  -> 间隔复习
```

## 快速开始

本项目使用 `uv`。

```bash
uv run flask --app jargongym.app run --debug --port 5001
```

打开：

```text
http://127.0.0.1:5001
```

运行测试：

```bash
uv run python -m pytest -v
```

## 项目结构

```text
jargongym/
  app.py       # Flask routes and page flow
  cards.py     # Markdown glossary parser
  leitner.py   # spaced repetition logic
  quiz.py      # four-choice reinforcement quiz
  store.py     # local JSON progress store

docs/
  claude-code-jargon-glossary.md

templates/
  index.html
  quiz.html

static/
  styles.css
```

## 数据

- 原始词典：`docs/claude-code-jargon-glossary.md`
- 本地进度：`data/progress.json`

应用不会修改原始词典。

## 路线图

- 增加拼写/输入答案模式，而不只是四选一。
- 增加每日复习上限和学习总结。
- 支持导入/导出自定义公司黑话。
- 增加“会议求生模式”，专练最容易在会上听懵的词。
- 生成可分享的学习进度卡片。

## 许可证

MIT

