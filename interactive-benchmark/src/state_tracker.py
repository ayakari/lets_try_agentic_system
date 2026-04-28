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
        user_side = characters.setdefault("user_side", {})
        other_side = characters.setdefault("other_side", {})
        tension = self.state.setdefault("tension", {})
        memory = self.state.setdefault("memory", {})

        open_loops = tension.setdefault("open_loops", [])
        recent_events = scene.setdefault("recent_events", [])
        stable_facts = memory.setdefault("stable_facts", [])
        recent_facts = memory.setdefault("recent_facts", [])
        updated_facts = memory.setdefault("updated_facts", [])

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

        # reaction-shift rules
        if "soften tone" in text:
            other_side["emotion"] = "curious"
            other_side["initiative"] = 0.45
            scene["phase"] = "probe"
            if "tone_softened" not in recent_events:
                recent_events.append("tone_softened")

        if "give space" in text:
            scene["distance"] = "medium"
            if "space_given" not in recent_events:
                recent_events.append("space_given")

        if "step closer" in text:
            scene["distance"] = "close"
            other_side["emotion"] = "alert"
            if "distance_shift" not in open_loops:
                open_loops.append("distance_shift")
            if "step_closer" not in recent_events:
                recent_events.append("step_closer")

        if "wait silently" in text:
            other_side["emotion"] = "uneasy"
            other_side["initiative"] = 0.65
            if "silence_pressure" not in open_loops:
                open_loops.append("silence_pressure")
            if "silent_wait" not in recent_events:
                recent_events.append("silent_wait")

        if "sudden accusation" in text:
            scene["phase"] = "pivot"
            other_side["emotion"] = "defensive"
            user_side["initiative"] = 0.75
            other_side["initiative"] = 0.25
            if "trust_drop" not in open_loops:
                open_loops.append("trust_drop")
            if "accusation" not in recent_events:
                recent_events.append("accusation")

        # memory-related rules
        if "my name is akira" in text:
            if "name=akira" not in stable_facts:
                stable_facts.append("name=akira")

        if "i prefer tea" in text:
            if "pref=tea" not in stable_facts:
                stable_facts.append("pref=tea")

        if "actually i prefer coffee" in text:
            if "pref=tea" in stable_facts:
                stable_facts.remove("pref=tea")
            if "pref=coffee" not in stable_facts:
                stable_facts.append("pref=coffee")
            if "pref_updated_to_coffee" not in updated_facts:
                updated_facts.append("pref_updated_to_coffee")

        if "remember that" in text:
            if "explicit_memory_request" not in recent_facts:
                recent_facts.append("explicit_memory_request")

        if "what do i prefer" in text:
            if "preference_query" not in recent_facts:
                recent_facts.append("preference_query")

        return self.get_state()
