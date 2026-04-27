
# Interactive Benchmark Prototype

這個專案是在做一個**長回合互動系統的 benchmark 骨架**。  
核心目標是先驗證：
1. 狀態維持  
2. 記憶讀寫
3. 情節熱寂  
4. 角色一致性  
5. 後端能不能穩定跑 benchmark

---

## 目前做到哪裡

現在這個 repo 是 **v0 骨架**，重點是先把 benchmark pipeline 跑通。

目前有：

- `benchmark_spec.md`：benchmark 規格草稿
- `src/state_schema.py`：canonical state 的最小結構
- `src/event_schema.py`：每輪 event record 結構
- `src/judge.py`：規則式 placeholder judge
- `src/run_benchmark.py`：benchmark runner
- `scenarios/`：scenario 測試案例
- `outputs/`：benchmark 輸出結果

目前還沒有：

- 真正的 planner / solver
- 真正的 memory manager
- 真正的 LLM judge
- 正式前端
- Runpod 自動部署流程

也就是說，**現在是 benchmark skeleton，不是成品系統**。

---

## 這個專案在做什麼

這不是一般聊天機器人。  
比較接近：

- 一個有狀態的互動引擎
- 一個可以長回合測試的 benchmark runner
- 未來可能接文字冒險前端的後端核心

目前設計方向是：

- `state tracker` 當唯一真相來源
- `planner / solver / renderer` 分工
- `memory` 用事件化方式寫入
- `judge` 對 session 做評分

---

## 專案結構

```text
project/
  README.md
  requirements.txt
  benchmark_spec.md
  .gitignore

  src/
    state_schema.py
    event_schema.py
    state_tracker.py
    planner.py
    renderer.py
    judge.py
    run_benchmark.py

  scenarios/
    scenario_001.yaml
    scenario_002.yaml

  outputs/