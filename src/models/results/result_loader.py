"""タイプ診断結果テンプレート（persona_result）の読み込み。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from utils.yaml_loader import load_yaml

RESULTS_DIR = Path(__file__).resolve().parent

CENTER_LABELS: dict[str, str] = {
    "instinct": "本能センター（Gut）",
    "thinking": "思考センター（Head）",
    "feeling": "感情センター（Heart）",
}


def load_type_result(main_type: int) -> dict[str, Any]:
    """type{N}_result.yaml を読み込む。"""
    if not 1 <= main_type <= 9:
        raise ValueError(f"main_type must be 1-9, got {main_type}")
    path = RESULTS_DIR / f"type{main_type}_result.yaml"
    if not path.exists():
        raise FileNotFoundError(f"Type result template not found: {path}")
    return load_yaml(path)


def merge_engine_into_template(
    template: dict[str, Any],
    type_res: dict[str, Any],
    center_res: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """診断エンジン結果をテンプレートに反映した表示用 dict を返す。"""
    result = dict(template)
    wing_label = type_res.get("wing_label") or ""

    center = dict(template.get("center") or {})
    if center_res:
        primary = center_res.get("primary_center")
        if primary in CENTER_LABELS:
            center["name"] = CENTER_LABELS[primary]

    wing = dict(template.get("wing") or {})
    if wing_label:
        wing["wing_type"] = wing_label

    result["center"] = center
    result["wing"] = wing
    result["_diagnosis"] = {
        "main_type": type_res.get("main_type"),
        "candidates": type_res.get("candidates", []),
        "wing_label": wing_label,
        "confidence": type_res.get("confidence"),
        "dominant_center": (center_res or {}).get("primary_center"),
    }
    return result
