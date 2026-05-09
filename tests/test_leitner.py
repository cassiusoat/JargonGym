from datetime import datetime, timezone

from jargongym.leitner import due_cards, review_card


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
    assert updated["reviews"] == 4
    assert updated["due"] == "2026-05-09T08:00:00+00:00"


def test_due_cards_include_new_and_overdue_cards_first():
    now = datetime(2026, 5, 9, 8, 0, tzinfo=timezone.utc)
    cards = [
        {"id": "new-card"},
        {"id": "future-card"},
        {"id": "overdue-card"},
    ]
    progress = {
        "future-card": {"due": "2026-05-10T08:00:00+00:00", "box": 2},
        "overdue-card": {"due": "2026-05-08T08:00:00+00:00", "box": 3},
    }

    due = due_cards(cards, progress, now)

    assert [card["id"] for card in due] == ["overdue-card", "new-card"]

