# Jargon Gym

A tiny local web demo for memorizing Claude Code jargon with active recall and a five-box Leitner system.

## Run

```bash
uv run flask --app jargongym.app run --debug --port 5001
```

Open `http://127.0.0.1:5001`.

## Test

```bash
uv run python -m pytest -v
```

## Data

- Source glossary: `docs/claude-code-jargon-glossary.md`
- Local progress: `data/progress.json`

The app does not modify the source glossary.

