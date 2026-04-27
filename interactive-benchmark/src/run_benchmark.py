from pathlib import Path
import yaml


def main():
    scenario_path = Path(__file__).resolve().parent.parent / "scenarios" / "scenario_001.yaml"
    if not scenario_path.exists():
        print(f"Scenario not found: {scenario_path}")
        return

    with open(scenario_path, "r", encoding="utf-8") as f:
        scenario = yaml.safe_load(f)

    print("Loaded scenario:", scenario.get("name", "unnamed"))
    print("Initial state:")
    print(scenario.get("initial_state", {}))
    print("Turns:")
    for turn in scenario.get("turns", []):
        print(f"- Turn {turn.get('turn_id')}: {turn.get('user_action')}")


if __name__ == "__main__":
    main()
