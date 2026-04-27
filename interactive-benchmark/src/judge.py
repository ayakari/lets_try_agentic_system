def get_nested(d: dict, path: str):
    cur = d
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur


def judge_turn(expected_checks: dict, current_state: dict) -> dict:
    passed = 0
    total = 0
    details = []

    for key, expected in expected_checks.items():
        total += 1

        if key.endswith("_contains"):
            real_key = key.replace("_contains", "")
            actual = get_nested(current_state, real_key)
            ok = isinstance(actual, list) and all(x in actual for x in expected)

        elif key.endswith("_in"):
            real_key = key.replace("_in", "")
            actual = get_nested(current_state, real_key)
            ok = actual in expected

        else:
            actual = get_nested(current_state, key)
            ok = actual == expected

        if ok:
            passed += 1

        details.append({
            "check": key,
            "expected": expected,
            "actual": actual,
            "ok": ok
        })

    return {
        "passed": passed,
        "total": total,
        "details": details
    }


def judge_session(run_result: dict) -> dict:
    turns = run_result.get("turn_results", [])

    total_checks = 0
    total_passed = 0
    per_turn = []

    for t in turns:
        expected_checks = t.get("expected_checks", {})
        current_state = t.get("current_state", {})
        judged = judge_turn(expected_checks, current_state)

        total_checks += judged["total"]
        total_passed += judged["passed"]

        per_turn.append({
            "turn_id": t["turn_id"],
            "passed": judged["passed"],
            "total": judged["total"],
            "details": judged["details"]
        })

    state_consistency = 0
    if total_checks > 0:
        state_consistency = round(30 * total_passed / total_checks)

    # 暫時其他分數先留空殼
    long_memory = 0
    reaction_coherence = 0
    tension_retention = 0
    sensory_rendering = 0

    total = (
        state_consistency
        + long_memory
        + reaction_coherence
        + tension_retention
        + sensory_rendering
    )

    return {
        "state_consistency": state_consistency,
        "long_memory": long_memory,
        "reaction_coherence": reaction_coherence,
        "tension_retention": tension_retention,
        "sensory_rendering": sensory_rendering,
        "total": total,
        "turn_breakdown": per_turn
    }
