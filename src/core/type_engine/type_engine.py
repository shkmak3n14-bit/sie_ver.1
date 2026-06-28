"""
S.I.E Type Engine — エニアグラム診断の最終統合ロジック

core 専用。dialogue への依存なし。
scoring.yaml に従い type/center/wing/episode の回答を統合して最終タイプを決定する。
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from typing import Any

_SRC = Path(__file__).resolve().parents[2]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from core.center_engine.center_engine import CenterEngine
from core.wing_engine.wing_engine import WingEngine
from utils.scoring_helpers import normalize_answer, question_score
from utils.yaml_loader import QUESTIONS_DIR, SCORING_PATH, load_questions, load_scoring

EPISODE_FILE = QUESTIONS_DIR / "episode_analysis.yaml"
DIMENSIONS = ("core", "fear", "desire", "defense")


class TypeEngine:
    """エニアグラム診断の最終統合エンジン。"""

    def __init__(
        self,
        scoring_path: Path | None = None,
        questions_dir: Path | None = None,
    ) -> None:
        self.scoring_path = scoring_path or SCORING_PATH
        self.questions_dir = questions_dir or QUESTIONS_DIR
        self.scoring = load_scoring(self.scoring_path)
        self.options_map: dict[str, int] = self.scoring["options_map"]
        self.scale_max = int(self.scoring.get("options_scale", {}).get("max", 3))
        self.top_n = int(self.scoring.get("type_scoring", {}).get("top_n", 3))
        self.episode_max_adj = float(
            self.scoring.get("episode_scoring", {}).get("max_total_adjustment", 0.15)
        )

        self.center_engine = CenterEngine(scoring_path=self.scoring_path)
        self.wing_engine = WingEngine(scoring_path=self.scoring_path)

        self.type_questions = self._load_type_questions()
        self.episode_questions = load_questions(EPISODE_FILE)

    def _load_type_questions(self) -> list[dict[str, Any]]:
        questions: list[dict[str, Any]] = []
        for n in range(1, 10):
            questions.extend(load_questions(self.questions_dir / f"type{n}.yaml"))
        return questions

    def score_types(self, answers: dict[str, Any]) -> tuple[dict[int, float], dict[int, list[int]]]:
        raw: dict[int, float] = {n: 0.0 for n in range(1, 10)}
        values: dict[int, list[int]] = {n: [] for n in range(1, 10)}

        for question in self.type_questions:
            qid = question["id"]
            if qid not in answers:
                continue
            value = normalize_answer(answers[qid], self.options_map, self.scale_max)
            if value is None:
                continue
            type_num = int(question["type_number"])
            raw[type_num] += question_score(question, value, self.scale_max)
            values[type_num].append(value)

        return raw, values

    def apply_center_adjustment(
        self,
        raw_scores: dict[int, float],
        center_evaluation: dict[str, Any],
    ) -> tuple[dict[int, float], dict[str, Any]]:
        center_adj_cfg = self.scoring.get("center_adjustment", {})
        center_scores = center_evaluation["scores"]
        dominant = center_evaluation["primary_center"]
        adjustments: dict[int, float] = {n: 0.0 for n in range(1, 10)}

        center_block = center_adj_cfg.get(dominant, {})
        for type_num in range(1, 10):
            key = f"type{type_num}"
            adjustments[type_num] = float(center_block.get(key, 0.0))

        adjusted = dict(raw_scores)
        for type_num, adj in adjustments.items():
            if adj > 0:
                adjusted[type_num] = adjusted[type_num] * (1.0 + adj)

        result = {
            "dominant_center": dominant,
            "primary_center": dominant,
            "center_scores": center_scores,
            "ranking": center_evaluation.get("ranking", []),
            "adjustments_applied": adjustments,
        }
        return adjusted, result

    def apply_wing_adjustment(
        self,
        scores: dict[int, float],
        wing_evaluation: dict[str, Any],
    ) -> tuple[dict[int, float], dict[str, Any]]:
        wing_adj_cfg = self.scoring.get("wing_adjustment", {})
        wing_scores = wing_evaluation["scores"]
        dominant_wing = wing_evaluation.get("primary_wing")

        if not dominant_wing:
            return scores, {
                "dominant_wing": None,
                "primary_wing": None,
                "wing_scores": wing_scores,
                "ranking": wing_evaluation.get("ranking", []),
                "adjustments_applied": {n: 0.0 for n in range(1, 10)},
            }

        wing_table = wing_adj_cfg.get(dominant_wing, {})
        adjustments: dict[int, float] = {n: 0.0 for n in range(1, 10)}

        for type_num in range(1, 10):
            key = f"type{type_num}"
            if key in wing_table:
                adjustments[type_num] = float(wing_table[key])

        adjusted = dict(scores)
        for type_num, adj in adjustments.items():
            if adj > 0:
                adjusted[type_num] = adjusted[type_num] * (1.0 + adj)

        result = {
            "dominant_wing": dominant_wing,
            "primary_wing": dominant_wing,
            "wing_label": dominant_wing,
            "wing_scores": wing_scores,
            "ranking": wing_evaluation.get("ranking", []),
            "adjustments_applied": adjustments,
        }
        return adjusted, result

    def apply_episode_adjustment(
        self,
        raw_scores: dict[int, float],
        scores: dict[int, float],
        answers: dict[str, Any],
    ) -> tuple[dict[int, float], dict[str, Any]]:
        episode_cfg = self.scoring.get("episode_adjustment", {})
        combined_text = " ".join(
            str(answers.get(q["id"], ""))
            for q in self.episode_questions
            if answers.get(q["id"])
        )

        if not combined_text.strip():
            return scores, {
                "matched_signals": [],
                "adjustments_applied": {n: 0.0 for n in range(1, 10)},
            }

        matched: list[str] = []
        type_adj: dict[int, float] = {n: 0.0 for n in range(1, 10)}

        for rule_name, rule in episode_cfg.items():
            if rule_name in ("method", "apply_rule"):
                continue
            if not isinstance(rule, dict):
                continue
            signals = rule.get("signals", [])
            if not any(sig in combined_text for sig in signals):
                continue
            matched.append(rule_name)
            for type_num in range(1, 10):
                key = f"type{type_num}"
                if key in rule:
                    type_adj[type_num] += float(rule[key])

        for type_num in range(1, 10):
            type_adj[type_num] = min(type_adj[type_num], self.episode_max_adj)

        adjusted = dict(scores)
        for type_num in range(1, 10):
            if type_adj[type_num] > 0:
                adjusted[type_num] += raw_scores[type_num] * type_adj[type_num]

        return adjusted, {
            "matched_signals": matched,
            "adjustments_applied": type_adj,
            "combined_text_length": len(combined_text),
        }

    def extract_candidates(
        self,
        scores: dict[int, float],
        answer_values: dict[int, list[int]],
    ) -> list[int]:
        ranked = sorted(
            range(1, 10),
            key=lambda t: (-scores[t], self._answer_std(answer_values[t]), t),
        )
        return ranked[: self.top_n]

    @staticmethod
    def _answer_std(values: list[int]) -> float:
        if len(values) < 2:
            return 0.0
        mean = sum(values) / len(values)
        variance = sum((v - mean) ** 2 for v in values) / len(values)
        return math.sqrt(variance)

    def compute_confidence(
        self,
        scores: dict[int, float],
        candidates: list[int],
    ) -> str:
        if len(candidates) < 2:
            return "low"
        first = scores[candidates[0]]
        second = scores[candidates[1]]
        if first <= 0:
            return "low"
        ratio = (first - second) / first
        if ratio >= 0.15:
            return "high"
        if ratio >= 0.08:
            return "medium"
        return "low"

    def run(self, answers: dict[str, Any]) -> dict[str, Any]:
        """回答 dict を受け取り、診断結果を JSON 可能な dict で返す。"""
        raw_scores, answer_values = self.score_types(answers)

        center_evaluation = self.center_engine.evaluate(answers)
        wing_evaluation = self.wing_engine.evaluate(answers)

        scores_after_center, center_result = self.apply_center_adjustment(
            raw_scores, center_evaluation
        )
        scores_after_wing, wing_result = self.apply_wing_adjustment(
            scores_after_center, wing_evaluation
        )
        adjusted_scores, episode_result = self.apply_episode_adjustment(
            raw_scores, scores_after_wing, answers
        )

        candidates = self.extract_candidates(adjusted_scores, answer_values)
        main_type = candidates[0] if candidates else 1
        confidence = self.compute_confidence(adjusted_scores, candidates)

        dominant_center = center_result.get("dominant_center")
        primary_in_center = False
        if dominant_center:
            center_types = (
                self.scoring.get("center_adjustment", {})
                .get(dominant_center, {})
                .get("types", [])
            )
            primary_in_center = main_type in center_types
        if not primary_in_center and confidence == "high":
            confidence = "medium"
        elif not primary_in_center and confidence == "medium":
            confidence = "low"

        corrections: list[str] = []
        if any(center_result["adjustments_applied"].values()):
            corrections.append("center")
        if wing_result.get("primary_wing"):
            corrections.append("wing")
        if episode_result.get("matched_signals"):
            corrections.append("episode")

        return {
            "main_type": main_type,
            "candidates": candidates,
            "raw_scores": {str(k): round(v, 4) for k, v in raw_scores.items()},
            "adjusted_scores": {
                str(k): round(v, 4) for k, v in adjusted_scores.items()
            },
            "center_result": center_result,
            "wing_result": wing_result,
            "episode_result": episode_result,
            "confidence": confidence,
            "wing_label": wing_result.get("wing_label"),
            "dominant_center": dominant_center,
            "corrections_applied": corrections,
        }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="S.I.E Type Engine")
    parser.add_argument("--answers", required=True, help="回答 JSON ファイル")
    parser.add_argument("--output", help="結果出力先 JSON")
    args = parser.parse_args()

    with Path(args.answers).open(encoding="utf-8") as f:
        answers = json.load(f)

    result = TypeEngine().run(answers)
    output = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(output + "\n", encoding="utf-8")
    else:
        print(output)


if __name__ == "__main__":
    main()
