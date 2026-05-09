from pathlib import Path

from jargongym.app import create_app


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
