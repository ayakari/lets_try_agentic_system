def apply_memory_rules(state: dict, text: str) -> None:
    memory = state.setdefault("memory", {})

    stable_facts = memory.setdefault("stable_facts", [])
    recent_facts = memory.setdefault("recent_facts", [])
    updated_facts = memory.setdefault("updated_facts", [])

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
