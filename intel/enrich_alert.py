import json
import time
from statistics import median
from datetime import datetime, timezone

FEED_FILE = "intel/threat_feed.json"
OUTPUT_FILE = "intel/enriched_alert.json"
LATENCY_FILE = "intel/enrichment_latency.json"


def load_feed():
    with open(FEED_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def enrich_alert(alert):
    start = time.perf_counter()

    feed = load_feed()
    ioc = alert.get("ioc")

    for indicator in feed["indicators"]:
        if indicator["ioc"] == ioc:
            result = {
                **alert,
                "threat_intelligence": {
                    "match": True,
                    "source": indicator["source"],
                    "confidence": indicator["confidence"],
                    "adversary_group": indicator["adversary_group"],
                    "campaign": indicator["campaign"],
                    "enriched_at": datetime.now(timezone.utc).isoformat()
                }
            }

            latency_ms = (time.perf_counter() - start) * 1000
            return result, latency_ms

    result = {
        **alert,
        "threat_intelligence": {
            "match": False,
            "source": None,
            "confidence": 0.0,
            "adversary_group": None,
            "campaign": None,
            "enriched_at": datetime.now(timezone.utc).isoformat()
        }
    }

    latency_ms = (time.perf_counter() - start) * 1000
    return result, latency_ms


def main():
    test_alerts = [
        {
            "alert_id": "ALERT-001",
            "rule_id": "DET-T1059-001",
            "ioc": "198.51.100.23"
        },
        {
            "alert_id": "ALERT-002",
            "rule_id": "DET-T1087-001",
            "ioc": "203.0.113.50"
        },
        {
            "alert_id": "ALERT-003",
            "rule_id": "DET-T1518-001",
            "ioc": "192.0.2.100"
        }
    ]

    latencies = []
    enriched_alerts = []

    for alert in test_alerts:
        alert["timestamp"] = datetime.now(timezone.utc).isoformat()

        enriched, latency = enrich_alert(alert)

        latencies.append(latency)
        enriched_alerts.append(enriched)

    latencies_sorted = sorted(latencies)

    p50 = median(latencies_sorted)

    p99_index = min(
        int(len(latencies_sorted) * 0.99),
        len(latencies_sorted) - 1
    )

    p99 = latencies_sorted[p99_index]

    result = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "alerts_tested": len(test_alerts),
        "enrichment_hits": sum(
            1 for alert in enriched_alerts
            if alert["threat_intelligence"]["match"]
        ),
        "enrichment_hit_percentage": (
            sum(
                1 for alert in enriched_alerts
                if alert["threat_intelligence"]["match"]
            )
            / len(test_alerts)
        ) * 100,
        "latency_requirement_seconds": 30,
        "p50_latency_ms": round(p50, 3),
        "p99_latency_ms": round(p99, 3),
        "within_30_seconds": p99 < 30000
    }

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(enriched_alerts, file, indent=2)

    with open(LATENCY_FILE, "w", encoding="utf-8") as file:
        json.dump(result, file, indent=2)

    print("Threat intelligence enrichment completed.")
    print(f"Alerts tested: {result['alerts_tested']}")
    print(f"Enrichment hits: {result['enrichment_hits']}")
    print(
        f"Enrichment hit percentage: "
        f"{result['enrichment_hit_percentage']:.2f}%"
    )
    print(f"P50 latency: {result['p50_latency_ms']} ms")
    print(f"P99 latency: {result['p99_latency_ms']} ms")
    print(
        f"Within 30 seconds: "
        f"{result['within_30_seconds']}"
    )
    print(f"Latency report: {LATENCY_FILE}")


if __name__ == "__main__":
    main()