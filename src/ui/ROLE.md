# Streamlit UI 起動

プロジェクトルートで実行:

```bash
pip install -r requirements.txt
streamlit run src/ui/main.py
```

## 役割

`main.py` は **司令塔（orchestrator）** のみ。

| 層 | 呼び出し |
|----|---------|
| core | `run_type_engine`, `run_center_engine`, `run_wing_engine`, `run_episode_engine` |
| dialogue | `load_persona`, `load_flow` |
| utils | `load_yaml_file`, `load_all_type_questions` |

ロジック本体は core / dialogue に分離したまま。
