"""YAML 読み込み共通ユーティリティ。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError as exc:
    raise ImportError("PyYAML が必要です: pip install pyyaml") from exc

CORE_DIR = Path(__file__).resolve().parents[1] / "core"
PROJECT_ROOT = Path(__file__).resolve().parents[2]
QUESTIONS_DIR = CORE_DIR / "questions"
SCORING_PATH = CORE_DIR / "scoring" / "scoring.yaml"
DIALOGUE_DIR = Path(__file__).resolve().parents[1] / "dialogue"


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


def load_yaml_file(relative_path: str) -> dict[str, Any]:
    """プロジェクトルートからの相対パスで YAML を読み込む。"""
    return load_yaml(PROJECT_ROOT / relative_path)


def load_all_type_questions() -> list[dict[str, Any]]:
    """type1.yaml 〜 type9.yaml を結合して返す。"""
    questions: list[dict[str, Any]] = []
    for n in range(1, 10):
        questions.extend(load_questions(QUESTIONS_DIR / f"type{n}.yaml"))
    return questions


def load_questions_by_category(category: str) -> list[dict[str, Any]]:
    """category 別に質問を読み込む。"""
    if category == "type":
        return load_all_type_questions()
    mapping = {
        "center": QUESTIONS_DIR / "center.yaml",
        "wing": QUESTIONS_DIR / "wing.yaml",
        "episode": QUESTIONS_DIR / "episode_analysis.yaml",
    }
    if category not in mapping:
        raise ValueError(f"Unknown category: {category}")
    return load_questions(mapping[category])
