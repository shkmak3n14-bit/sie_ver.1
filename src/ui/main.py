"""
S.I.E Streamlit UI — 司令塔（orchestrator）

core（診断）と dialogue（対話）を橋渡しする。
ロジック本体は各 engine / flow / persona に委譲する。
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
for path in (ROOT, SRC):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

import streamlit as st

from src.core.center_engine.center_engine import run_center_engine
from src.core.episode_analysis.episode_engine import run_episode_engine
from src.core.type_engine.type_engine import run_type_engine
from src.core.wing_engine.wing_engine import run_wing_engine
from src.dialogue.flow.flow_loader import load_flow
from src.dialogue.persona.persona import load_persona
from src.utils.yaml_loader import load_all_type_questions, load_questions_by_category

DEFAULT_OPTIONS = ["ほとんどない", "たまにある", "よくある", "ほぼいつもそう"]

# -----------------------------
# Streamlit 初期設定
# -----------------------------
st.set_page_config(page_title="S.I.E（サイ）診断", layout="wide")

# -----------------------------
# セッション初期化
# -----------------------------
if "phase" not in st.session_state:
    st.session_state.phase = "intro"

if "answers" not in st.session_state:
    st.session_state.answers = {}

if "persona" not in st.session_state:
    st.session_state.persona = load_persona()

if "diagnosis_step" not in st.session_state:
    st.session_state.diagnosis_step = 0

if "type_result" not in st.session_state:
    st.session_state.type_result = None


# -----------------------------
# サイのメッセージ表示
# -----------------------------
def sie_message(text: str) -> None:
    persona = st.session_state.persona
    tone = persona["tone"]["base"]
    st.markdown(f"**サイ（{tone}）:** {text}")


def render_flow_steps(flow: list[dict], key_prefix: str) -> None:
    """対話フローの message / suggestion / question を表示。"""
    for i, step in enumerate(flow):
        speaker = step.get("speaker", "SIE")
        text = step.get("text", "")
        step_type = step.get("type", "message")

        if speaker == "SIE":
            sie_message(text)
        else:
            st.write(text)

        if step_type == "question" and step.get("options"):
            st.radio(
                "選択してください",
                step["options"],
                key=f"{key_prefix}_{step['id']}_{i}",
            )


def render_scale_questions(questions: list[dict], key_prefix: str) -> None:
    """リッカート尺度の質問群を表示。"""
    for q in questions:
        options = q.get("options") or DEFAULT_OPTIONS
        st.markdown(f"**{q['id']}** — {q['text']}")
        answer = st.radio(
            "選択してください",
            options,
            key=f"{key_prefix}_{q['id']}",
            label_visibility="collapsed",
        )
        st.session_state.answers[q["id"]] = answer


def render_episode_questions(questions: list[dict]) -> None:
    """幼少期エピソード（自由記述）を表示。"""
    for q in questions:
        st.markdown(f"**{q['id']}** — {q['text']}")
        answer = st.text_area(
            "自由記述",
            key=f"episode_{q['id']}",
            label_visibility="collapsed",
        )
        if answer:
            st.session_state.answers[q["id"]] = answer


# -----------------------------
# フローのロード
# -----------------------------
intro_flow = load_flow("intro")
self_flow = load_flow("self_understanding")
other_flow = load_flow("other_understanding")
relation_flow = load_flow("relationship")


# -----------------------------
# 診断フェーズ（type → center → wing → episode）
# -----------------------------
DIAGNOSIS_STEPS = [
    ("type", "タイプ診断（135問）", load_all_type_questions),
    ("center", "センター判定（15問）", lambda: load_questions_by_category("center")),
    ("wing", "ウイング判定（54問）", lambda: load_questions_by_category("wing")),
    ("episode", "幼少期エピソード（10問）", lambda: load_questions_by_category("episode")),
]


def run_diagnosis() -> None:
    sie_message("診断を開始するよ。ゆっくり答えてね。")

    step_idx = st.session_state.diagnosis_step
    step_id, step_label, loader = DIAGNOSIS_STEPS[step_idx]

    st.subheader(f"ステップ {step_idx + 1}/{len(DIAGNOSIS_STEPS)}: {step_label}")

    if step_id == "type":
        type_index = st.session_state.get("type_batch", 0)
        all_type = loader()
        batch_size = 15
        start = type_index * batch_size
        end = start + batch_size
        batch = all_type[start:end]
        type_num = type_index + 1

        st.caption(f"タイプ {type_num} / 9（15問）")
        render_scale_questions(batch, f"type{type_num}")

        col1, col2 = st.columns(2)
        with col1:
            if type_index > 0 and st.button("前のタイプへ"):
                st.session_state.type_batch = type_index - 1
                st.rerun()
        with col2:
            if type_index < 8 and st.button("次のタイプへ"):
                st.session_state.type_batch = type_index + 1
                st.rerun()
            elif type_index == 8 and st.button("センター判定へ"):
                st.session_state.diagnosis_step += 1
                st.rerun()

    elif step_id == "center":
        render_scale_questions(loader(), "center")
        if st.button("ウイング判定へ"):
            st.session_state.diagnosis_step += 1
            st.rerun()

    elif step_id == "wing":
        wing_index = st.session_state.get("wing_batch", 0)
        all_wing = loader()
        batch_size = 9
        start = wing_index * batch_size
        batch = all_wing[start : start + batch_size]
        st.caption(f"ウイング質問 {wing_index + 1} / 6")
        render_scale_questions(batch, f"wing{wing_index}")

        col1, col2 = st.columns(2)
        with col1:
            if wing_index > 0 and st.button("前へ"):
                st.session_state.wing_batch = wing_index - 1
                st.rerun()
        with col2:
            if wing_index < 5 and st.button("次へ"):
                st.session_state.wing_batch = wing_index + 1
                st.rerun()
            elif wing_index == 5 and st.button("エピソードへ"):
                st.session_state.diagnosis_step += 1
                st.rerun()

    elif step_id == "episode":
        render_episode_questions(loader())
        if st.button("診断結果を見る"):
            answers = st.session_state.answers
            st.session_state.type_result = {
                "type": run_type_engine(answers),
                "center": run_center_engine(answers),
                "wing": run_wing_engine(answers),
                "episode": run_episode_engine(answers),
            }
            st.session_state.phase = "self"
            st.rerun()


# -----------------------------
# 自己理解フェーズ
# -----------------------------
def run_self_understanding() -> None:
    sie_message("まずは自分のパターンを一緒に見ていこう。")

    result = st.session_state.type_result
    if result:
        type_res = result["type"]
        st.json(
            {
                "main_type": type_res.get("main_type"),
                "candidates": type_res.get("candidates"),
                "wing_label": type_res.get("wing_label"),
                "confidence": type_res.get("confidence"),
            }
        )

    render_flow_steps(self_flow, "self")

    if st.button("次へ（他者理解）"):
        st.session_state.phase = "other"
        st.rerun()


# -----------------------------
# 他者理解フェーズ
# -----------------------------
def run_other_understanding() -> None:
    sie_message("次は、理解したい相手について教えてほしい。")
    render_flow_steps(other_flow, "other")

    if st.button("次へ（相互理解）"):
        st.session_state.phase = "relation"
        st.rerun()


# -----------------------------
# 相互理解フェーズ
# -----------------------------
def run_relationship() -> None:
    sie_message("関係をどう整えるか、一緒に考えていこう。")
    render_flow_steps(relation_flow, "relation")
    st.success("これで全てのフェーズが完了したよ。")


# -----------------------------
# メイン処理
# -----------------------------
st.title("S.I.E — Support Intelligence on Ego（サイ）")

if st.session_state.phase == "intro":
    render_flow_steps(intro_flow, "intro")
    if st.button("診断を始める"):
        st.session_state.phase = "diagnosis"
        st.session_state.diagnosis_step = 0
        st.session_state.type_batch = 0
        st.session_state.wing_batch = 0
        st.rerun()

elif st.session_state.phase == "diagnosis":
    run_diagnosis()

elif st.session_state.phase == "self":
    run_self_understanding()

elif st.session_state.phase == "other":
    run_other_understanding()

elif st.session_state.phase == "relation":
    run_relationship()
