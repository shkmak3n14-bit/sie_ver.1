# /src/utils

## 責務

core / dialogue 双方から利用可能な共通処理（依存方向に注意）。

| モジュール | 内容 |
|-----------|------|
| `yaml_loader.py` | YAML / JSON 読み込み |
| `scoring_helpers.py` | 回答正規化・質問スコア・グループ集計 |

## 依存ルール

- utils は **core も dialogue も import しない**
- core / dialogue / ui から utils を呼ぶ一方向のみ
