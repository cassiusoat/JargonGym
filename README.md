# Jargon Gym 黑话健身房

![Jargon Gym hero](docs/assets/readme-hero.svg)

**一个不太严肃、但真的能帮你背工程黑话的本地网页应用。**  
**A tiny, unserious local web app for memorizing very serious engineering jargon.**

Jargon Gym 会把 Claude Code 风格的黑话词典变成一个背诵训练器：先主动回忆，再揭晓答案，再用 Leitner 间隔重复和即时小测把“刚刚还会、转头就忘”的词重新捞回来。

Jargon Gym turns a Claude Code-style glossary into a flashcard trainer: active recall first, answer reveal second, then Leitner spaced repetition and instant rescue quizzes for the terms your brain rage-quits on.

如果你曾经在别人说 `yak shaving`、`dogfooding`、`bus factor`、`shadow traffic` 的时候认真点头，但心里想的是“我是不是应该早就知道这个词是什么意思”，那这里就是你的黑话训练台。

If you have ever nodded confidently at `yak shaving`, `dogfooding`, `bus factor`, or `shadow traffic` while secretly thinking "I should know what that means by now", this is your training room.

## 为什么做这个 / Why

工程黑话有时真的有用，但它们听起来也很像一个群聊被强行晋升成了架构评审：

Engineering jargon can be useful, but it often sounds like a group chat that somehow got promoted to architecture review:

- `dogfooding` / 吃自家狗粮：不是宠物食品测评，而是团队自己先用自家产品，先被自己产品咬一口，再发现痛点。
- `yak shaving` / 剃牦牛：你只是想合并一个 PR，结果先修工具链，再修工具链的工具链。
- `bikeshedding` / 自行车棚效应：没人质疑反应堆设计，大家为自行车棚颜色吵到天亮。
- `bus factor` / 公交车系数：一个项目风险指标，但语气像城市交通事故模拟器。
- `footgun` / 坑脚枪：一个 API 贴心到会帮你自己开事故单。
- `spaghetti code` / `lasagna code`：软件架构，主打碳水化合物。
- `heisenbug` / 海森堡 bug：你一看它就消失，调试从此带上哲学意味。
- `nuke` / 核平：技术语境里的“删了吧，先自信，后后悔”。

English notes:

- `dogfooding`: using your own product first, and discovering the pain before users do.
- `yak shaving`: trying to do A, then needing B, C, D, and suddenly maintaining the toolchain's toolchain.
- `bikeshedding`: the big decision passes quickly; the tiny detail eats the meeting.
- `bus factor`: a project risk metric with surprisingly aggressive urban-planning energy.
- `footgun`: an API so sharp it files the incident report for you.
- `spaghetti code` / `lasagna code`: software architecture, now with carbs.
- `heisenbug`: a bug that disappears when observed, because debugging needed philosophy.
- `nuke`: the technical term for "delete it with confidence and maybe regret".

这个项目的气质是轻松搞笑的，但背诵流程是认真设计过的：

The project is deliberately lighthearted, but the learning loop is real:

1. 选择一个黑话词库。  
   Pick a jargon library.
2. 先看题面，尝试主动回忆。  
   Try to recall the meaning before seeing the answer.
3. 揭晓答案，并给自己的回忆质量打分。  
   Reveal the answer and rate your recall.
4. 忘记或模糊的卡片进入即时四选一小测。  
   Forgotten or fuzzy cards enter an immediate multiple-choice quiz.
5. 通过小测强化后的卡片，再按 Leitner 间隔重复安排复习。  
   Correctly reinforced cards return later through a Leitner schedule.

## 功能 / Features

- **Markdown 词典驱动**：题库从 `docs/claude-code-jargon-glossary.md` 自动解析。  
  **Markdown-powered glossary**: the card deck is parsed from `docs/claude-code-jargon-glossary.md`.
- **词库选择**：可以只背测试、调试、部署、Claude Code/Git 等某一类黑话。  
  **Library selection**: study one category at a time, such as testing, debugging, deployment, or Claude Code/Git terms.
- **主动回忆优先**：答案默认遮盖，不先偷看。  
  **Active recall first**: answers are hidden until you choose to reveal them.
- **救援模式**：完全想不起来时，可以直接进入小测。  
  **Direct rescue mode**: if a term is blank in your head, send it straight to a quiz.
- **Leitner 间隔重复**：根据记忆质量推进五箱制复习。  
  **Leitner spaced repetition**: cards move through five boxes based on recall quality.
- **即时强化小测**：`完全忘了` 和 `有点眼熟` 的卡片会进入四选一测试。  
  **Instant reinforcement quizzes**: `again` and `hard` cards become four-choice tests.
- **本地 JSON 进度**：不用数据库、不用账号、不依赖云端。  
  **Local JSON progress**: no database, no account, no cloud dependency.
- **浅色搞笑 UI**：更像办公室黑话健身房，而不是严肃企业后台。  
  **Light comic UI**: designed to feel like an office jargon gym, not a serious enterprise dashboard.

## 学习流程 / Demo Flow

```text
选择词库 Pick library
  -> 主动回忆 Recall term
  -> 揭晓答案 Reveal answer
  -> 评价记忆 Rate memory
  -> 弱项小测 Quiz weak cards
  -> 间隔复习 Repeat later
```

## 快速开始 / Quick Start

本项目使用 `uv`。  
This project uses `uv`.

```bash
uv run flask --app jargongym.app run --debug --port 5001
```

打开 / Open:

```text
http://127.0.0.1:5001
```

运行测试 / Run tests:

```bash
uv run python -m pytest -v
```

## 项目结构 / Project Structure

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

## 数据 / Data

- 原始词典 / Source glossary: `docs/claude-code-jargon-glossary.md`
- 本地进度 / Local progress: `data/progress.json`

应用不会修改原始词典。  
The app does not modify the source glossary.

## 路线图 / Roadmap Ideas

- 增加拼写/输入答案模式，而不只是四选一。  
  Add typed-answer mode instead of only multiple choice.
- 增加每日复习上限和学习总结。  
  Add daily review limits and session summaries.
- 支持导入/导出自定义公司黑话。  
  Add import/export for custom company jargon.
- 增加“会议求生模式”，专练最容易在会上听懵的词。  
  Add a meeting survival mode for the most cursed terms.
- 生成可分享的学习进度卡片。  
  Add a shareable progress card for social posting.

## 许可证 / License

MIT

