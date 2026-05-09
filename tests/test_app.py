import json
from pathlib import Path

from jargongym.app import create_app


def write_multi_category_glossary(path: Path) -> None:
    path.write_text(
        "## 一、测试与质量\n\n"
        "### smoke test —— 冒烟测试\n\n"
        "- **含义**：浅层检查。\n\n"
        "### regression test —— 回归测试\n\n"
        "- **含义**：确认旧功能没坏。\n\n"
        "### TDD（Test-Driven Development） —— 测试驱动开发\n\n"
        "- **含义**：先写测试再实现。\n\n"
        "### flaky test —— 抖动测试\n\n"
        "- **含义**：时好时坏的测试。\n\n"
        "## 二、调试与排查\n\n"
        "### root cause —— 根因\n\n"
        "- **含义**：真正的源头。\n",
        encoding="utf-8",
    )


def test_homepage_renders_a_card(tmp_path: Path):
    glossary = tmp_path / "glossary.md"
    glossary.write_text(
        "## 一、测试与质量\n\n"
        "### smoke test —— 冒烟测试\n\n"
        "- **含义**：浅层检查。\n",
        encoding="utf-8",
    )
    progress = tmp_path / "progress.json"
    app = create_app(glossary_path=glossary, progress_path=progress)

    response = app.test_client().get("/")

    assert response.status_code == 200
    assert "smoke test" in response.get_data(as_text=True)
    assert "冒烟测试" in response.get_data(as_text=True)


def test_homepage_filters_cards_by_selected_category(tmp_path: Path):
    glossary = tmp_path / "glossary.md"
    write_multi_category_glossary(glossary)
    progress = tmp_path / "progress.json"
    app = create_app(glossary_path=glossary, progress_path=progress)

    response = app.test_client().get("/", query_string={"category": "二、调试与排查"})
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "root cause" in html
    assert "smoke test" not in html
    assert "二、调试与排查" in html


def test_homepage_renders_markdown_bold_in_answer(tmp_path: Path):
    glossary = tmp_path / "glossary.md"
    glossary.write_text(
        "## 一、测试与质量\n\n"
        "### smoke test —— 冒烟测试\n\n"
        "- **含义**：浅层检查。\n",
        encoding="utf-8",
    )
    progress = tmp_path / "progress.json"
    app = create_app(glossary_path=glossary, progress_path=progress)

    html = app.test_client().get("/").get_data(as_text=True)

    assert "<strong>含义</strong>" in html
    assert "**含义**" not in html


def test_review_post_records_progress_and_redirects(tmp_path: Path):
    glossary = tmp_path / "glossary.md"
    glossary.write_text(
        "## 一、测试与质量\n\n"
        "### smoke test —— 冒烟测试\n\n"
        "- **含义**：浅层检查。\n",
        encoding="utf-8",
    )
    progress = tmp_path / "progress.json"
    app = create_app(glossary_path=glossary, progress_path=progress)

    response = app.test_client().post("/review/smoke-test", data={"grade": "good"})

    assert response.status_code == 302
    assert '"smoke-test"' in progress.read_text(encoding="utf-8")
    assert '"box": 2' in progress.read_text(encoding="utf-8")


def test_again_review_enters_immediate_quiz_queue(tmp_path: Path):
    glossary = tmp_path / "glossary.md"
    write_multi_category_glossary(glossary)
    progress = tmp_path / "progress.json"
    app = create_app(glossary_path=glossary, progress_path=progress)

    response = app.test_client().post(
        "/review/smoke-test",
        data={"grade": "again", "category": "一、测试与质量"},
    )

    saved = json.loads(progress.read_text(encoding="utf-8"))
    assert response.status_code == 302
    assert response.headers["Location"].endswith(
        "/quiz/smoke-test?category=%E4%B8%80%E3%80%81%E6%B5%8B%E8%AF%95%E4%B8%8E%E8%B4%A8%E9%87%8F"
    )
    assert saved["smoke-test"]["needs_quiz"] is True
    assert saved["smoke-test"]["lapses"] == 1


