# /src/core/scoring

## 責務

質問回答のスコアリング、重み付け（core / defense / fear / desire）、選択肢の数値化（0〜3）。
タイプ集計・センター補正・ウイング補正・エピソード補正・最終タイプ決定。

## ファイル

| ファイル | 内容 |
|---------|------|
| **`scoring.yaml`** | **マスタ** — スコアリング仕様全体 |
| `weights.yaml` | dimension 別デフォルト重み（scoring.yaml 参照） |
| `rules.yaml` | 基本ルール（scoring.yaml 参照） |

## 参照

- `type_engine/pipeline.yaml` → `scoring.yaml#pipeline`
- 質問データ: `src/core/questions/`

## 依存

- **参照可**: `src/core/questions/`
- **参照禁止**: `src/dialogue/`
