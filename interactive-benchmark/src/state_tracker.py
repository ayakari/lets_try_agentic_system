from copy import deepcopy


class StateTracker:
    def __init__(self, initial_state: dict):
        self.state = deepcopy(initial_state)

    def get_state(self) -> dict:
        return deepcopy(self.state)

    def apply_user_action(self, user_action: str) -> dict:
        text = (user_action or "").lower()

        scene = self.state.setdefault("scene", {})
        characters = self.state.setdefault("characters", {})
        other_side = characters.setdefault("other_side", {})
        tension = self.state.setdefault("tension", {})
        open_loops = tension.setdefault("open_loops", [])
        recent_events = scene.setdefault("recent_events", [])

        # Rule-based v0 transitions
        if "start conversation" in text:
            scene["phase"] = "setup"
            if "conversation_started" not in recent_events:
                recent_events.append("conversation_started")

        if "probe" in text or "reaction" in text:
            scene["phase"] = "probe"
            other_side["emotion"] = "guarded"
            if "unknown_motive" not in open_loops:
                open_loops.append("unknown_motive")
            if "probing_started" not in recent_events:
                recent_events.append("probing_started")

        if "approach" in text:
            scene["distance"] = "close"
            if "approach" not in recent_events:
                recent_events.append("approach")

        if "press" in text:
            other_side["emotion"] = "tense"
            scene["phase"] = "probe"
            if "pressure_applied" not in recent_events:
                recent_events.append("pressure_applied")
            if "emotional_shift" not in open_loops:
                open_loops.append("emotional_shift")

        if "change topic" in text:
            scene["phase"] = "pivot"
            if "topic_shift" not in recent_events:
                recent_events.append("topic_shift")
            if "consistency_test" not in open_loops:
                open_loops.append("consistency_test")

        return self.get_state()
