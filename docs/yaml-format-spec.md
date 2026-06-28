# 質問データ YAML フォーマット仕様

S.I.E の質問データは `src/core/questions/` 配下の YAML で管理する。
**core（診断）と dialogue（対話）は独立** — 質問 YAML は core のみが参照する。

---

## 1. タイプ別質問（type1.yaml 〜 type9.yaml）

135問の本体。各タイプ15問。

```yaml
meta:
  version: "0.1.0"
  kind: type              # type | center | wing
  type_id: 1              # 1〜9（center/wing の場合は null）
  type_name: "改革する人"
  center: gut             # gut | heart | head
  question_count: 15

scale:
  min: 0
  max: 3
  labels:
    0: "全く当てはまらない"
    1: "あまり当てはまらない"
    2: "やや当てはまる"
    3: "非常に当てはまる"

questions:
  - id: T1_01
    text: "物事には正しいやり方があると感じることが多い"
    dimension: core       # core | defense | fear | desire
    weight: 1.0           # scoring/weights.yaml 参照可
    reverse_scored: false # true の場合 (max - answer) で数値化

  - id: T1_02
    text: "ミスや不正を見ると、放っておけない"
    dimension: defense
    weight: 1.2
    reverse_scored: false
```

### フィールド定義

| フィールド | 必須 | 説明 |
|-----------|------|------|
| `meta.version` | ○ | スキーマバージョン |
| `meta.kind` | ○ | `type` / `center` / `wing` |
| `meta.type_id` | △ | タイプ番号（type のみ必須） |
| `meta.center` | ○ | 所属センター |
| `scale.min` / `scale.max` | ○ | 回答の数値範囲（既定 0〜3） |
| `questions[].id` | ○ | 一意ID（例: `T1_01`, `C_01`, `W_01`） |
| `questions[].text` | ○ | 質問文 |
| `questions[].dimension` | ○ | 重みカテゴリ（core/defense/fear/desire） |
| `questions[].weight` | ○ | 質問ごとの重み係数 |
| `questions[].reverse_scored` | ○ | 逆転採点フラグ |

---

## 2. センター判定質問（center.yaml）

本能・思考・感情の判定用。**センターを先に決めない** — スコアは type_engine で統合する。

```yaml
meta:
  version: "0.1.0"
  kind: center
  question_count: 12      # 例: 各センター4問

scale:
  min: 0
  max: 3

questions:
  - id: C_GUT_01
    text: "境界を侵されると、すぐ反応する"
    center: gut
    dimension: core
    weight: 1.0
    reverse_scored: false

  - id: C_HEART_01
    text: "認められないと、自分の価値を疑う"
    center: heart
    dimension: core
    weight: 1.0
    reverse_scored: false

  - id: C_HEAD_01
    text: "不確実な状況は、不安を感じやすい"
    center: head
    dimension: core
    weight: 1.0
    reverse_scored: false
```

---

## 3. w（ウィング）判定質問（wing.yaml）

タイプ確定**後**に wing_engine が参照する補助質問。

```yaml
meta:
  version: "0.1.0"
  kind: wing
  question_count: 18      # 例: タイプ境界ごとに2問

scale:
  min: 0
  max: 3

questions:
  - id: W_1_9
    text: "正しさより、まず関係の平和を選びたい"
    primary_type: 1
    wing_type: 9
    dimension: core
    weight: 1.0
    reverse_scored: false

  - id: W_1_2
    text: "正しいことをするために、人の役に立ちたい"
    primary_type: 1
    wing_type: 2
    dimension: core
    weight: 1.0
    reverse_scored: false
```

---

## 4. 質問マスタインデックス（index.yaml）

```yaml
meta:
  version: "0.1.0"
  total_type_questions: 135
  total_center_questions: 0   # center.yaml の実数に合わせる
  total_wing_questions: 0     # wing.yaml の実数に合わせる

files:
  types:
    - { type_id: 1, file: type1.yaml }
    - { type_id: 2, file: type2.yaml }
    # ... type9.yaml
  center: center.yaml
  wing: wing.yaml

load_order:
  - types          # type1 → type9
  - center
  - wing           # wing は type_engine 確定後に wing_engine が読む
```

---

## 5. 回答データ（/data 保存形式）

```yaml
session_id: "uuid"
answers:
  T1_01: 2
  T1_02: 3
  C_GUT_01: 1
  # ...
episodes: []   # episode_analysis 用（任意）
```

---

## 6. dimension（重みカテゴリ）

| 値 | 意味 | 参照 |
|----|------|------|
| `core` | コアタイプの本質 | `src/core/scoring/weights.yaml` |
| `defense` | 防衛機制 | 同上 |
| `fear` | 基本恐れ | 同上 |
| `desire` | 基本欲望 | 同上 |
