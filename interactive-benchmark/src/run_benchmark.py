from pathlib import Path
import json
import yaml
import argparse

from judge import judge_session
from state_tracker import StateTracker
from benchmark_loader import resolve_scenario_paths


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_one_scenario(scenario_path: Path, profile: str) -> dict:
    scenario = load_yaml(scenario_path)

    tracker = StateTracker(scenario.get("initial_state", {}))
    turn_results = []

    for turn in scenario.get("turns", []):
        current_state = tracker.apply_user_action(turn.get("user_action", ""))
        expected_checks = turn.get("expected_checks", {})

        turn_results.append({
            "turn_id": turn["turn_id"],
            "user_action": turn.get("user_action", ""),
            "expected_checks": expected_checks,
            "current_state": current_state
        })

    run_result = {
        "scenario_file": scenario_path.name,
        "scenario_path": str(scenario_path),
        "scenario_name": scenario.get("name", "unnamed"),
        "initial_state": scenario.get("initial_state", {}),
        "turn_results": turn_results
    }

    scores = judge_session(run_result, profile=profile)
    run_result["scores"] = scores
    return run_result


def save_result(result: dict, output_dir: Path) -> None:
    scenario_stem = Path(result["scenario_file"]).stem
    output_path = output_dir / f"{scenario_stem}_result.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--suite", default="product", choices=["product", "public"])
    parser.add_argument("--profile", default="product_v0")
    parser.add_argument("--scenario-dir", default=None)
    parser.add_argument("--scenario", default=None)
    return parser.parse_args()


def main():
    args = parse_args()

    project_root = Path(__file__).resolve().parent.parent
    output_dir = project_root / "outputs"
    output_dir.mkdir(parents=True, exist_ok=True)

    scenario_paths = resolve_scenario_paths(
        project_root=project_root,
        suite=args.suite,
        scenario_dir=args.scenario_dir,
        scenario=args.scenario
    )

    if not scenario_paths:
        print("No scenario files found.")
        return

    all_results = []

    for scenario_path in scenario_paths:
        result = run_one_scenario(scenario_path, profile=args.profile)
        save_result(result, output_dir)
        all_results.append(result)
        print(f"{result['scenario_name']}: {result['scores']['total']} ({result['scores']['profile']})")

    summary = {
        "suite": args.suite,
        "profile": args.profile,
        "num_scenarios": len(all_results),
        "results": [
            {
                "scenario_file": r["scenario_file"],
                "scenario_name": r["scenario_name"],
                "total": r["scores"]["total"],
                "state_consistency": r["scores"]["state_consistency"],
                "long_memory": r["scores"]["long_memory"],
                "reaction_coherence": r["scores"]["reaction_coherence"],
                "tension_retention": r["scores"]["tension_retention"]
            }
            for r in all_results
        ]
    }

    summary_path = output_dir / f"summary_{args.suite}_{args.profile}.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Summary written to: {summary_path}")


if __name__ == "__main__":
    main()
