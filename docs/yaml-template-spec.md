# YAML テンプレート仕様書 v0.2.0

S.I.E のすべての質問・対話・人格データを統一フォーマットで管理する。
テンプレート実体: `src/templates/`

**core と dialogue の双方から参照可能。** 診断ロジックと対話ロジックは相互非依存のまま、データ形式のみ共通化する。

---

## 1. 診断質問（原子テンプレート）

type1〜9 / center / wing / dialogue 内の埋め込み質問はすべてこの形式。

```yaml
id: q001
category: type                  # type | center | wing | dialogue
type_number: 1                  # 下表参照
text: "ここに質問文を入れる"
options:
  - "ほとんどない"
  - "たまにある"
  - "よくある"
  - "ほぼいつもそう"
weight:
  core: 1.0                     # 核心動機
  fear: 1.0                     # 恐れ
  desire: 1.0                   # 欲求
  defense: 1.0                  # 防衛パターン
tags:
  - "self"
  - "childhood"
  - "emotion"
next: null                      # 分岐時のみ次の質問ID
```

### category 別 type_number

| category | type_number の値 | 例 |
|----------|-----------------|-----|
| `type` | 整数 1〜9 | `1` |
| `center` | `instinct` / `thinking` / `feeling` | `instinct` |
| `wing` | 文字列 `"NwM"` | `"1w9"` |
| `dialogue` | フェーズ名 | `self_understanding` |

### 拡張フィールド（任意）

| フィールド | 型 | 説明 |
|-----------|-----|------|
| `reverse_scored` | bool | 選択肢インデックスを反転採点 |
| `required` | bool | 必須回答（default: true） |
| `branch.condition` | string | 分岐条件（将来拡張） |
| `branch.true_next` | string | 条件成立時の next |
| `branch.false_next` | string | 条件不成立時の next |

### スコア計算（core 参照）

```
score = options_index × weight.{core|fear|desire|defense}
# reverse_scored: (3 - index) × weight.*
```

---

## 2. 診断質問（ファイル単位）

```yaml
meta:
  version: "0.2.0"
  template: question.type       # question.type | question.center | question.wing
  category: type
  type_number: 1
  question_count: 15
  default_options: [...]        # options: null 時に継承
  default_weight: { core: 1.0, fear: 1.0, desire: 1.0, defense: 1.0 }

questions:
  - id: T1_01
    category: type
    type_number: 1
    text: "..."
    options: null
    weight: { core: 1.0, fear: 1.0, desire: 1.0, defense: 1.0 }
    tags: ["self"]
    next: T1_02
```

### ファイル対応

| 配置 | テンプレート | 問数 |
|------|-------------|------|
| `src/core/questions/type1.yaml` | `question.type.template.yaml` | 15 |
| `src/core/questions/center.yaml` | `question.center.template.yaml` | 任意 |
| `src/core/questions/wing.yaml` | `question.wing.template.yaml` | 18 |

---

## 3. 対話フロー（原子テンプレート）

```yaml
id: intro_001
speaker: SIE
text: "やあ、サイだよ。今日はエニアグラムを使って、君のパターンを一緒に見ていこう。"
type: message                   # message | question | suggestion
options: null                   # question のみ選択肢配列
next: intro_002
```

### type の意味

| type | options | 用途 |
|------|---------|------|
| `message` | null | サイの発話・説明 |
| `question` | 配列 | ユーザーへの質問 |
| `suggestion` | null | 提案・リフレーム |

### ファイル単位

```yaml
meta:
  version: "0.2.0"
  template: dialogue.file
  phase: intro                  # intro | self_understanding | other_understanding | relationship

flow:
  - id: intro_001
    speaker: SIE
    text: "..."
    type: message
    options: null
    next: intro_002
```

配置: `src/dialogue/flow/{phase}.yaml`

---

## 4. 人格モデル

```yaml
id: persona_1w9
type: "1w9"
core_traits:
  - "正しさを重視"
  - "怒りを抑える"
  - "穏やかさを求める"
stress_pattern:
  - "自己批判"
growth_pattern:
  - "柔軟性"
dialogue_style:
  greeting: "ごきげんよう、章男さん"
  tone: "落ち着いたK.I.T.T.風"
  humor_rate: 0.12
```

配置: `src/models/1w9.yaml` 等（18ファイル）

---

## 5. ID 命名規則

| 種別 | 形式 | 例 |
|------|------|-----|
| タイプ質問 | `T{n}_{nn}` | `T1_01` |
| センター | `C_{center}_{nn}` | `C_instinct_01` |
| ウィング | `W_{n}w{m}` | `W_1w9` |
| 対話 | `{phase}_{nnn}` | `intro_001`, `self_001` |
| 人格 | `persona_{n}w{m}` | `persona_1w9` |

---

## 6. core / dialogue 参照ルール

| データ | core | dialogue |
|--------|------|----------|
| question.type/center/wing | ○ スコアリング | × |
| dialogue.flow | × | ○ 誘導・表示 |
| persona | × | ○ 口調・traits |
| question.item（dialogue内） | △ 任意 | ○ 自己理解等 |

**橋渡し**: `src/ui/orchestrator.md` — core 出力を dialogue に渡す。

---

## 7. タグ一覧（推奨）

```
self, other, childhood, emotion, behavior, relationship,
gut, heart, head, wing, mismatch, values, red_line, cycle
```

---

## 8. テンプレートファイル一覧

```
src/templates/
├── question.item.template.yaml    # 診断1問（共通）
├── question.template.yaml         # 診断ファイル
├── question.type.template.yaml
├── question.center.template.yaml
├── question.wing.template.yaml
├── dialogue.item.template.yaml    # 対話1件
├── dialogue.template.yaml         # 対話ファイル
└── persona.template.yaml          # 人格モデル
```
