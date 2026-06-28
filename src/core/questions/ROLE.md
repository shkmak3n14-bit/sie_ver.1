# /src/core/questions

## 責務

135問（タイプ別15問×9）、センター判定質問、w判定質問を YAML で管理する。

## ファイル

| ファイル | 内容 |
|---------|------|
| `_template.yaml` | 質問データの雛形 |
| `index.yaml` | マスタインデックス・読み込み順 |
| `type1.yaml` 〜 `type9.yaml` | タイプ別15問 |
| `center.yaml` | センター判定質問 |
| `wing.yaml` | w判定質問（タイプ確定後） |

## 依存

- **参照可**: `src/core/scoring/`
- **参照禁止**: `src/dialogue/`（対話ロジック）
