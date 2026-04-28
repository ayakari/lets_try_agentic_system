# public_longmem_eval_spec

## Goal

這個 profile 只評估 long-term memory related checks。

## Scoring scope

Only count checks whose keys start with:

- memory.

Ignore:

- scene.
- characters.
- tension.

## Output policy

For `public_longmem`:

- long_memory: real score
- state_consistency: 0
- reaction_coherence: 0
- tension_retention: 0
- sensory_rendering: 0

## Reason

這條 profile 是 public benchmark mapping，用來對齊外部記憶能力，不混入產品特有的 state / tension / reaction 指標。
