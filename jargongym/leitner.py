from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Mapping


VALID_GRADES = {"again", "hard", "good", "easy"}
BOX_INTERVAL_DAYS = {
    1: 0,
    2: 1,
    3: 3,
    4: 7,
    5: 14,
}


def review_card(
    state: Mapping[str, Any] | None,
    grade: str,
    now: datetime | None = None,
) -> dict[str, Any]:
    if grade not in VALID_GRADES:
        raise ValueError(f"unknown review grade: {grade}")

    now = _as_utc(now or datetime.now(timezone.utc))
    current = dict(state or {})
    current_box = int(current.get("box", 1))

    if grade == "again":
        next_box = 1
    elif grade == "hard":
        next_box = current_box
    elif grade == "good":
        next_box = min(5, current_box + 1)
    else:
        next_box = min(5, current_box + 2)

    due = now + timedelta(days=BOX_INTERVAL_DAYS[next_box])
    return {
        "box": next_box,
        "due": due.isoformat(),
        "reviews": int(current.get("reviews", 0)) + 1,
        "last_grade": grade,
        "last_reviewed": now.isoformat(),
    }


def due_cards(
    cards: list[Any],
    progress: Mapping[str, Mapping[str, Any]],
    now: datetime | None = None,
) -> list[Any]:
    now = _as_utc(now or datetime.now(timezone.utc))
    due: list[tuple[int, datetime, int, Any]] = []

    for index, card in enumerate(cards):
        card_id = _card_id(card)
        state = progress.get(card_id)
        is_new = 0 if state else 1
        due_at = _parse_due(state.get("due")) if state else now
        if due_at <= now:
            due.append((is_new, due_at, index, card))

    due.sort(key=lambda item: (item[0], item[1], item[2]))
    return [item[3] for item in due]


def _card_id(card: Any) -> str:
    if isinstance(card, Mapping):
        return str(card["id"])
    return str(card.id)


def _parse_due(value: Any) -> datetime:
    if not value:
        return datetime.min.replace(tzinfo=timezone.utc)
    return _as_utc(datetime.fromisoformat(str(value)))


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)
