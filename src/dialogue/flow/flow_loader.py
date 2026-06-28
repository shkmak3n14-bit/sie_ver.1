"""対話フロー YAML の読み込み（dialogue 層）。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from utils.yaml_loader import load_yaml

FLOW_DIR = Path(__file__).resolve().parent

PHASE_FILES: dict[str, str] = {
    "intro": "intro.yaml",
    "self_understanding": "self_understanding.yaml",
    "self": "self_understanding.yaml",
    "other_understanding": "other_understanding.yaml",
    "other": "other_understanding.yaml",
    "relationship": "relationship.yaml",
    "relation": "relationship.yaml",
    "questioning": "questioning.yaml",
    "feedback": "feedback.yaml",
}


def load_flow(phase: str) -> list[dict[str, Any]]:
    filename = PHASE_FILES.get(phase)
    if not filename:
        raise ValueError(f"Unknown flow phase: {phase}")
    data = load_yaml(FLOW_DIR / filename)
    return list(data.get("flow") or [])
