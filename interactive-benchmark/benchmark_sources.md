# benchmark_sources

## Core rule

這個專案使用混合式 benchmark：

- public benchmark：拿來做外部對照
- product benchmark：拿來測自己的產品能力

不要只借公共 benchmark，也不要全自己亂造。

---

## Public benchmark mapping

### state_consistency
- borrow: ConStory-Bench
- custom: branching state transition / save-load consistency / world-state persistence

### long_memory
- borrow: LongMemEval, LoCoMo
- custom: memory overwrite / fact invalidation / cross-branch recall

### reaction_coherence
- borrow: PERMA
- custom: emotion continuity / initiative continuity / role reaction tests

### tension_retention
- borrow: narrative planning benchmark
- custom: open-loop survival / premature payoff / pivot density / novelty budget

### sensory_rendering
- mostly custom
- custom: sensory channel coverage / causal linkage to state / hollow adjective density

---

## Execution order

1. 先把 product benchmark 跑穩
2. 再接 public benchmark 的最小子集
3. 先接 LongMemEval
4. 再接 PERMA
5. 再接 ConStory-Bench
6. 最後再考慮 LoCoMo 這種更長的壓力測試

---

## Current principle

- public benchmark 不要一次全接
- 只接和本專案 metric 直接對應的部分
- product benchmark 才是主體
