# /src/ui

## 責務

画面表示・入力処理。Web UI / CLI、選択肢表示、サイのメッセージ表示。

## 役割

- **core と dialogue の唯一の接合点（Orchestrator）**
- core の診断結果を dialogue に渡す
- ユーザー入力を core / dialogue に振り分ける

## ファイル

| ファイル | 内容 |
|---------|------|
| `ROLE.md` | 本ファイル |
| `orchestrator.md` | core ↔ dialogue 橋渡し仕様 |
| `cli.md` | CLI 仕様 |
| `web.md` | Web UI 仕様 |

## 依存

- **参照可**: `src/core/`, `src/dialogue/`, `src/utils/`, `config/`, `data/`
