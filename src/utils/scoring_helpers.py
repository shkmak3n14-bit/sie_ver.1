"""スコアリング共通ヘルパー。"""

from __future__ import annotations

from typing import Any

DIMENSIONS = ("core", "fear", "desire", "defense")


def normalize_answer(
    answer: Any,
    options_map: dict[str, int],
    scale_max: int = 3,
) -> int | None:
    """選択肢文字列・数値を 0-3 に正規化。自由記述は None。"""
    if answer is None:
        return None
    if isinstance(answer, int):
        if 0 <= answer <= scale_max:
            return answer
        return None
    if isinstance(answer, str):
        text = answer.strip()
        if text in options_map:
            return options_map[text]
        if text.isdigit():
            value = int(text)
            if 0 <= value <= scale_max:
                return value
        return None
    return None


def question_score(question: dict[str, Any], answer_value: int, scale_max: int = 3) -> float:
    weight = question.get("weight") or {}
    if question.get("reverse_scored"):
        answer_value = scale_max - answer_value
    total = 0.0
    for dim in DIMENSIONS:
        total += answer_value * float(weight.get(dim, 1.0))
    return total


def aggregate_by_group(
    questions: list[dict[str, Any]],
    answers: dict[str, Any],
    group_key: str,
    options_map: dict[str, int],
    scale_max: int = 3,
    default_keys: list[Any] | None = None,
) -> dict[Any, float]:
    """質問群を group_key ごとにスコア合計。"""
    scores: dict[Any, float] = {}
    if default_keys:
        scores = {key: 0.0 for key in default_keys}

    for question in questions:
        qid = question["id"]
        if qid not in answers:
            continue
        value = normalize_answer(answers[qid], options_map, scale_max)
        if value is None:
            continue
        key = question.get(group_key)
        scores[key] = scores.get(key, 0.0) + question_score(question, value, scale_max)

    return scores


def rank_desc(scores: dict[str, float]) -> list[tuple[str, float]]:
    """スコア降順ランキング。"""
    return sorted(scores.items(), key=lambda item: (-item[1], item[0]))
