def apply_reaction_rules(state: dict, text: str) -> None:
    scene = state.setdefault("scene", {})
    characters = state.setdefault("characters", {})
    tension = state.setdefault("tension", {})

    user_side = characters.setdefault("user_side", {})
    other_side = characters.setdefault("other_side", {})
    recent_events = scene.setdefault("recent_events", [])
    open_loops = tension.setdefault("open_loops", [])

    if "probe" in text or "reaction" in text:
        other_side["emotion"] = "guarded"

    if "press" in text:
        other_side["emotion"] = "tense"
        scene["phase"] = "probe"
        if "pressure_applied" not in recent_events:
            recent_events.append("pressure_applied")
        if "emotional_shift" not in open_loops:
            open_loops.append("emotional_shift")

    if "soften tone" in text:
        other_side["emotion"] = "curious"
        other_side["initiative"] = 0.45
        scene["phase"] = "probe"
        if "tone_softened" not in recent_events:
            recent_events.append("tone_softened")

    if "step closer" in text:
        other_side["emotion"] = "alert"

    if "wait silently" in text:
        other_side["emotion"] = "uneasy"
        other_side["initiative"] = 0.65
        if "silent_wait" not in recent_events:
            recent_events.append("silent_wait")
        if "silence_pressure" not in open_loops:
            open_loops.append("silence_pressure")

    if "sudden accusation" in text:
        scene["phase"] = "pivot"
        other_side["emotion"] = "defensive"
        user_side["initiative"] = 0.75
        other_side["initiative"] = 0.25
        if "accusation" not in recent_events:
            recent_events.append("accusation")
        if "trust_drop" not in open_loops:
            open_loops.append("trust_drop")
