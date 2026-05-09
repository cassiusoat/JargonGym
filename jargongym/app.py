from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from flask import Flask, abort, redirect, render_template, request, url_for
import markdown as markdown_lib
from markupsafe import Markup

from jargongym.cards import Card, parse_glossary
from jargongym.leitner import VALID_GRADES, due_cards, review_card
from jargongym.quiz import build_choice_quiz
from jargongym.store import load_progress, reset_progress, save_progress


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_GLOSSARY = PROJECT_ROOT / "docs" / "claude-code-jargon-glossary.md"
DEFAULT_PROGRESS = PROJECT_ROOT / "data" / "progress.json"


def create_app(
    glossary_path: Path = DEFAULT_GLOSSARY,
    progress_path: Path = DEFAULT_PROGRESS,
) -> Flask:
    app = Flask(
        __name__,
        template_folder=str(PROJECT_ROOT / "templates"),
        static_folder=str(PROJECT_ROOT / "static"),
    )
    app.config["GLOSSARY_PATH"] = Path(glossary_path)
    app.config["PROGRESS_PATH"] = Path(progress_path)
    app.add_template_filter(_render_inline_markdown, "inline_markdown")

    @app.get("/")
    def index() -> str:
        cards = _load_cards(app)
        selected_category = request.args.get("category", "")
        scoped_cards = _filter_cards(cards, selected_category)
        progress = load_progress(app.config["PROGRESS_PATH"])
        now = datetime.now(timezone.utc)
        due = due_cards(scoped_cards, progress, now)
        current = due[0] if due else None
        pending_quiz = _pending_quiz_cards(scoped_cards, progress)
        stats = _stats(scoped_cards, progress, len(due), len(pending_quiz))

        return render_template(
            "index.html",
            card=current,
            card_state=progress.get(current.id, {}) if current else {},
            answer_html=_render_markdown(current.answer_markdown) if current else Markup(""),
            stats=stats,
            categories=_categories(cards),
            selected_category=selected_category,
            pending_quiz_card=pending_quiz[0] if pending_quiz else None,
        )

    @app.post("/review/<card_id>")
    def review(card_id: str):
        grade = request.form.get("grade", "")
        selected_category = request.form.get("category", "")
        if grade not in VALID_GRADES:
            abort(400, "unknown review grade")

        cards = _load_cards(app)
        card = _find_card(cards, card_id)

        progress_path = app.config["PROGRESS_PATH"]
        progress = load_progress(progress_path)
        previous = progress.get(card_id, {})
        updated = review_card(previous, grade)
        updated["category"] = card.category
        updated["needs_quiz"] = grade in {"again", "hard"}
        updated["lapses"] = int(previous.get("lapses", 0)) + (1 if grade == "again" else 0)
        updated["quiz_correct"] = int(previous.get("quiz_correct", 0))
        updated["quiz_wrong"] = int(previous.get("quiz_wrong", 0))
        progress[card_id] = updated
        save_progress(progress_path, progress)
        if updated["needs_quiz"]:
            return redirect(url_for("quiz", card_id=card_id, category=selected_category))
        return _redirect_to_index(selected_category)

    @app.get("/quiz/<card_id>")
    def quiz(card_id: str) -> str:
        selected_category = request.args.get("category", "")
        cards = _load_cards(app)
        card = _find_card(cards, card_id)
        scoped_cards = _filter_cards(cards, selected_category)
        choice_quiz = build_choice_quiz(card, scoped_cards, cards)
        return render_template(
            "quiz.html",
            quiz=choice_quiz,
            answer_html=_render_markdown(card.answer_markdown),
            selected_category=selected_category,
            feedback=None,
            selected_choice=None,
        )

    @app.post("/quiz/<card_id>")
    def submit_quiz(card_id: str):
        selected_category = request.form.get("category", "")
        choice = request.form.get("choice", "")
        cards = _load_cards(app)
        card = _find_card(cards, card_id)
        scoped_cards = _filter_cards(cards, selected_category)
        choice_quiz = build_choice_quiz(card, scoped_cards, cards)
        progress_path = app.config["PROGRESS_PATH"]
        progress = load_progress(progress_path)
        state = dict(progress.get(card_id, {"box": 1}))

        if choice == choice_quiz.answer:
            state["needs_quiz"] = False
            state["quiz_correct"] = int(state.get("quiz_correct", 0)) + 1
            if _is_due_now(state):
                state["due"] = (datetime.now(timezone.utc) + timedelta(minutes=20)).isoformat()
            progress[card_id] = state
            save_progress(progress_path, progress)
            return _redirect_to_index(selected_category)

        state["needs_quiz"] = True
        state["quiz_wrong"] = int(state.get("quiz_wrong", 0)) + 1
        progress[card_id] = state
        save_progress(progress_path, progress)
        return render_template(
            "quiz.html",
            quiz=choice_quiz,
            answer_html=_render_markdown(card.answer_markdown),
            selected_category=selected_category,
            feedback="还差一点：这张卡继续留在强化训练里。",
            selected_choice=choice,
        )

    @app.post("/reset")
    def reset():
        reset_progress(app.config["PROGRESS_PATH"])
        return redirect(url_for("index"))

    return app


def _load_cards(app: Flask) -> list[Card]:
    return parse_glossary(app.config["GLOSSARY_PATH"])


def _stats(
    cards: list[Card],
    progress: dict[str, dict[str, Any]],
    due_count: int,
    quiz_count: int,
) -> dict[str, int]:
    learned = sum(1 for card in cards if int(progress.get(card.id, {}).get("box", 1)) >= 5)
    reviewed = sum(1 for card in cards if card.id in progress)
    return {
        "total": len(cards),
        "due": due_count,
        "reviewed": reviewed,
        "learned": learned,
        "quiz": quiz_count,
    }


def _categories(cards: list[Card]) -> list[str]:
    seen: set[str] = set()
    values: list[str] = []
    for card in cards:
        if card.category not in seen:
            seen.add(card.category)
            values.append(card.category)
    return values


def _filter_cards(cards: list[Card], selected_category: str) -> list[Card]:
    if not selected_category:
        return cards
    filtered = [card for card in cards if card.category == selected_category]
    return filtered


def _pending_quiz_cards(cards: list[Card], progress: dict[str, dict[str, Any]]) -> list[Card]:
    return [card for card in cards if progress.get(card.id, {}).get("needs_quiz") is True]


def _find_card(cards: list[Card], card_id: str) -> Card:
    for card in cards:
        if card.id == card_id:
            return card
    abort(404, "unknown card")


def _redirect_to_index(selected_category: str):
    if selected_category:
        return redirect(url_for("index", category=selected_category))
    return redirect(url_for("index"))


def _is_due_now(state: dict[str, Any]) -> bool:
    due = state.get("due")
    if not due:
        return True
    return datetime.fromisoformat(str(due)) <= datetime.now(timezone.utc)


def _render_markdown(markdown_text: str) -> Markup:
    html = markdown_lib.markdown(
        markdown_text,
        extensions=["extra", "sane_lists"],
        output_format="html",
    )
    return Markup(html)


def _render_inline_markdown(markdown_text: str) -> Markup:
    html = markdown_lib.markdown(
        markdown_text,
        extensions=["extra", "sane_lists"],
        output_format="html",
    ).strip()
    if html.startswith("<p>") and html.endswith("</p>"):
        html = html[3:-4]
    return Markup(html)


def card_to_dict(card: Card) -> dict[str, Any]:
    return asdict(card)


app = create_app()
