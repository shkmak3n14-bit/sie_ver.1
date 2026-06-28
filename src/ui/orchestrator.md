# Orchestrator — core ↔ dialogue 橋渡し

flow:
  1. ui が questions を表示（dialogue/flow/questioning.yaml）
  2. 回答を core/type_engine に渡し診断実行
  3. 診断結果（JSON/YAML）を dialogue/flow に渡す
  4. dialogue が persona + models で対話生成
  5. ui がサイのメッセージを表示

boundary:
  core_output_schema: "docs/type-result-spec.md"
  dialogue_input: "structured_result_only"
