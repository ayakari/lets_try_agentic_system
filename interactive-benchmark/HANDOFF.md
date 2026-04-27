# Handoff

## 1. Project
Interactive Benchmark Prototype

## 2. One-line summary
This project is a benchmark skeleton for a long-turn interactive system. The current priority is backend benchmark reliability, not frontend polish.

## 3. Current stage
benchmark_skeleton

## 4. What has been completed
- Git project initialized
- GitHub repo created and pushed
- Basic project structure created
- README added
- benchmark_spec.md added
- Minimal canonical state schema added
- Minimal event schema added
- Placeholder judge added
- Benchmark runner can scan scenarios and output JSON results
- scenario_001.yaml exists
- scenario_002.yaml exists

## 5. What is not done yet
- No real planner
- No real solver
- No real state update logic
- No event-based memory manager
- No LLM judge
- No proper ablation
- No frontend
- No Runpod execution workflow script yet

## 6. Key decisions
- Backend first, frontend later
- Benchmark first, product shell later
- Canonical state is the single source of truth
- Runpod is only an execution node, not the source of truth
- Git repo stores code/specs/prompts/scenarios
- Large artifacts, models, logs, and outputs should not be committed into git
- Text-adventure style frontend is the most promising later frontend
- Kobold-like frontend can be used later as a shell only, not as the memory/state core

## 7. Important files
- README.md
- benchmark_spec.md
- src/state_schema.py
- src/event_schema.py
- src/judge.py
- src/run_benchmark.py
- scenarios/scenario_001.yaml
- scenarios/scenario_002.yaml
- outputs/summary.json

## 8. Current weak points
- judge.py is still placeholder quality
- scenario coverage is too small
- state tracking is defined but not really enforced
- benchmark currently measures structure only in a rough way
- no real long-memory test yet
- no real tension-retention test yet

## 9. Immediate next steps
1. Improve judge.py from placeholder to stronger rule-based judge
2. Add scenario_003.yaml
3. Make run_benchmark.py produce richer logs
4. Add baseline comparison modes
5. Add first real state update logic

## 10. Recommended read order for a new session
1. README.md
2. HANDOFF.md
3. benchmark_spec.md
4. SESSION_STATE.json
5. src/run_benchmark.py
6. src/judge.py
7. scenarios/
8. outputs/summary.json

## 11. Handoff prompt for a new LLM session
You are taking over a Python benchmark project for a long-turn interactive system.

Read these first:
1. README.md
2. HANDOFF.md
3. benchmark_spec.md
4. SESSION_STATE.json

Important constraints:
- Keep the backend-first direction
- Do not redesign the architecture from scratch
- Canonical state remains the single source of truth
- Focus on benchmark quality before frontend work

Immediate tasks:
1. Improve src/judge.py
2. Add one more scenario
3. Re-run the benchmark and inspect outputs

First, summarize current status briefly. Then continue implementation.
