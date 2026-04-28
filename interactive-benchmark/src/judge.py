def get_nested(d: dict, path: str):
    cur = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def judge_turn(expected_checks: dict, current_state: dict) -> list:
    details = []

    for key, expected in expected_checks.items():
        category = "state_consistency"

        if key.startswith("memory."):
            category = "long_memory"
        elif key.startswith("characters."):
            category = "reaction_coherence"
        elif key.startswith("tension."):
            category = "tension_retention"
        elif key.startswith("scene."):
            category = "state_consistency"

        if key.endswith("_contains"):
            real_key = key.replace("_contains", "")
            actual = get_nested(current_state, real_key)
            ok = isinstance(actual, list) and all(x in actual for x in expected)

        elif key.endswith("_not_contains"):
            real_key = key.replace("_not_contains", "")
            actual = get_nested(current_state, real_key)
            ok = isinstance(actual, list) and all(x not in actual for x in expected)

        elif key.endswith("_in"):
            real_key = key.replace("_in", "")
            actual = get_nested(current_state, real_key)
            ok = actual in expected

        else:
            actual = get_nested(current_state, key)
            ok = actual == expected

        details.append({
            "category": category,
            "check": key,
            "expected": expected,
            "actual": actual,
            "ok": ok
        })

    return details


def score_bucket(details: list, category: str, max_score: int) -> int:
    filtered = [d for d in details if d["category"] == category]
    if not filtered:
        return 0

    passed = sum(1 for d in filtered if d["ok"])
    total = len(filtered)
    return round(max_score * passed / total)


def judge_product_v0(run_result: dict) -> dict:
    turns = run_result.get("turn_results", [])
    all_details = []
    per_turn = []

    for t in turns:
        expected_checks = t.get("expected_checks", {})
        current_state = t.get("current_state", {})
        details = judge_turn(expected_checks, current_state)
        all_details.extend(details)

        per_turn.append({
            "turn_id": t["turn_id"],
            "details": details
        })

    state_consistency = score_bucket(all_details, "state_consistency", 30)
    long_memory = score_bucket(all_details, "long_memory", 25)
    reaction_coherence = score_bucket(all_details, "reaction_coherence", 20)
    tension_retention = score_bucket(all_details, "tension_retention", 15)
    sensory_rendering = 0

    total = (
        state_consistency
        + long_memory
        + reaction_coherence
        + tension_retention
        + sensory_rendering
    )

    return {
        "profile": "product_v0",
        "state_consistency": state_consistency,
        "long_memory": long_memory,
        "reaction_coherence": reaction_coherence,
        "tension_retention": tension_retention,
        "sensory_rendering": sensory_rendering,
        "total": total,
        "turn_breakdown": per_turn
    }


def judge_public_longmem(run_result: dict) -> dict:
    base = judge_product_v0(run_result)
    base["profile"] = "public_longmem"
    return base


def judge_session(run_result: dict, profile: str = "product_v0") -> dict:
    if profile == "product_v0":
        return judge_product_v0(run_result)
    if profile == "public_longmem":
        return judge_public_longmem(run_result)

    raise ValueError(f"Unknown judge profile: {profile}")
