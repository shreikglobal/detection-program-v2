import json

RULES_FILE = "triage/triage_rules.json"
ALERT_FILE = "intel/enriched_alert.json"
OUTPUT_FILE = "triage/triage_results.json"


def load_json(path):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)


def classify_alert(confidence, thresholds):
    if confidence > thresholds["escalate_above"]:
        return "ESCALATE"
    elif confidence < thresholds["suppress_below"]:
        return "SUPPRESS"
    else:
        return "HUMAN_REVIEW"


def get_reason(action, confidence):
    if action == "ESCALATE":
        return f"High confidence ({confidence}) requires escalation."
    elif action == "SUPPRESS":
        return f"Low confidence ({confidence}) is below suppression threshold."
    else:
        return f"Confidence ({confidence}) requires human review."


def main():
    rules = load_json(RULES_FILE)
    alerts = load_json(ALERT_FILE)

    if isinstance(alerts, dict):
        alerts = [alerts]

    results = []

    for alert in alerts:
        confidence = alert["threat_intelligence"]["confidence"]

        action = classify_alert(
            confidence,
            rules["thresholds"]
        )

        results.append({
            "alert_id": alert["alert_id"],
            "rule_id": alert["rule_id"],
            "ioc": alert["ioc"],
            "confidence": confidence,
            "action": action,
            "reason": get_reason(action, confidence)
        })

    output = {
        "total_alerts": len(results),
        "results": results
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(output, file, indent=2)

    print("Triage completed.")
    print(f"Alerts processed: {len(results)}")

    for result in results:
        print(
            f'{result["alert_id"]} | '
            f'Confidence: {result["confidence"]} | '
            f'Action: {result["action"]} | '
            f'Reason: {result["reason"]}'
        )


if __name__ == "__main__":
    main()