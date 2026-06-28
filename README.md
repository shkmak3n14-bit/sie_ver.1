# S.I.E — Support Intelligence on Ego（サイ）

エニアグラム性格診断・カウンセリング AI のノーコード構成。

## フォルダ構成

```
sie_ver.1/
├── src/
│   ├── core/                  # 診断エンジン（dialogue 非依存）
│   │   ├── questions/         # 135問 + center + wing（YAML）
│   │   ├── scoring/
│   │   ├── type_engine/
│   │   ├── center_engine/
│   │   ├── wing_engine/
│   │   └── episode_analysis/
│   ├── dialogue/              # 対話・人格（core 非依存）
│   │   ├── persona/
│   │   ├── flow/
│   │   └── templates/
│   ├── models/                # 18種 w 人格モデル
│   ├── utils/
│   └── ui/                    # core ↔ dialogue 接合
├── tests/
├── docs/
├── config/
└── data/                      # ユーザー回答（gitignore）
```

## 依存関係

```
ui → core
ui → dialogue → models
core ✗ dialogue  （相互非依存）
```

## ドキュメント

- **YAML テンプレート仕様**: `docs/yaml-template-spec.md`
- テンプレート実体: `src/templates/`
- 診断仕様: `docs/diagnosis-logic-spec.md`
- サイ人格: `docs/sie-persona-spec.md`

各フォルダの `ROLE.md` に責務を記載。
