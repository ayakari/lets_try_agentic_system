from pathlib import Path


def resolve_scenario_paths(project_root: Path, suite: str = "product", scenario_dir: str | None = None, scenario: str | None = None):
    if scenario:
        path = Path(scenario).resolve()
        if not path.exists():
            raise FileNotFoundError(f"Scenario file not found: {path}")
        return [path]

    if scenario_dir:
        dir_path = Path(scenario_dir).resolve()
        if not dir_path.exists():
            raise FileNotFoundError(f"Scenario directory not found: {dir_path}")
        return sorted(dir_path.glob("*.yaml"))

    if suite == "product":
        dir_path = project_root / "benchmarks" / "product" / "scenarios"
    elif suite == "public":
        dir_path = project_root / "benchmarks" / "public" / "scenarios"
    else:
        raise ValueError(f"Unknown suite: {suite}")

    if not dir_path.exists():
        raise FileNotFoundError(f"Scenario directory not found: {dir_path}")

    return sorted(dir_path.glob("*.yaml"))
