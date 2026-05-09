from __future__ import annotations

from dataclasses import dataclass
import hashlib

from jargongym.cards import Card


@dataclass(frozen=True)
class ChoiceQuiz:
    card: Card
    prompt: str
    answer: str
    options: list[str]


def build_choice_quiz(card: Card, scoped_cards: list[Card], all_cards: list[Card]) -> ChoiceQuiz:
    answer = card.translation
    distractors = _unique_translations(scoped_cards, card)

    if len(distractors) < 3:
        existing = set(distractors)
        for translation in _unique_translations(all_cards, card):
            if translation not in existing:
                distractors.append(translation)
                existing.add(translation)
            if len(distractors) >= 3:
                break

    options = _stable_shuffle([answer] + distractors[:3], f"{card.id}:options")
    return ChoiceQuiz(
        card=card,
        prompt=f"{card.term} 最像下面哪个中文含义？",
        answer=answer,
        options=options,
    )


def _unique_translations(cards: list[Card], current: Card) -> list[str]:
    seen: set[str] = set()
    values: list[str] = []
    for card in cards:
        if card.id == current.id or not card.translation or card.translation in seen:
            continue
        seen.add(card.translation)
        values.append(card.translation)
    return _stable_shuffle(values, current.id)


def _stable_shuffle(values: list[str], seed: str) -> list[str]:
    return sorted(
        values,
        key=lambda value: hashlib.sha256(f"{seed}:{value}".encode("utf-8")).hexdigest(),
    )

