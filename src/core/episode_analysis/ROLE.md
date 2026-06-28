# /src/core/episode_analysis

## 責務

幼少期エピソードのテキスト解析、感情・行動パターン抽出、タイプ補正への反映。

## ファイル

| ファイル | 内容 |
|---------|------|
| `rules.yaml` | 解析・補正ルール |
| `signals.yaml` | タイプ別シグナルキーワード |
| `../questions/episode_analysis.yaml` | 幼少期エピソード構造化質問（10問） |

## 依存

- **参照可**: `src/core/scoring/`, `src/core/type_engine/`
- **参照禁止**: `src/dialogue/`
