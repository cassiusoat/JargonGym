from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any


Progress = dict[str, dict[str, Any]]


def load_progress(path: Path) -> Progress:
    if not path.exists():
        return {}

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        backup = path.with_name(f"{path.name}.corrupt-{_timestamp()}")
        path.replace(backup)
        return {}

    if not isinstance(data, dict):
        return {}
    return {str(key): value for key, value in data.items() if isinstance(value, dict)}


def save_progress(path: Path, progress: Progress) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(
        json.dumps(progress, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    tmp_path.replace(path)


def reset_progress(path: Path) -> None:
    if path.exists():
        path.unlink()


def _timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")

