# /src/dialogue/persona

## 責務

サイの人格設定。口調・冗談頻度・気遣い・否定しない姿勢を YAML で管理する。

## ファイル

| ファイル | 内容 |
|---------|------|
| `persona.yaml` | **マスタ** — 対話フロー共通参照 |
| `sie_persona.yaml` | 旧形式（後方互換・`persona.yaml` へ移行） |

## 参照

- 対話フロー: `src/dialogue/flow/*.yaml` → `flow_reference` セクション
- 設定: `config/persona.yaml`

## 依存

- **参照禁止**: `src/core/`
