# /src/core/wing_engine

## 責務

wing.yaml の回答から 18種ウイング（1w9〜9w1）の判定結果を返す。
**補正の適用は type_engine の責務** — 本モジュールは判定のみ。

## ファイル

| ファイル | 内容 |
|---------|------|
| **`wing_engine.py`** | ウイング判定実装 |
| `wings.yaml` | タイプ別隣接ウィング定義（参考） |
| `correction.yaml` | 補正ルール（type_engine が参照） |

## 実行

```bash
python src/core/wing_engine/wing_engine.py --answers examples/sample_answers_partial.json
```

## 返却値

```json
{
  "primary_wing": "7w6",
  "scores": { "1w9": 3, "7w6": 12, ... },
  "ranking": [{ "wing": "7w6", "score": 12 }, ...]
}
```

## 依存

- `src/utils/` — YAML 読み込み・スコア集計
- `src/core/questions/wing.yaml`

