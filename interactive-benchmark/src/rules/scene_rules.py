def apply_scene_rules(state: dict, text: str) -> None:
    scene = state.setdefault("scene", {})
    tension = state.setdefault("tension", {})
    recent_events = scene.setdefault("recent_events", [])
    open_loops = tension.setdefault("open_loops", [])

    if "start conversation" in text:
        scene["phase"] = "setup"
        if "conversation_started" not in recent_events:
            recent_events.append("conversation_started")

    if "probe" in text or "reaction" in text:
        scene["phase"] = "probe"
        if "unknown_motive" not in open_loops:
            open_loops.append("unknown_motive")
        if "probing_started" not in recent_events:
            recent_events.append("probing_started")

    if "approach" in text:
        scene["distance"] = "close"
        if "approach" not in recent_events:
            recent_events.append("approach")

    if "change topic" in text:
        scene["phase"] = "pivot"
        if "topic_shift" not in recent_events:
            recent_events.append("topic_shift")
        if "consistency_test" not in open_loops:
            open_loops.append("consistency_test")

    if "give space" in text:
        scene["distance"] = "medium"
        if "space_given" not in recent_events:
            recent_events.append("space_given")

    if "step closer" in text:
        scene["distance"] = "close"
        if "step_closer" not in recent_events:
            recent_events.append("step_closer")
        if "distance_shift" not in open_loops:
            open_loops.append("distance_shift")
