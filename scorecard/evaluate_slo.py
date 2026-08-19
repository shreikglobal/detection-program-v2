import json


SLO_FILE = "scorecard/slo.json"
METRICS_FILE = "scorecard/weekly_metrics.json"
OUTPUT_FILE = "scorecard/slo_report.json"


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate():
    slo = load_json(SLO_FILE)
    metrics = load_json(METRICS_FILE)

    noise_limit = slo["slo"]["noise_budget"]["max_false_positive_rate_weekly"]
    debt_threshold = slo["slo"]["coverage_debt"]["alert_threshold"]

    rule_results = []

    for rule in metrics["rules"]:
        fp_rate = rule["false_positive_rate"]

        if fp_rate > noise_limit:
            status = "DRAFT"
            page_on_call = True
        else:
            status = "ACTIVE"
            page_on_call = False

        rule_results.append({
            "rule_id": rule["rule_id"],
            "false_positive_rate": fp_rate,
            "noise_budget": noise_limit,
            "status": status,
            "page_on_call": page_on_call
        })

    coverage_debt = metrics["coverage_debt"]

    coverage_alert = coverage_debt >= debt_threshold

    report = {
        "noise_budget_enforced": True,
        "coverage_debt": coverage_debt,
        "coverage_debt_threshold": debt_threshold,
        "coverage_debt_alert": coverage_alert,
        "rules": rule_results
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2)

    print("SLO evaluation completed.")
    print(f"Coverage debt: {coverage_debt}")
    print(f"Coverage debt alert: {coverage_alert}")

    for rule in rule_results:
        print(
            f"{rule['rule_id']} | "
            f"FP rate: {rule['false_positive_rate'] * 100:.2f}% | "
            f"Status: {rule['status']} | "
            f"Page: {rule['page_on_call']}"
        )


if __name__ == "__main__":
    evaluate()