def test_quiz_page_renders_multiple_choice_options(tmp_path: Path):
    glossary = tmp_path / "glossary.md"
    write_multi_category_glossary(glossary)
    progress = tmp_path / "progress.json"
    app = create_app(glossary_path=glossary, progress_path=progress)

    response = app.test_client().get(
        "/quiz/smoke-test",
        query_string={"category": "一、测试与质量"},
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "smoke test" in html
    assert "浅层检查" in html
    assert "确认旧功能没坏" in html
    assert 'value="冒烟测试"' not in html
    assert 'value="回归测试"' not in html
    assert "小测一下" in html


def test_quiz_page_shows_translation_and_renders_option_markdown(tmp_path: Path):
    glossary = tmp_path / "glossary.md"
    glossary.write_text(
        "## 七、论证 / 沟通比喻类\n\n"
        "### steel man —— 钢人\n\n"
        "- 反过来：用**最强版本**表述对方观点，再来反驳。诚实辩论的姿态。\n\n"
        "### de minimis —— 微不足道原则\n\n"
        "- 全称 *de minimis non curat lex*：\"法律不理会琐碎小事\"。\n\n"
        "### straw man —— 稻草人\n\n"
        "- 故意扭曲对方观点变成更容易反驳的版本，再去打。\n\n"
        "### caveat —— 限定 / 警告\n\n"
        "- \"这话有前提，别外推\"。\n",
        encoding="utf-8",
    )
    progress = tmp_path / "progress.json"
    app = create_app(glossary_path=glossary, progress_path=progress)

    response = app.test_client().get(
        "/quiz/steel-man",
        query_string={"category": "七、论证 / 沟通比喻类"},
    )
    html = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "steel man" in html
    assert "钢人" in html
    assert "下面哪个是真实含义？" in html
    assert "steel man 最接近" not in html
    assert "<em>de minimis non curat lex</em>" in html
    assert "*de minimis non curat lex*" not in html


def test_wrong_quiz_answer_keeps_reinforcement_flag(tmp_path: Path):
    glossary = tmp_path / "glossary.md"
    write_multi_category_glossary(glossary)
    progress = tmp_path / "progress.json"
    progress.write_text('{"smoke-test": {"box": 1, "needs_quiz": true}}', encoding="utf-8")
    app = create_app(glossary_path=glossary, progress_path=progress)

    response = app.test_client().post(
        "/quiz/smoke-test",
        data={"choice": "确认旧功能没坏。", "category": "一、测试与质量"},
    )
    saved = json.loads(progress.read_text(encoding="utf-8"))

    assert response.status_code == 200
    assert "还差一点" in response.get_data(as_text=True)
    assert saved["smoke-test"]["needs_quiz"] is True
    assert saved["smoke-test"]["quiz_wrong"] == 1


def test_correct_quiz_answer_clears_reinforcement_flag(tmp_path: Path):
    glossary = tmp_path / "glossary.md"
    write_multi_category_glossary(glossary)
    progress = tmp_path / "progress.json"
    progress.write_text('{"smoke-test": {"box": 1, "needs_quiz": true}}', encoding="utf-8")
    app = create_app(glossary_path=glossary, progress_path=progress)

    response = app.test_client().post(
        "/quiz/smoke-test",
        data={"choice": "浅层检查。", "category": "一、测试与质量"},
    )
    saved = json.loads(progress.read_text(encoding="utf-8"))

    assert response.status_code == 302
    assert response.headers["Location"].endswith(
        "/?category=%E4%B8%80%E3%80%81%E6%B5%8B%E8%AF%95%E4%B8%8E%E8%B4%A8%E9%87%8F"
    )
    assert saved["smoke-test"]["needs_quiz"] is False
    assert saved["smoke-test"]["quiz_correct"] == 1
    assert saved["smoke-test"]["due"] > saved["smoke-test"].get("last_reviewed", "")


def test_reset_removes_progress_file(tmp_path: Path):
    glossary = tmp_path / "glossary.md"
    glossary.write_text(
        "## 一、测试与质量\n\n"
        "### smoke test —— 冒烟测试\n\n"
        "- **含义**：浅层检查。\n",
        encoding="utf-8",
    )
    progress = tmp_path / "progress.json"
    progress.write_text('{"smoke-test": {"box": 2}}', encoding="utf-8")
    app = create_app(glossary_path=glossary, progress_path=progress)

    response = app.test_client().post("/reset")

    assert response.status_code == 302
    assert not progress.exists()
