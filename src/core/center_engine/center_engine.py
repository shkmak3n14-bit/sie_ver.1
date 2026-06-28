"""
S.I.E Center Engine — センター判定

本能 / 思考 / 感情センターのスコア集計と primary_center 判定。
補正の適用は type_engine の責務（本モジュールは判定結果のみ返す）。
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

_SRC = Path(__file__).resolve().parents[2]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from utils.scoring_helpers import aggregate_by_group, rank_desc
from utils.yaml_loader import QUESTIONS_DIR, load_questions, load_scoring

CENTER_FILE = QUESTIONS_DIR / "center.yaml"
CENTER_KEYS = ("instinct", "thinking", "feeling")


class CenterEngine:
    """センター判定エンジン。"""

    def __init__(
        self,
        questions_path: Path | None = None,
        scoring_path: Path | None = None,
    ) -> None:
        self.questions = load_questions(questions_path or CENTER_FILE)
        scoring = load_scoring(scoring_path)
        self.options_map: dict[str, int] = scoring["options_map"]
        self.scale_max = int(scoring.get("options_scale", {}).get("max", 3))

    def evaluate(self, answers: dict[str, Any]) -> dict[str, Any]:
        """
        回答 dict を受け取り、センター判定結果を返す。

        Returns:
            primary_center, scores, ranking
        """
        scores = aggregate_by_group(
            self.questions,
            answers,
            group_key="type_number",
            options_map=self.options_map,
            scale_max=self.scale_max,
            default_keys=list(CENTER_KEYS),
        )
        scores = {k: round(scores.get(k, 0.0), 4) for k in CENTER_KEYS}
        ranking = rank_desc(scores)
        primary_center = ranking[0][0] if ranking else CENTER_KEYS[0]

        return {
            "primary_center": primary_center,
            "scores": scores,
            "ranking": [{"center": k, "score": v} for k, v in ranking],
        }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="S.I.E Center Engine")
    parser.add_argument("--answers", required=True, help="回答 JSON ファイル")
    parser.add_argument("--output", help="結果出力先 JSON")
    args = parser.parse_args()

    with Path(args.answers).open(encoding="utf-8") as f:
        answers = json.load(f)

    result = CenterEngine().evaluate(answers)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
