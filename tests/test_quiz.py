from jargongym.cards import Card
from jargongym.quiz import build_choice_quiz


def test_choice_quiz_uses_meaning_line_instead_of_translation():
    cards = [
        Card(
            id="smoke-test",
            term="smoke test",
            translation="冒烟测试",
            category="一、测试与质量",
            answer_markdown="- **字面**：只检查会不会冒烟。\n- **含义**：跑一组最浅的检查，确认整体能启动。",
        ),
        Card(
            id="regression-test",
            term="regression test",
            translation="回归测试",
            category="一、测试与质量",
            answer_markdown="- **含义**：固定一组老用例，每次改完都重跑。",
        ),
        Card(
            id="flaky-test",
            term="flaky test",
            translation="抖动测试",
            category="一、测试与质量",
            answer_markdown="- **含义**：时好时坏、偶尔失败的测试。",
        ),
        Card(
            id="tdd",
            term="TDD",
            translation="测试驱动开发",
            category="一、测试与质量",
            answer_markdown="- **含义**：先写测试，再写刚好能通过测试的实现。",
        ),
    ]

    quiz = build_choice_quiz(cards[0], cards, cards)
    option_values = [option.value for option in quiz.options]

    assert quiz.answer == "跑一组最浅的检查，确认整体能启动。"
    assert "冒烟测试" not in option_values
    assert "回归测试" not in option_values
    assert "固定一组老用例，每次改完都重跑。" in option_values


def test_choice_quiz_falls_back_to_first_explanation_bullet():
    cards = [
        Card(
            id="steel-man",
            term="steel man",
            translation="钢人",
            category="七、论证 / 沟通比喻类",
            answer_markdown="- 反过来：用**最强版本**表述对方观点，再来反驳。诚实辩论的姿态。",
        ),
        Card(
            id="straw-man",
            term="straw man",
            translation="稻草人",
            category="七、论证 / 沟通比喻类",
            answer_markdown="- 故意扭曲对方观点变成更容易反驳的版本，再去打。",
        ),
        Card(
            id="caveat",
            term="caveat",
            translation="限定 / 警告",
            category="七、论证 / 沟通比喻类",
            answer_markdown='- "这话有前提，别外推"。',
        ),
        Card(
            id="rationale",
            term="rationale",
            translation="理据",
            category="七、论证 / 沟通比喻类",
            answer_markdown='- "为什么这么做"的理由 / 推理过程。',
        ),
    ]

    quiz = build_choice_quiz(cards[0], cards, cards)
    option_values = [option.value for option in quiz.options]

    assert quiz.answer == "反过来：用最强版本表述对方观点，再来反驳。诚实辩论的姿态。"
    assert "钢人" not in option_values
    assert "故意扭曲对方观点变成更容易反驳的版本，再去打。" in option_values


def test_choice_quiz_keeps_markdown_label_separate_from_plain_value():
    cards = [
        Card(
            id="de-minimis",
            term="de minimis",
            translation="微不足道原则",
            category="七、论证 / 沟通比喻类",
            answer_markdown='- 全称 *de minimis non curat lex*："法律不理会琐碎小事"。',
        ),
        Card(
            id="steel-man",
            term="steel man",
            translation="钢人",
            category="七、论证 / 沟通比喻类",
            answer_markdown="- 反过来：用**最强版本**表述对方观点，再来反驳。诚实辩论的姿态。",
        ),
        Card(
            id="straw-man",
            term="straw man",
            translation="稻草人",
            category="七、论证 / 沟通比喻类",
            answer_markdown="- 故意扭曲对方观点变成更容易反驳的版本，再去打。",
        ),
        Card(
            id="caveat",
            term="caveat",
            translation="限定 / 警告",
            category="七、论证 / 沟通比喻类",
            answer_markdown='- "这话有前提，别外推"。',
        ),
    ]

    quiz = build_choice_quiz(cards[0], cards, cards)

    assert quiz.answer == '全称 de minimis non curat lex："法律不理会琐碎小事"。'
    assert quiz.options[0].value
    assert any("*de minimis non curat lex*" in option.label_markdown for option in quiz.options)
