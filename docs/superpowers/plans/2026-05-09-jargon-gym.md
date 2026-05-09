# Jargon Gym Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a local Flask demo that turns the existing Claude Code jargon glossary into a Leitner flashcard trainer.

**Architecture:** The app parses the Markdown glossary at startup, stores only review progress in JSON, and renders a single study page. Core behavior is isolated in parser, scheduler, and store modules so tests can cover the learning logic without a browser.

**Tech Stack:** Python 3.9+, uv, Flask, pytest.

---

### Task 1: Project Skeleton and Parser

**Files:**
- Create: `pyproject.toml`
- Create: `jargongym/__init__.py`
- Create: `jargongym/cards.py`
- Test: `tests/test_cards.py`

- [ ] **Step 1: Write parser tests**

```python
from pathlib import Path

from jargongym.cards import parse_glossary


def test_parse_glossary_extracts_heading_answer_and_category(tmp_path: Path):
    source = tmp_path / "glossary.md"
    source.write_text(
        "# Title\n\n"
        "## 一、测试与质量\n\n"
        "### smoke test —— 冒烟测试\n\n"
        "- **字面**：只检查会不会冒烟。\n"
        "- **含义**：浅层检查。\n\n"
        "### regression test —— 回归测试\n\n"
        "- **含义**：确认旧功能没坏。\n",
        encoding="utf-8",
    )

    cards = parse_glossary(source)

    assert [card.term for card in cards] == ["smoke test", "regression test"]
    assert cards[0].translation == "冒烟测试"
    assert cards[0].category == "一、测试与质量"
    assert "浅层检查" in cards[0].answer_markdown
    assert cards[0].id == "smoke-test"
```

- [ ] **Step 2: Run parser test to verify it fails**

Run: `uv run python -m pytest tests/test_cards.py -v`
Expected: FAIL because `jargongym.cards` does not exist.

- [ ] **Step 3: Implement parser**

Create a `Card` dataclass and parse `##` categories plus `### term —— translation` sections into cards with stable slug IDs.

- [ ] **Step 4: Run parser test to verify it passes**

Run: `uv run python -m pytest tests/test_cards.py -v`
Expected: PASS.

### Task 2: Leitner Scheduler

**Files:**
- Create: `jargongym/leitner.py`
- Test: `tests/test_leitner.py`

- [ ] **Step 1: Write scheduler tests**

```python
from datetime import datetime, timezone

from jargongym.leitner import review_card


def test_good_grade_moves_card_up_one_box():
    now = datetime(2026, 5, 9, 8, 0, tzinfo=timezone.utc)
    state = {"box": 1, "reviews": 0}

    updated = review_card(state, "good", now)

    assert updated["box"] == 2
    assert updated["reviews"] == 1
    assert updated["last_grade"] == "good"
    assert updated["due"] == "2026-05-10T08:00:00+00:00"


def test_again_grade_resets_to_box_one_due_now():
    now = datetime(2026, 5, 9, 8, 0, tzinfo=timezone.utc)
    state = {"box": 4, "reviews": 3}

    updated = review_card(state, "again", now)

    assert updated["box"] == 1
    assert updated["due"] == "2026-05-09T08:00:00+00:00"
```

- [ ] **Step 2: Run scheduler test to verify it fails**

Run: `uv run python -m pytest tests/test_leitner.py -v`
Expected: FAIL because `jargongym.leitner` does not exist.

- [ ] **Step 3: Implement scheduler**

Implement box transitions, interval calculation, due-card filtering, and overdue sorting.

- [ ] **Step 4: Run scheduler test to verify it passes**

Run: `uv run python -m pytest tests/test_leitner.py -v`
Expected: PASS.

### Task 3: JSON Store and Flask UI

**Files:**
- Create: `jargongym/store.py`
- Create: `jargongym/app.py`
- Create: `templates/index.html`
- Create: `static/styles.css`
- Test: `tests/test_app.py`

- [ ] **Step 1: Write route smoke test**

```python
from pathlib import Path

from jargongym.app import create_app


def test_homepage_renders_a_card(tmp_path: Path):
    glossary = tmp_path / "glossary.md"
    glossary.write_text(
        "## 一、测试与质量\n\n"
        "### smoke test —— 冒烟测试\n\n"
        "- **含义**：浅层检查。\n",
        encoding="utf-8",
    )
    progress = tmp_path / "progress.json"
    app = create_app(glossary_path=glossary, progress_path=progress)

    response = app.test_client().get("/")

    assert response.status_code == 200
    assert "smoke test" in response.get_data(as_text=True)
```

- [ ] **Step 2: Run route test to verify it fails**

Run: `uv run python -m pytest tests/test_app.py -v`
Expected: FAIL because `create_app` is missing.

- [ ] **Step 3: Implement Flask app and templates**

Implement `GET /`, `POST /review/<card_id>`, and `POST /reset`. Render a revealable answer panel and grading buttons.

- [ ] **Step 4: Run route test to verify it passes**

Run: `uv run python -m pytest tests/test_app.py -v`
Expected: PASS.

### Task 4: Full Verification and Demo Server

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Run all tests**

Run: `uv run python -m pytest -v`
Expected: all tests pass.

- [ ] **Step 2: Start the demo server**

Run: `uv run flask --app jargongym.app run --debug --port 5001`
Expected: local server listens on `http://127.0.0.1:5001`.
