from __future__ import annotations

from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from flask import Flask, abort, redirect, render_template, request, url_for

from jargongym.cards import Card, parse_glossary
from jargongym.leitner import VALID_GRADES, due_cards, review_card
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

    @app.get("/")
    def index() -> str:
        cards = _load_cards(app)
        progress = load_progress(app.config["PROGRESS_PATH"])
        now = datetime.now(timezone.utc)
        due = due_cards(cards, progress, now)
        current = due[0] if due else None
        stats = _stats(cards, progress, len(due))

        return render_template(
            "index.html",
            card=current,
            card_state=progress.get(current.id, {}) if current else {},
            stats=stats,
        )

    @app.post("/review/<card_id>")
    def review(card_id: str):
        grade = request.form.get("grade", "")
        if grade not in VALID_GRADES:
            abort(400, "unknown review grade")

        cards = _load_cards(app)
        card_ids = {card.id for card in cards}
        if card_id not in card_ids:
            abort(404, "unknown card")

        progress_path = app.config["PROGRESS_PATH"]
        progress = load_progress(progress_path)
        progress[card_id] = review_card(progress.get(card_id), grade)
        save_progress(progress_path, progress)
        return redirect(url_for("index"))

    @app.post("/reset")
    def reset():
        reset_progress(app.config["PROGRESS_PATH"])
        return redirect(url_for("index"))

    return app


def _load_cards(app: Flask) -> list[Card]:
    return parse_glossary(app.config["GLOSSARY_PATH"])


def _stats(cards: list[Card], progress: dict[str, dict[str, Any]], due_count: int) -> dict[str, int]:
    learned = sum(1 for state in progress.values() if int(state.get("box", 1)) >= 5)
    reviewed = sum(1 for card in cards if card.id in progress)
    return {
        "total": len(cards),
        "due": due_count,
        "reviewed": reviewed,
        "learned": learned,
    }


def card_to_dict(card: Card) -> dict[str, Any]:
    return asdict(card)


app = create_app()

