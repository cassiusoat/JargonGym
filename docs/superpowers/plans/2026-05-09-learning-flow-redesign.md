# Learning Flow Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the linear flashcard demo flow with category selection and immediate quiz reinforcement while preserving the existing light, funny UI style.

**Architecture:** Keep Markdown parsing and Leitner scheduling as separate modules. Add a small quiz module for deterministic four-choice tests, and extend Flask routes so category filters and quiz state are carried through review actions.

**Tech Stack:** Python 3.9+, uv, Flask, Markdown, pytest.

---

### Task 1: Category-Scoped Study

**Files:**
- Modify: `tests/test_app.py`
- Modify: `jargongym/app.py`
- Modify: `templates/index.html`

- [ ] Add a failing route test for `/?category=<name>` showing only cards from that category.
- [ ] Implement category extraction, selected-category filtering, and category selector links.
- [ ] Run `uv run python -m pytest tests/test_app.py -v`.

### Task 2: Immediate Reinforcement State

**Files:**
- Modify: `tests/test_app.py`
- Modify: `jargongym/app.py`
- Modify: `templates/index.html`

- [ ] Add a failing test that posting `again` redirects to `/quiz/<card_id>` and stores `needs_quiz: true`.
- [ ] Preserve the selected category through hidden form fields.
- [ ] Add a direct pre-reveal forgotten button.
- [ ] Run `uv run python -m pytest tests/test_app.py -v`.

### Task 3: Four-Choice Quiz

**Files:**
- Create: `jargongym/quiz.py`
- Create: `templates/quiz.html`
- Modify: `tests/test_app.py`
- Modify: `jargongym/app.py`
- Modify: `static/styles.css`

- [ ] Add failing tests for quiz rendering, wrong-answer feedback, and correct-answer clearing.
- [ ] Implement deterministic answer-option construction.
- [ ] Add GET/POST quiz routes with instant feedback.
- [ ] Style the quiz using the existing light palette.
- [ ] Run `uv run python -m pytest -v`.

