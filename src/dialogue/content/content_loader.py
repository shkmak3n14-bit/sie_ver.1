"""対話コンテンツ YAML の読み込み（dialogue 層）。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from utils.yaml_loader import load_yaml

CONTENT_DIR = Path(__file__).resolve().parent

CONTENT_FILES: dict[str, str] = {
    "enneagram_foundation": "enneagram_foundation.yaml",
}


def load_content(name: str) -> dict[str, Any]:
    filename = CONTENT_FILES.get(name)
    if not filename:
        raise ValueError(f"Unknown content: {name}")
    return load_yaml(CONTENT_DIR / filename)


def load_enneagram_foundation() -> dict[str, Any]:
    return load_content("enneagram_foundation")
