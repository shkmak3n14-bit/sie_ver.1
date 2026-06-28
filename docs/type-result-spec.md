# core 出力スキーマ — ui → dialogue 橋渡し用

module: type_engine
version: "0.1.0"

fields:
  primary_type: { type: integer, min: 1, max: 9 }
  wing_label: { type: string, example: "3w2" }
  type_candidates: { type: array, maxItems: 3 }
  dominant_center: { enum: [gut, heart, head] }
  confidence: { enum: [high, medium, low] }
  type_scores: { type: object }

note: dialogue はこの構造のみ受け取り、スコア再計算しない
