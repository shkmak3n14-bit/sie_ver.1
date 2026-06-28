# /src/models

## 責務

人格モデル（18種類）。診断後の対話に使用する w 組み合わせ別プロファイル。

## ファイル

`{type}w{wing}.yaml` — 計18ファイル（各タイプ2ウィング）

## 依存

- **参照可**: `src/dialogue/` のみ
- **参照禁止**: `src/core/`（core の出力 JSON/YAML を dialogue が models に橋渡し）
