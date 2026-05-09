from pathlib import Path

from jargongym.cards import parse_glossary


def test_parse_glossary_extracts_heading_answer_and_category(tmp_path: Path):
    source = tmp_path / "glossary.md"
    source.write_text(
        "# Title\n\n"
        "## 一、测试与质量\n\n"
        "### smoke test —— 冒烟测试\n\n"
        "- **字面**：只检查会不会冒烟。\n"
        "- **含义**：浅层检查。\n\n"
        "### regression test —— 回归测试\n\n"
        "- **含义**：确认旧功能没坏。\n",
        encoding="utf-8",
    )

    cards = parse_glossary(source)

    assert [card.term for card in cards] == ["smoke test", "regression test"]
    assert cards[0].translation == "冒烟测试"
    assert cards[0].category == "一、测试与质量"
    assert "浅层检查" in cards[0].answer_markdown
    assert cards[0].id == "smoke-test"


def test_parse_real_glossary_finds_many_jargon_cards():
    cards = parse_glossary(Path("docs/claude-code-jargon-glossary.md"))

    assert len(cards) > 80
    assert any(card.term == "smoke test" for card in cards)
    assert any(card.term == "yak shaving" for card in cards)

