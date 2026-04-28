def apply_scene_rules(state: dict, text: str) -> None:
    scene = state.setdefault("scene", {})
    tension = state.setdefault("tension", {})
    memory = state.setdefault("memory", {})

    recent_events = scene.setdefault("recent_events", [])
    open_loops = tension.setdefault("open_loops", [])
    stable_facts = memory.setdefault("stable_facts", [])

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

    # branching rules
    if "choose left path" in text:
        scene["location"] = "left_path"
        scene["phase"] = "branch_left"
        if "branch=right" in stable_facts:
            stable_facts.remove("branch=right")
        if "branch=left" not in stable_facts:
            stable_facts.append("branch=left")
        if "left_path_chosen" not in recent_events:
            recent_events.append("left_path_chosen")
        if "left_path_mystery" not in open_loops:
            open_loops.append("left_path_mystery")

    if "choose right path" in text:
        scene["location"] = "right_path"
        scene["phase"] = "branch_right"
        if "branch=left" in stable_facts:
            stable_facts.remove("branch=left")
        if "branch=right" not in stable_facts:
            stable_facts.append("branch=right")
        if "right_path_chosen" not in recent_events:
            recent_events.append("right_path_chosen")
        if "right_path_mystery" not in open_loops:
            open_loops.append("right_path_mystery")

    if "inspect the marked door" in text and scene.get("location") == "left_path":
        if "left_door_inspected" not in recent_events:
            recent_events.append("left_door_inspected")

    if "ask about the lantern" in text and scene.get("location") == "right_path":
        if "right_lantern_checked" not in recent_events:
            recent_events.append("right_lantern_checked")
