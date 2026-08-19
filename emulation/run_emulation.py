import json
from datetime import datetime, timezone


TECHNIQUES_FILE = "emulation/techniques.json"
RULES_FILE = "detections/rules.json"
REPORT_FILE = "emulation/coverage_report.json"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_techniques():
    data = load_json(TECHNIQUES_FILE)

    return [
        technique
        for technique in data["techniques"]
        if technique.get("enabled", False)
    ]


def load_detection_rules():
    data = load_json(RULES_FILE)

    return [
        rule
        for rule in data["rules"]
        if rule.get("enabled", False)
    ]


def run_emulation(techniques, rules):
    results = []

    detected_techniques = {
        rule["technique_id"]
        for rule in rules
    }

    for technique in techniques:
        technique_id = technique["id"]

        if technique_id in detected_techniques:
            detection_status = "DETECTED"
        else:
            detection_status = "MISSED"

        result = {
            "technique_id": technique_id,
            "technique_name": technique["name"],
            "emulation_status": "SIMULATED",
            "detection_status": detection_status,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

        results.append(result)

    return results


def save_report(results):
    total = len(results)
    detected = sum(
        1
        for result in results
        if result["detection_status"] == "DETECTED"
    )

    coverage_percentage = (
        (detected / total) * 100
        if total > 0
        else 0
    )

    report = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total_techniques": total,
        "detected": detected,
        "missed": total - detected,
        "coverage_percentage": round(coverage_percentage, 2),
        "results": results
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(f"Coverage report generated: {REPORT_FILE}")
    print(f"Coverage: {coverage_percentage:.2f}%")


def main():
    techniques = load_techniques()
    rules = load_detection_rules()

    if not techniques:
        print("No enabled techniques found.")
        return

    results = run_emulation(techniques, rules)
    save_report(results)


if __name__ == "__main__":
    main()
