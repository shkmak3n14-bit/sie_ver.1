"""診断結果テンプレート（persona_result）の Streamlit 表示。"""

from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any

import streamlit as st

from src.models.results.result_loader import load_type_result, merge_engine_into_template

DEBUG_LOG_PATH = Path(__file__).resolve().parents[2] / "debug-7cf15b.log"


def _debug_log(location: str, message: str, data: dict, hypothesis_id: str) -> None:
    # #region agent log
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


def _text_block(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def render_persona_result(
    type_res: dict[str, Any],
    center_res: dict[str, Any] | None = None,
) -> None:
    """persona_result テンプレートを診断結果として表示。"""
    main_type = int(type_res.get("main_type") or 1)
    wing_label = type_res.get("wing_label") or "—"

    # #region agent log
    _debug_log(
        "result_view.py:render_persona_result",
        "loading type result template",
        {
            "main_type": main_type,
            "wing_label": wing_label,
            "template_file": f"type{main_type}_result.yaml",
        },
        "DISPLAY",
    )
    # #endregion

    template = load_type_result(main_type)
    persona = merge_engine_into_template(template, type_res, center_res)
    diagnosis = persona.get("_diagnosis", {})

    st.subheader("診断結果")
    st.markdown(
        f"**{persona.get('type_name', '')}** "
        f"（タイプ {persona.get('type_number', main_type)} / ウイング {wing_label}）"
    )
    st.caption(
        f"確信度: {diagnosis.get('confidence', '—')} ｜ "
        f"候補: {diagnosis.get('candidates', [])} ｜ "
        f"センター: {diagnosis.get('dominant_center', '—')}"
    )

    st.markdown("#### 概要")
    st.markdown(_text_block(persona.get("summary_200")))

    center = persona.get("center") or {}
    st.markdown("#### センター")
    st.markdown(f"**{center.get('name', '')}**")
    st.markdown(_text_block(center.get("reason")))

    wing = persona.get("wing") or {}
    st.markdown("#### ウイング")
    st.markdown(f"**{wing.get('wing_type', wing_label)}**")
    st.markdown(_text_block(wing.get("influence")))

    values = persona.get("values") or {}
    st.markdown("#### 価値観")
    st.markdown("**大切にしていること**")
    st.markdown(_text_block(values.get("important")))
    st.markdown("**レッドライン**")
    st.markdown(_text_block(values.get("red_line")))

    st.markdown("#### 認知のクセ")
    st.markdown(_text_block(persona.get("cognitive_pattern")))

    st.markdown("#### 幼少期のコアストーリー")
    st.markdown(_text_block(persona.get("childhood_story")))

    st.markdown("#### 他者からの印象")
    st.markdown(_text_block(persona.get("external_impression")))

    arrows = persona.get("integration_disintegration") or {}
    st.markdown("#### 成長・退行（矢印）")
    st.markdown(f"- 成長の矢: {arrows.get('growth_arrow', '')}")
    st.markdown(f"- ストレスの矢: {arrows.get('stress_arrow', '')}")
    st.markdown(_text_block(arrows.get("explanation")))

    st.markdown("#### 好循環 / 悪循環")
    st.markdown("**好循環**")
    st.markdown(_text_block(persona.get("good_cycle")))
    st.markdown("**悪循環**")
    st.markdown(_text_block(persona.get("bad_cycle")))
    st.markdown(f"好循環スコア: {persona.get('good_cycle_score', 0)}")

    st.markdown("#### 強みの活かし方")
    st.markdown(_text_block(persona.get("strength_usage")))

    comm = persona.get("communication") or {}
    st.markdown("#### コミュニケーション")
    st.markdown("**相性の良いスタイル**")
    st.markdown(_text_block(comm.get("good_style")))
    st.markdown("**相性の悪いスタイル**")
    st.markdown(_text_block(comm.get("bad_style")))

    st.markdown("#### 好転のためのアドバイス")
    st.markdown(_text_block(persona.get("advice")))

    maturity = persona.get("maturity_level") or {}
    st.markdown("#### 成熟度")
    st.markdown(f"**{maturity.get('level', '')}**")
    st.markdown(_text_block(maturity.get("description")))

    with st.expander("診断エンジン詳細（JSON）"):
        st.json(type_res)
