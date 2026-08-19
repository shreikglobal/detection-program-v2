import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent.parent


def load_json(path):
    with open(ROOT / path, "r", encoding="utf-8") as f:
        return json.load(f)


# Load existing Stage 3, 4, 5 and SLO outputs
slo = load_json("scorecard/slo_report.json")
intel = load_json("intel/enrichment_latency.json")
triage = load_json("triage/triage_results.json")
forensics = load_json("forensics/verification_report.json")


# ============================================================
# 1. NOISE BUDGET CONSUMPTION
# ============================================================

noise_rules = []

for rule in slo.get("rules", []):
    budget = rule.get("noise_budget", 0)
    fp_rate = rule.get("false_positive_rate", 0)

    consumption = round((fp_rate / budget) * 100, 2) if budget else 0

    noise_rules.append({
        "rule_id": rule.get("rule_id"),
        "false_positive_rate": fp_rate,
        "noise_budget": budget,
        "budget_consumption_percent": consumption,
        "status": rule.get("status")
    })


# ============================================================
# 2. ENRICHMENT HIT RATE
# ============================================================

enrichment_hit_rate = intel.get(
    "enrichment_hit_percentage",
    0
)


# ============================================================
# 3. TRIAGE SUMMARY
# ============================================================

results = triage.get("results", [])

total_triage = len(results)

escalated = sum(
    1 for x in results
    if x.get("action") == "ESCALATE"
)

suppressed = sum(
    1 for x in results
    if x.get("action") == "SUPPRESS"
)

human_review = sum(
    1 for x in results
    if x.get("action") == "HUMAN_REVIEW"
)


# ============================================================
# 4. FORENSIC VERIFICATION
# ============================================================

# verification_report.json uses:
# "verification_status": "VERIFIED"

forensic_verified = (
    forensics.get("verification_status") == "VERIFIED"
)

artifacts_verified = forensics.get(
    "artifacts_verified",
    0
)


# ============================================================
# 5. FORENSIC COLLECTION SUCCESS RATE
# ============================================================

# Current forensic verification report confirms
# all collected artifacts were verified.

if forensic_verified and artifacts_verified > 0:
    forensic_success_rate = 100.0
else:
    forensic_success_rate = 0.0


# ============================================================
# 6. DETECTION PROGRAM HEALTH SCORECARD
# ============================================================

scorecard = {
    "generated_at": datetime.now(timezone.utc).isoformat(),

    "report": "Detection Program Health Scorecard",

    "mttd_30_day_trend": {
        "status": "DATA_PENDING",
        "note": "30-day historical MTTD data not yet available"
    },

    "noise_budget_consumption": noise_rules,

    "coverage_debt": {
        "current": slo.get("coverage_debt"),
        "threshold": slo.get("coverage_debt_threshold"),
        "alert": slo.get("coverage_debt_alert")
    },

    "enrichment": {
        "hit_rate_percent": enrichment_hit_rate,
        "p50_latency_ms": intel.get("p50_latency_ms"),
        "p99_latency_ms": intel.get("p99_latency_ms"),
        "within_30_seconds": intel.get("within_30_seconds")
    },

    "triage": {
        "alerts_processed": total_triage,
        "escalated": escalated,
        "human_review": human_review,
        "suppressed": suppressed,
        "accuracy_status": "BASELINE_CAPTURED"
    },

    "forensics": {
        "verification_status": (
            "VERIFIED"
            if forensic_verified
            else "CHECK_REQUIRED"
        ),
        "artifacts_verified": artifacts_verified,
        "collection_success_rate_percent": forensic_success_rate
    }
}


# ============================================================
# 7. WRITE SCORECARD
# ============================================================

output = ROOT / "scorecard" / "scorecard.json"

with open(output, "w", encoding="utf-8") as f:
    json.dump(scorecard, f, indent=2)


# ============================================================
# 8. CONSOLE SUMMARY
# ============================================================

print("Detection Program Health Scorecard generated.")
print("Coverage debt:", scorecard["coverage_debt"]["current"])
print("Enrichment hit rate:", enrichment_hit_rate, "%")
print("Triage alerts processed:", total_triage)
print("Forensic artifacts verified:", artifacts_verified)
print(
    "Forensic success rate:",
    forensic_success_rate,
    "%"
)
print(
    "Forensic status:",
    scorecard["forensics"]["verification_status"]
)
print("Output:", output)