# Jargon Gym

English | [中文](README.md)

![Dogfooding comic in English](docs/assets/dogfooding-comic-en.png)

**A tiny, unserious local web app for memorizing very serious engineering jargon.**

Jargon Gym turns a Claude Code-style glossary into a flashcard trainer: active recall first, answer reveal second, then Leitner spaced repetition and instant rescue quizzes for the terms your brain rage-quits on.

If you have ever nodded confidently at `yak shaving`, `dogfooding`, `bus factor`, or `shadow traffic` while secretly thinking "I should know what that means by now", this is your training room.

## Project Positioning

Jargon Gym is a **local-first** learning tool: run it on your own machine, use it for yourself, and keep your progress locally. It is not designed as a production web service and does not require accounts.

This version is intentionally finished as an entertainment demo. The repo is public mainly so interested developers can fork it and keep playing with it, for example by turning it into a mobile, Mac, or desktop app.

## Interface Preview

![Jargon Gym interface screenshot](docs/assets/app-screenshot.png)

## Why

Engineering jargon can be useful, but it often sounds like a group chat that somehow got promoted to architecture review:

- `dogfooding`: using your own product first, and discovering the pain before users do.
- `yak shaving`: trying to do A, then needing B, C, D, and suddenly maintaining the toolchain's toolchain.
- `bikeshedding`: the big decision passes quickly; the tiny detail eats the meeting.
- `bus factor`: a project risk metric with surprisingly aggressive urban-planning energy.
- `footgun`: an API so sharp it files the incident report for you.
- `spaghetti code` / `lasagna code`: software architecture, now with carbs.
- `heisenbug`: a bug that disappears when observed, because debugging needed philosophy.
- `nuke`: the technical term for "delete it with confidence and maybe regret".

The project is deliberately lighthearted, but the learning loop is real:

1. Pick a jargon library.
2. Try to recall the meaning before seeing the answer.
3. Reveal the answer and rate your recall.
4. Forgotten or fuzzy cards enter an immediate multiple-choice quiz.
5. Correctly reinforced cards return later through a Leitner schedule.

## Features

- **Markdown-powered glossary**: the card deck is parsed from `docs/claude-code-jargon-glossary.md`.
- **Library selection**: study one category at a time, such as testing, debugging, deployment, or Claude Code/Git terms.
- **Active recall first**: answers are hidden until you choose to reveal them.
- **Direct rescue mode**: if a term is blank in your head, send it straight to a quiz.
- **Leitner spaced repetition**: cards move through five boxes based on recall quality.
- **Instant reinforcement quizzes**: `again` and `hard` cards become four-choice tests.
- **Local JSON memory system**: no database, no account, no cloud dependency; progress survives after the local server stops.
- **Light comic UI**: designed to feel like an office jargon gym, not a serious enterprise dashboard.

## Demo Flow

```text
Pick library
  -> Recall term
  -> Reveal answer
  -> Rate memory
  -> Quiz weak cards
  -> Repeat later
```

## Quick Start

This project uses `uv`.

```bash
uv run flask --app jargongym.app run --debug --port 5001
```

Open:

```text
http://127.0.0.1:5001
```

Run tests:

```bash
uv run python -m pytest -v
```

## Project Structure

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

## Data

- Source glossary: `docs/claude-code-jargon-glossary.md`
- Local progress: `data/progress.json`

The app does not modify the source glossary.

`data/progress.json` is the local memory system. It records each card's Leitner Box, next due time, review count, last grade, and last review time. Stopping the local server only stops the web process; it does not erase this file. When you start the app again, it continues from the previous learning state.

To start over, click the in-app reset button or delete `data/progress.json` manually. The file is ignored by `.gitignore`, so personal learning progress is not published to GitHub.

## Fork Ideas

This is not a promised roadmap. It is a list of ideas for other developers who want to fork the project and keep the joke alive:

- Package it as a mobile Web/PWA app, a Mac app, or a Windows/Linux desktop app.
- Build fuller clients with Tauri, Electron, PyInstaller, or native mobile stacks.
- Add typed-answer mode instead of only multiple choice.
- Add daily review limits and session summaries.
- Add import/export for custom company jargon.
- Add a meeting survival mode for the most cursed terms.
- Add a shareable progress card for social posting.

## License

MIT
