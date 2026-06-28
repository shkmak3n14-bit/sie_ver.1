# /src/core/center_engine

## 責務

center.yaml の回答から instinct / thinking / feeling の判定結果を返す。
**補正の適用は type_engine の責務** — 本モジュールは判定のみ。

## ファイル

| ファイル | 内容 |
|---------|------|
| **`center_engine.py`** | センター判定実装 |

## 実行

```bash
python src/core/center_engine/center_engine.py --answers examples/sample_answers_partial.json
```

## 返却値

```json
{
  "primary_center": "instinct",
  "scores": { "instinct": 12, "thinking": 8, "feeling": 6 },
  "ranking": [{ "center": "instinct", "score": 12 }, ...]
}
```

## 依存

- `src/utils/` — YAML 読み込み・スコア集計
- `src/core/questions/center.yaml`

