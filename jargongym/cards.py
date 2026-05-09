from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


@dataclass(frozen=True)
class Card:
    id: str
    term: str
    translation: str
    category: str
    answer_markdown: str


def parse_glossary(path: Path) -> list[Card]:
    lines = path.read_text(encoding="utf-8").splitlines()
    cards: list[Card] = []
    used_ids: dict[str, int] = {}
    category = "未分类"
    current_heading: str | None = None
    current_category = category
    body_lines: list[str] = []

    for line in lines:
        if line.startswith("### "):
            _append_card(cards, used_ids, current_heading, current_category, body_lines)
            current_heading = line[4:].strip()
            current_category = category
            body_lines = []
            continue

        if line.startswith("## ") and not line.startswith("### "):
            category = line[3:].strip()
            continue

        if current_heading is not None:
            body_lines.append(line)

    _append_card(cards, used_ids, current_heading, current_category, body_lines)
    return cards


def _append_card(
    cards: list[Card],
    used_ids: dict[str, int],
    heading: str | None,
    category: str,
    body_lines: list[str],
) -> None:
    if heading is None:
        return

    term, translation = _split_heading(heading)
    base_id = _slugify(term) or f"card-{len(cards) + 1}"
    count = used_ids.get(base_id, 0) + 1
    used_ids[base_id] = count
    card_id = base_id if count == 1 else f"{base_id}-{count}"
    answer = "\n".join(body_lines).strip()
    cards.append(
        Card(
            id=card_id,
            term=term,
            translation=translation,
            category=category,
            answer_markdown=answer,
        )
    )


def _split_heading(heading: str) -> tuple[str, str]:
    if "——" in heading:
        term, translation = heading.split("——", 1)
        return term.strip(), translation.strip()
    return heading.strip(), ""


def _slugify(value: str) -> str:
    ascii_text = value.encode("ascii", "ignore").decode("ascii").lower()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text)
    return slug.strip("-")

