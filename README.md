# Detection Program V2

## Threat Detection Engineering Platform

A practical detection engineering project focused on repeatable adversary emulation, detection SLO enforcement, threat intelligence enrichment, automated alert triage, forensic evidence integrity, and detection program health measurement.

## Project Objective

The goal of this project is to build a repeatable and measurable threat detection program that can:

- Execute ATT&CK-based adversary emulation
- Measure detection coverage and coverage debt
- Enforce detection SLOs and noise budgets
- Automatically enrich alerts with threat intelligence
- Assign confidence scores and automate alert triage
- Collect and verify forensic evidence using cryptographic hashes
- Detect evidence tampering
- Generate a detection program health scorecard

## Project Stages

### Stage 1 — Repeatable Adversary Emulation
A configurable emulation platform executes selected ATT&CK techniques and generates machine-readable coverage reports and coverage deltas.

### Stage 2 — Detection SLO
Detection rules are evaluated using false-positive noise budgets and coverage debt thresholds. Rules exceeding the allowed noise budget can be demoted and escalated.

### Stage 3 — Threat Intelligence Enrichment
Alerts are automatically enriched with adversary group, campaign context, IOC confidence and enrichment latency information.

### Stage 4 — Automated Triage
Alerts receive confidence scores and are automatically classified into:
- ESCALATE
- HUMAN_REVIEW
- SUPPRESS

### Stage 5 — Forensic Chain of Custody
Forensic artifacts are collected with cryptographic hashes, verified through re-hashing, and tested for tampering.

### Stage 6 — Detection Program Health Scorecard
A health scorecard combines detection coverage, noise budget, coverage debt, threat-intelligence enrichment, triage and forensic metrics.

## Repository Structure

```text
detection-program-v2/
├── detections/
├── emulation/
├── intel/
├── triage/
├── forensics/
├── scorecard/
├── docs/
└── README.md
