"""サイ人格 YAML の読み込み（dialogue 層）。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from utils.yaml_loader import load_yaml

PERSONA_PATH = Path(__file__).resolve().parent / "persona.yaml"


def load_persona(path: Path | str | None = None) -> dict[str, Any]:
    return load_yaml(path or PERSONA_PATH)
