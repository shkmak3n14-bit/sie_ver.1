"""
S.I.E Episode Engine — 幼少期エピソード解析

自由記述からシグナルを抽出し、タイプ補正用の判定結果を返す。
補正の適用は type_engine の責務（本モジュールは解析結果のみ返す）。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_SRC = Path(__file__).resolve().parents[2]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from utils.yaml_loader import QUESTIONS_DIR, load_questions, load_scoring

EPISODE_FILE = QUESTIONS_DIR / "episode_analysis.yaml"


class EpisodeEngine:
    def __init__(self, scoring_path: Path | None = None) -> None:
        self.scoring = load_scoring(scoring_path)
        self.questions = load_questions(EPISODE_FILE)
        self.episode_cfg = self.scoring.get("episode_adjustment", {})
        self.max_total = float(
            self.scoring.get("episode_scoring", {}).get("max_total_adjustment", 0.15)
        )

    def evaluate(self, answers: dict[str, Any]) -> dict[str, Any]:
        combined_text = " ".join(
            str(answers.get(q["id"], ""))
            for q in self.questions
            if answers.get(q["id"])
        )

        if not combined_text.strip():
            return {
                "matched_signals": [],
                "adjustments": {f"type{n}": 0.0 for n in range(1, 10)},
                "combined_text_length": 0,
            }

        matched: list[str] = []
        adjustments: dict[str, float] = {f"type{n}": 0.0 for n in range(1, 10)}

        for rule_name, rule in self.episode_cfg.items():
            if rule_name in ("method", "apply_rule") or not isinstance(rule, dict):
                continue
            signals = rule.get("signals", [])
            if not any(sig in combined_text for sig in signals):
                continue
            matched.append(rule_name)
            for type_num in range(1, 10):
                key = f"type{type_num}"
                if key in rule:
                    adjustments[key] += float(rule[key])

        for key in adjustments:
            adjustments[key] = round(min(adjustments[key], self.max_total), 4)

        return {
            "matched_signals": matched,
            "adjustments": adjustments,
            "combined_text_length": len(combined_text),
        }


def run_episode_engine(answers: dict[str, Any]) -> dict[str, Any]:
    return EpisodeEngine().evaluate(answers)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="S.I.E Episode Engine")
    parser.add_argument("--answers", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    with Path(args.answers).open(encoding="utf-8") as f:
        answers = json.load(f)

    result = run_episode_engine(answers)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
