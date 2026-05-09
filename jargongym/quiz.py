from __future__ import annotations

from dataclasses import dataclass
import hashlib
import re
from typing import TypeVar

from jargongym.cards import Card


T = TypeVar("T")


@dataclass(frozen=True)
class ChoiceOption:
    value: str
    label_markdown: str


@dataclass(frozen=True)
class ChoiceQuiz:
    card: Card
    prompt: str
    answer: str
    options: list[ChoiceOption]


def build_choice_quiz(card: Card, scoped_cards: list[Card], all_cards: list[Card]) -> ChoiceQuiz:
    answer = _meaning_option(card)
    distractors = _unique_meaning_options(scoped_cards, card)

    if len(distractors) < 3:
        existing = {option.value for option in distractors}
        for option in _unique_meaning_options(all_cards, card):
            if option.value not in existing:
                distractors.append(option)
                existing.add(option.value)
            if len(distractors) >= 3:
                break

    options = _stable_shuffle([answer] + distractors[:3], f"{card.id}:options")
    return ChoiceQuiz(
        card=card,
        prompt="下面哪个是真实含义？",
        answer=answer.value,
        options=options,
    )


def _unique_meaning_options(cards: list[Card], current: Card) -> list[ChoiceOption]:
    seen: set[str] = set()
    values: list[ChoiceOption] = []
    for card in cards:
        option = _meaning_option(card)
        if card.id == current.id or not option.value or option.value in seen:
            continue
        seen.add(option.value)
        values.append(option)
    return _stable_shuffle(values, current.id)


def _meaning_option(card: Card) -> ChoiceOption:
    label_markdown = _extract_meaning_markdown(card.answer_markdown) or card.translation
    return ChoiceOption(
        value=_clean_markdown(label_markdown),
        label_markdown=label_markdown,
    )


def _extract_meaning_markdown(markdown_text: str) -> str:
    lines = [_strip_list_marker(line.strip()) for line in markdown_text.splitlines()]

    for line in lines:
        label, body = _split_labeled_line(line)
        if label == "含义" and body:
            return body

    for line in lines:
        if not line:
            continue
        _label, body = _split_labeled_line(line)
        return body or line

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
    value = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", value)
    value = re.sub(r"_([^_\n]+)_", r"\1", value)
    value = re.sub(r"`([^`]+)`", r"\1", value)
    return re.sub(r"\s+", " ", value).strip()


def _stable_shuffle(values: list[T], seed: str) -> list[T]:
    return sorted(
        values,
        key=lambda value: hashlib.sha256(
            f"{seed}:{_shuffle_key(value)}".encode("utf-8")
        ).hexdigest(),
    )


def _shuffle_key(value: object) -> str:
    if isinstance(value, ChoiceOption):
        return value.value
    return str(value)
