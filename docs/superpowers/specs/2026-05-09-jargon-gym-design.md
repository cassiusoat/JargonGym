# Jargon Gym Demo Design

## Goal

Build a local, funny, low-friction web demo for memorizing Claude Code jargon from `docs/claude-code-jargon-glossary.md`.

## Learning Method

Use active recall plus a five-box Leitner system.

- The learner selects a library scope before studying.
- A card first shows the term and category only.
- The learner tries to recall the meaning before revealing the answer.
- If the learner has no recall at all, they can mark the card as forgotten immediately.
- After revealing, the learner grades recall with four buttons.
- Forgotten and fuzzy cards enter an immediate quiz queue.
- The grade updates the card's Leitner box and next review time.

Intervals:

- Box 1: now or same-day retry
- Box 2: 1 day
- Box 3: 3 days
- Box 4: 7 days
- Box 5: 14 days

Grades:

- `again`: move to box 1, due now
- `hard`: stay in the same box, due tomorrow
- `good`: move up one box
- `easy`: move up two boxes

Immediate reinforcement:

- `again` and `hard` redirect to a four-choice quiz.
- The quiz gives instant feedback.
- Wrong answers keep the card in the reinforcement queue.
- Correct answers clear the reinforcement flag and return to the selected library.

## Architecture

Use Flask with server-rendered HTML. The app parses the Markdown glossary at startup, keeps the original glossary read-only, and stores learner progress in `data/progress.json`.

Files:

- `jargongym/cards.py`: parse Markdown into card objects.
- `jargongym/leitner.py`: choose due cards and update review state.
- `jargongym/quiz.py`: build deterministic four-choice vocabulary tests.
- `jargongym/store.py`: read/write JSON progress safely.
- `jargongym/app.py`: Flask routes.
- `templates/index.html`: one-page study interface.
- `templates/quiz.html`: immediate reinforcement quiz.
- `static/styles.css`: playful UI styling.
- `tests/`: parser, Leitner, and route smoke tests.

## UI Direction

Use a light, playful "office jargon gym" style rather than a dark theme.

- Base background: warm off-white.
- Accent colors: lemon yellow, mint green, tomato red, and sky blue.
- Visual language: chunky borders, simple tiles, and joke-heavy button labels.
- Avoid dark panels, purple-blue gradients, and decorative glow effects.

## Data Flow

1. `cards.py` extracts each `###` heading as a card.
2. The route loads progress JSON and merges it with parsed cards.
3. The homepage selects the most overdue card, or shows an all-clear state.
4. A POST to `/review/<card_id>` records the selected grade.
5. The JSON file is updated atomically enough for a local single-user demo.

## Error Handling

- If progress JSON does not exist, start with an empty progress dictionary.
- If progress JSON is corrupt, keep a backup copy and start fresh.
- If the glossary has no parsable cards, the homepage shows a clear message.

## Testing

- Parser test: glossary headings become stable card IDs and answer bodies.
- Leitner test: grading changes box and due dates as expected.
- Flask smoke test: homepage renders and review POST redirects without crashing.
