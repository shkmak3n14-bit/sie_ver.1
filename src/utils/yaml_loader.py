"""YAML 読み込み共通ユーティリティ。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise ImportError("PyYAML が必要です: pip install pyyaml") from exc

CORE_DIR = Path(__file__).resolve().parents[1] / "core"
QUESTIONS_DIR = CORE_DIR / "questions"
SCORING_PATH = CORE_DIR / "scoring" / "scoring.yaml"


def load_yaml(path: Path | str) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_questions(path: Path | str) -> list[dict[str, Any]]:
    data = load_yaml(path)
    return list(data.get("questions") or [])


def load_scoring(path: Path | str | None = None) -> dict[str, Any]:
    return load_yaml(path or SCORING_PATH)


def load_answers_json(path: Path | str) -> dict[str, Any]:
    import json

    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)
