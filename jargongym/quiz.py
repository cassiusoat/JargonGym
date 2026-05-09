from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re

from jargongym.cards import Card


@dataclass(frozen=True)
class ChoiceQuiz:
    card: Card
    prompt: str
    answer: str
    options: list[str]


def build_choice_quiz(card: Card, scoped_cards: list[Card], all_cards: list[Card]) -> ChoiceQuiz:
    answer = _meaning(card)
    distractors = _unique_meanings(scoped_cards, card)

    if len(distractors) < 3:
        existing = set(distractors)
        for meaning in _unique_meanings(all_cards, card):
            if meaning not in existing:
                distractors.append(meaning)
                existing.add(meaning)
            if len(distractors) >= 3:
                break

    options = _stable_shuffle([answer] + distractors[:3], f"{card.id}:options")
    return ChoiceQuiz(
        card=card,
        prompt=f"{card.term} 最接近下面哪个真实含义？",
        answer=answer,
        options=options,
    )


def _unique_meanings(cards: list[Card], current: Card) -> list[str]:
    seen: set[str] = set()
    values: list[str] = []
    for card in cards:
        meaning = _meaning(card)
        if card.id == current.id or not meaning or meaning in seen:
            continue
        seen.add(meaning)
        values.append(meaning)
    return _stable_shuffle(values, current.id)


def _meaning(card: Card) -> str:
    return _extract_meaning(card.answer_markdown) or card.translation


def _extract_meaning(markdown_text: str) -> str:
    lines = [_strip_list_marker(line.strip()) for line in markdown_text.splitlines()]

    for line in lines:
        label, body = _split_labeled_line(line)
        if label == "含义" and body:
            return _clean_markdown(body)

    for line in lines:
        if not line:
            continue
        _label, body = _split_labeled_line(line)
        return _clean_markdown(body or line)

    return ""


def _strip_list_marker(line: str) -> str:
    return re.sub(r"^(?:[-*+]|\d+[.)])\s+", "", line)


def _split_labeled_line(line: str) -> tuple[str, str]:
    match = re.match(r"^\*\*(?P<label>[^*：:]+)\*\*[：:]\s*(?P<body>.*)$", line)
    if not match:
        return "", ""
    return match.group("label").strip(), match.group("body").strip()


def _clean_markdown(value: str) -> str:
    value = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"\1", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    return re.sub(r"\s+", " ", value).strip()


def _stable_shuffle(values: list[str], seed: str) -> list[str]:
    return sorted(
        values,
        key=lambda value: hashlib.sha256(f"{seed}:{value}".encode("utf-8")).hexdigest(),
    )
