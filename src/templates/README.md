# S.I.E YAML テンプレート一覧

core（診断）と dialogue（対話）の**双方から参照**する統一テンプレート。

## 質問データ（診断）

| ファイル | 用途 |
|---------|------|
| `question.item.template.yaml` | **1問分**の原子テンプレート（全 category 共通） |
| `question.template.yaml` | **ファイル単位**（meta + questions 配列） |
| `question.type.template.yaml` | type1〜type9（15問×9） |
| `question.center.template.yaml` | センター判定（instinct/thinking/feeling） |
| `question.wing.template.yaml` | w判定（18種: 1w9 〜 9w1） |

## 対話フロー

| ファイル | 用途 |
|---------|------|
| `dialogue.item.template.yaml` | **1件分**の原子テンプレート |
| `dialogue.template.yaml` | **ファイル単位**（meta + flow 配列） |

## 人格モデル

| ファイル | 用途 |
|---------|------|
| `persona.template.yaml` | models/ の 18種 w プロファイル |

## 配置先

```
src/core/questions/     ← question.*.template をコピー
src/dialogue/flow/      ← dialogue.template をコピー
src/models/             ← persona.template をコピー
```

## 仕様書

`docs/yaml-template-spec.md`
