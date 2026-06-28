# /src

## 責務

S.I.E（サイ）アプリケーション本体。診断ロジックと対話ロジックを完全分離する。

```
src/
├── core/       … 診断エンジン（頭脳）— dialogue 非依存
├── dialogue/   … 人格・対話（声）— core 非依存
├── models/     … 18種 w 人格モデル — dialogue 用
├── utils/      … 共通処理
└── ui/         … 表示・入力・core↔dialogue 接合
```

## 依存関係

```
ui ──→ core
ui ──→ dialogue
dialogue ──→ models
core ✗ dialogue  （相互非依存）
```
