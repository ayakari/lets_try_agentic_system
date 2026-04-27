from pathlib import Path
import json
import yaml

from judge import judge_session


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def run_one_scenario(scenario_path: Path) -> dict:
    scenario = load_yaml(scenario_path)
    scores = judge_session(scenario)

    result = {
        "scenario_file": scenario_path.name,
        "scenario_name": scenario.get("name", "unnamed"),
        "initial_state": scenario.get("initial_state", {}),
        "turns": scenario.get("turns", []),
        "scores": scores,
    }
    return result


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

    print(f"Found {len(scenario_paths)} scenario(s).")
    print("-" * 60)

    for scenario_path in scenario_paths:
        result = run_one_scenario(scenario_path)
        save_result(result, output_dir)
        all_results.append(result)

        print(f"Scenario: {result['scenario_name']} ({result['scenario_file']})")
        print(f"Turns: {len(result['turns'])}")
        print(f"Scores: {result['scores']}")
        print("-" * 60)

    avg_total = sum(r["scores"]["total"] for r in all_results) / len(all_results)

    summary = {
        "num_scenarios": len(all_results),
        "average_total": avg_total,
        "results": [
            {
                "scenario_file": r["scenario_file"],
                "scenario_name": r["scenario_name"],
                "total": r["scores"]["total"],
            }
            for r in all_results
        ],
    }

    summary_path = output_dir / "summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print("Benchmark complete.")
    print(f"Average total score: {avg_total:.2f}")
    print(f"Summary written to: {summary_path}")


if __name__ == "__main__":
    main()
