def judge_session(scenario: dict) -> dict:
    turns = scenario.get("turns", [])
    initial_state = scenario.get("initial_state", {})

    state_consistency = 0
    long_memory = 0
    reaction_coherence = 0
    tension_retention = 0
    sensory_rendering = 0

    # Very simple rule-based placeholder scoring
    if initial_state.get("scene"):
        state_consistency += 10
    if initial_state.get("characters"):
        state_consistency += 10
    if initial_state.get("tension"):
        state_consistency += 10

    if initial_state.get("memory"):
        long_memory += 10
    if len(turns) >= 2:
        long_memory += 5

    if initial_state.get("characters", {}).get("other_side"):
        reaction_coherence += 10
    if len(turns) >= 2:
        reaction_coherence += 5

    open_loops = initial_state.get("tension", {}).get("open_loops", [])
    if len(open_loops) > 0:
        tension_retention += 10
    if len(turns) >= 2:
        tension_retention += 5

    # Placeholder for now
    sensory_rendering = 2

    total = (
        state_consistency
        + long_memory
        + reaction_coherence
        + tension_retention
        + sensory_rendering
    )

    return {
        "state_consistency": min(state_consistency, 30),
        "long_memory": min(long_memory, 25),
        "reaction_coherence": min(reaction_coherence, 20),
        "tension_retention": min(tension_retention, 15),
        "sensory_rendering": min(sensory_rendering, 10),
        "total": min(total, 100),
    }
