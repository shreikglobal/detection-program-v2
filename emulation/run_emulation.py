import json
from datetime import datetime


TECHNIQUES_FILE = "emulation/techniques.json"
REPORT_FILE = "emulation/coverage_report.json"


def load_techniques():
    with open(TECHNIQUES_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    return [
        technique
        for technique in data["techniques"]
        if technique.get("enabled", False)
    ]


def run_emulation(techniques):
    results = []

    for technique in techniques:
        result = {
            "technique_id": technique["id"],
            "technique_name": technique["name"],
            "emulation_status": "SIMULATED",
            "detection_status": "PENDING",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }

        results.append(result)

    return results


def save_report(results):
    report = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "total_techniques": len(results),
        "results": results
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print(f"Coverage report generated: {REPORT_FILE}")


def main():
    techniques = load_techniques()

    if not techniques:
        print("No enabled techniques found.")
        return

    results = run_emulation(techniques)
    save_report(results)


if __name__ == "__main__":
    main()
