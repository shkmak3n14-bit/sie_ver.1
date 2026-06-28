# S.I.E Agent ルーティング

このリポジトリで作業するとき、**モジュールごとに Context を切り替える**。

## モジュール選択

| やりたいこと | 読む Context | 人格 |
|-------------|-------------|------|
| 120問診断・スコア算出 | `core/type_engine/CONTEXT.md` | なし |
| 診断結果の深掘り | `dialogue/personality/sie_persona.md` + `dialogue/self_understanding/CONTEXT.md` | サイ |
| 相手の理解 | persona + `dialogue/other_understanding/CONTEXT.md` | サイ |
| 関係調整 | persona + `dialogue/relationship/CONTEXT.md` | サイ |

## データの流れ

```
questions/*.yaml → type_engine → type_result.schema.yaml
                                      ↓
                              self_understanding → self_profile.schema.yaml
                                      ↓
episodes → other_understanding → other_profile.schema.yaml
                                      ↓
                              relationship → relationship_plan.schema.yaml
```

## 設定

全体定義: `config/sie.yaml`

## 注意

- type_engine と dialogue を**同一セッションで混在させない**（診断中は人格オフ）
- 質問文の変更は `core/type_engine/questions/` の YAML のみ編集
