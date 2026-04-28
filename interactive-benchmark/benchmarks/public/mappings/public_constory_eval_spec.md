# public_constory_eval_spec

## Goal

這個 profile 只評估 story consistency related checks。

## Scoring scope

Count checks whose keys start with:

- scene.
- tension.
- characters.

Ignore:

- memory.

## Output policy

For `public_constory`:

- state_consistency: real score from scene.* checks
- tension_retention: real score from tension.* checks
- reaction_coherence: real score from characters.* checks
- long_memory: 0
- sensory_rendering: 0

## Reason

這條 profile 是 public benchmark mapping，用來對齊故事一致性、角色連續性、張力維持。
