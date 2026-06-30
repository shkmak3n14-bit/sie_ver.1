"""Reproduce wing bug: main_type=9 but global 1w9 wins over adjacent 9w8."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
sys.path.insert(0, str(ROOT))

from core.type_engine.type_engine import TypeEngine

answers: dict = {}

# Type 9 questions: high scores
for i in range(1, 16):
    answers[f"type9_q{i:02d}"] = "ほぼいつもそう"

# Other types: moderate
for t in range(1, 9):
    for i in range(1, 16):
        answers[f"type{t}_q{i:02d}"] = "たまにある"

# Type 8 slightly high (candidate)
for i in range(1, 16):
    answers[f"type8_q{i:02d}"] = "よくある"

# Wing: 9w8 high, 9w1 low, 1w9 highest globally
for i in range(49, 52):
    answers[f"wing_q{i:02d}"] = "ほぼいつもそう"  # 9w8
for i in range(52, 55):
    answers[f"wing_q{i:02d}"] = "ほとんどない"  # 9w1
for i in range(1, 4):
    answers[f"wing_q{i:02d}"] = "ほぼいつもそう"  # 1w9

result = TypeEngine().run(answers)
print(json.dumps({
    "main_type": result["main_type"],
    "candidates": result["candidates"],
    "wing_label": result["wing_label"],
    "wing_ranking_top5": result["wing_result"].get("ranking", [])[:5],
}, ensure_ascii=False, indent=2))
