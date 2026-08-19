import json


BASELINE_FILE = "emulation/baseline_report.json"
CURRENT_FILE = "emulation/coverage_report.json"
DELTA_FILE = "emulation/coverage_delta.json"


def load_report(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def build_detection_map(report):
    return {
        result["technique_id"]: result["detection_status"]
        for result in report["results"]
    }


def calculate_delta(baseline, current):
    baseline_map = build_detection_map(baseline)
    current_map = build_detection_map(current)

    newly_detected = []
    newly_missed = []
    unchanged = []

    all_techniques = set(baseline_map) | set(current_map)

    for technique_id in sorted(all_techniques):
        old_status = baseline_map.get(technique_id, "NOT_PRESENT")
        new_status = current_map.get(technique_id, "NOT_PRESENT")

        if old_status != "DETECTED" and new_status == "DETECTED":
            newly_detected.append(technique_id)

        elif old_status == "DETECTED" and new_status != "DETECTED":
            newly_missed.append(technique_id)

        else:
            unchanged.append(technique_id)

    coverage_change = round(
        current["coverage_percentage"]
        - baseline["coverage_percentage"],
        2
    )

    return {
        "baseline_coverage": baseline["coverage_percentage"],
        "current_coverage": current["coverage_percentage"],
        "coverage_change_percentage_points": coverage_change,
        "newly_detected": newly_detected,
        "newly_missed": newly_missed,
        "unchanged": unchanged
    }


def main():
    baseline = load_report(BASELINE_FILE)
    current = load_report(CURRENT_FILE)

    delta = calculate_delta(baseline, current)

    with open(DELTA_FILE, "w", encoding="utf-8") as file:
        json.dump(delta, file, indent=2)

    print("Coverage delta generated.")
    print(f"Baseline coverage: {delta['baseline_coverage']}%")
    print(f"Current coverage: {delta['current_coverage']}%")
    print(
        "Coverage change: "
        f"{delta['coverage_change_percentage_points']} percentage points"
    )
    print(f"Newly detected: {delta['newly_detected']}")
    print(f"Newly missed: {delta['newly_missed']}")


if __name__ == "__main__":
    main()