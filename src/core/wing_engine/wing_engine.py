"""
S.I.E Wing Engine — ウイング判定

18種ウイング（1w9〜9w1）のスコア集計と primary_wing 判定。
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

WING_FILE = QUESTIONS_DIR / "wing.yaml"

WING_LABELS = (
    "1w9", "1w2", "2w1", "2w3", "3w2", "3w4", "4w3", "4w5",
    "5w4", "5w6", "6w5", "6w7", "7w6", "7w8", "8w7", "8w9",
    "9w8", "9w1",
)

ADJACENT_WING_LABELS: dict[int, tuple[str, str]] = {
    1: ("1w9", "1w2"),
    2: ("2w1", "2w3"),
    3: ("3w2", "3w4"),
    4: ("4w3", "4w5"),
    5: ("5w4", "5w6"),
    6: ("6w5", "6w7"),
    7: ("7w6", "7w8"),
    8: ("8w7", "8w9"),
    9: ("9w8", "9w1"),
}

DEBUG_LOG_PATH = Path(__file__).resolve().parents[3] / "debug-7cf15b.log"


def _debug_log(location: str, message: str, data: dict, hypothesis_id: str) -> None:
    # #region agent log
    import json
    import time

    payload = {
        "sessionId": "7cf15b",
        "timestamp": int(time.time() * 1000),
        "location": location,
        "message": message,
        "data": data,
        "hypothesisId": hypothesis_id,
    }
    with DEBUG_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    # #endregion


class WingEngine:
    """ウイング判定エンジン。"""

    def __init__(
        self,
        questions_path: Path | None = None,
        scoring_path: Path | None = None,
    ) -> None:
        self.questions = load_questions(questions_path or WING_FILE)
        scoring = load_scoring(scoring_path)
        self.options_map: dict[str, int] = scoring["options_map"]
        self.scale_max = int(scoring.get("options_scale", {}).get("max", 3))

    def evaluate(self, answers: dict[str, Any]) -> dict[str, Any]:
        """
        回答 dict を受け取り、ウイング判定結果を返す。

        Returns:
            primary_wing, scores, ranking
        """
        raw_scores = aggregate_by_group(
            self.questions,
            answers,
            group_key="type_number",
            options_map=self.options_map,
            scale_max=self.scale_max,
            default_keys=list(WING_LABELS),
        )
        scores = {label: round(raw_scores.get(label, 0.0), 4) for label in WING_LABELS}
        answered = {k: v for k, v in scores.items() if v > 0}
        ranking = rank_desc(answered if answered else scores)

        primary_wing = None
        if answered:
            primary_wing = ranking[0][0]

        # #region agent log
        adjacent_for_9 = {
            label: scores.get(label, 0.0) for label in ADJACENT_WING_LABELS.get(9, ())
        }
        _debug_log(
            "wing_engine.py:evaluate",
            "global wing selection",
            {
                "primary_wing_global": primary_wing,
                "top3_global": ranking[:3],
                "adjacent_scores_type9": adjacent_for_9,
                "main_type_not_used": True,
            },
            "A",
        )
        # #endregion

        return {
            "primary_wing": primary_wing,
            "scores": scores,
            "ranking": [{"wing": k, "score": v} for k, v in ranking if v > 0],
        }

    def select_primary_wing_for_type(
        self,
        main_type: int,
        scores: dict[str, float],
    ) -> str | None:
        """メインタイプ確定後、隣接ウイング2種のみから最高スコアを選ぶ。"""
        labels = ADJACENT_WING_LABELS.get(main_type, ())
        if not labels:
            return None

        ranked = sorted(
            ((label, scores.get(label, 0.0)) for label in labels),
            key=lambda item: (-item[1], item[0]),
        )
        if not ranked or ranked[0][1] <= 0:
            return None

        selected = ranked[0][0]
        # #region agent log
        _debug_log(
            "wing_engine.py:select_primary_wing_for_type",
            "adjacent wing selection",
            {
                "main_type": main_type,
                "candidates": labels,
                "scores": {label: scores.get(label, 0.0) for label in labels},
                "selected_wing": selected,
                "runId": "post-fix",
            },
            "FIX",
        )
        # #endregion
        return selected

    def ranking_for_main_type(
        self,
        main_type: int,
        scores: dict[str, float],
    ) -> list[dict[str, float | str]]:
        labels = ADJACENT_WING_LABELS.get(main_type, ())
        ranked = sorted(
            ((label, scores.get(label, 0.0)) for label in labels),
            key=lambda item: (-item[1], item[0]),
        )
        return [{"wing": label, "score": score} for label, score in ranked if score > 0]


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="S.I.E Wing Engine")
    parser.add_argument("--answers", required=True, help="回答 JSON ファイル")
    parser.add_argument("--output", help="結果出力先 JSON")
    args = parser.parse_args()

    with Path(args.answers).open(encoding="utf-8") as f:
        answers = json.load(f)

    result = WingEngine().evaluate(answers)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()


def run_wing_engine(answers: dict[str, Any]) -> dict[str, Any]:
    """wing_engine 判定のエントリポイント（ui / orchestrator 用）。"""
    return WingEngine().evaluate(answers)
