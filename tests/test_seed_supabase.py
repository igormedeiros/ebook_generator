from src import seed_supabase as seed


def test_build_markdown_payloads_reads_all_markdown_files(tmp_path, monkeypatch):
    project_root = tmp_path / "project"
    kb_dir = project_root / "kb"
    nested_dir = kb_dir / "nested"
    nested_dir.mkdir(parents=True)

    top_file = kb_dir / "root_doc.md"
    nested_file = nested_dir / "sub_doc.md"
    ignored_file = nested_dir / "ignore.txt"

    top_file.write_text("top", encoding="utf-8")
    nested_file.write_text("nested", encoding="utf-8")
    ignored_file.write_text("ignore", encoding="utf-8")

    monkeypatch.setattr(seed, "PROJECT_ROOT", project_root, raising=False)
    monkeypatch.setattr(seed, "KB_PATH", kb_dir, raising=False)

    payloads = seed._build_markdown_payloads()

    assert len(payloads) == 2
    assert payloads[0]["type"] == payloads[1]["type"] == "markdown"
    assert {p["source"] for p in payloads} == {
        str(top_file.relative_to(project_root)),
        str(nested_file.relative_to(project_root)),
    }
    assert {p["content"] for p in payloads} == {"top", "nested"}


def test_build_markdown_payloads_returns_empty_when_kb_missing(tmp_path, monkeypatch):
    project_root = tmp_path / "project"
    missing_kb = project_root / "kb_missing"

    monkeypatch.setattr(seed, "PROJECT_ROOT", project_root, raising=False)
    monkeypatch.setattr(seed, "KB_PATH", missing_kb, raising=False)

    assert seed._build_markdown_payloads() == []
