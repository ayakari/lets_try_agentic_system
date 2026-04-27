from pathlib import Path
import json
import yaml

from judge import judge_session


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def deep_copy(obj):
    return json.loads(json.dumps(obj))


def apply_expected_checks_to_state(state: dict, expected_checks: dict) -> dict:
    state = deep_copy(state)

    for key, expected in expected_checks.items():
        if key.endswith("_contains") or key.endswith("_in"):
            continue

        parts = key.split(".")
        cur = state
        for part in parts[:-1]:
            if part not in cur or not isinstance(cur[part], dict):
                cur[part] = {}
            cur = cur[part]
        cur[parts[-1]] = expected

    for key, expected in expected_checks.items():
        if key.endswith("_contains"):
            real_key = key.replace("_contains", "")
            parts = real_key.split(".")
            cur = state
            for part in parts[:-1]:
                if part not in cur or not isinstance(cur[part], dict):
                    cur[part] = {}
                cur = cur[part]
            leaf = parts[-1]
            if leaf not in cur or not isinstance(cur[leaf], list):
                cur[leaf] = []
            for x in expected:
                if x not in cur[leaf]:
                    cur[leaf].append(x)

    return state


def run_one_scenario(scenario_path: Path) -> dict:
    scenario = load_yaml(scenario_path)

    current_state = deep_copy(scenario.get("initial_state", {}))
    turn_results = []

    for turn in scenario.get("turns", []):
        expected_checks = turn.get("expected_checks", {})
        current_state = apply_expected_checks_to_state(current_state, expected_checks)

        turn_results.append({
            "turn_id": turn["turn_id"],
            "user_action": turn.get("user_action", ""),
            "expected_checks": expected_checks,
            "current_state": deep_copy(current_state)
        })

    run_result = {
        "scenario_file": scenario_path.name,
        "scenario_name": scenario.get("name", "unnamed"),
        "initial_state": scenario.get("initial_state", {}),
        "turn_results": turn_results
    }

    scores = judge_session(run_result)
    run_result["scores"] = scores
    return run_result


def save_result(result: dict, output_dir: Path) -> None:
    scenario_stem = Path(result["scenario_file"]).stem
    output_path = output_dir / f"{scenario_stem}_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def main():
    project_root = Path(__file__).resolve().parent.parent
    scenario_dir = project_root / "scenarios"
    output_dir = project_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    scenario_paths = sorted(scenario_dir.glob("*.yaml"))
    if not scenario_paths:
        print("No scenario files found.")
        return

    all_results = []

    for scenario_path in scenario_paths:
        result = run_one_scenario(scenario_path)
        save_result(result, output_dir)
        all_results.append(result)
        print(f"{result['scenario_name']}: {result['scores']['total']}")

    summary = {
        "num_scenarios": len(all_results),
        "results": [
            {
                "scenario_file": r["scenario_file"],
                "scenario_name": r["scenario_name"],
                "total": r["scores"]["total"],
                "state_consistency": r["scores"]["state_consistency"]
            }
            for r in all_results
        ]
    }

    summary_path = output_dir / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Summary written to: {summary_path}")


if __name__ == "__main__":
    main()
