# /src/core/type_engine

## 責務

135問 + center + wing + episode の回答を統合し、最終タイプを決定する。

## ファイル

| ファイル | 内容 |
|---------|------|
| **`type_engine.yaml`** | 統合ロジック仕様書 |
| **`type_engine.py`** | 計算実装（CLI 付き） |
| `pipeline.yaml` | パイプライン定義（レガシー参照） |

## 実行

```bash
pip install -r requirements.txt
python src/core/type_engine/type_engine.py --answers examples/sample_answers_partial.json
```

## 参照

- `../scoring/scoring.yaml` — スコアリング・補正ルール
- `../questions/` — 質問データ

## 依存

- **参照可**: scoring, questions, center_engine, wing_engine, episode_analysis
- **参照禁止**: `src/dialogue/`, `src/models/`

## 返却値

`main_type`, `candidates`, `raw_scores`, `adjusted_scores`, `center_result`, `wing_result`, `episode_result`, `confidence`, `wing_label`
