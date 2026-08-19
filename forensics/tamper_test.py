import json
import hashlib
from pathlib import Path

BASE = Path(__file__).parent
EVIDENCE = BASE / "evidence"
CHAIN_FILE = BASE / "chain_of_custody.json"


def sha256_file(path):
    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)

    return h.hexdigest()


with open(CHAIN_FILE, "r", encoding="utf-8") as f:
    chain = json.load(f)

# Use a copy so the original evidence remains unchanged
source = EVIDENCE / "api_call_log.json"
tampered = EVIDENCE / "api_call_log_tampered.json"

tampered.write_bytes(source.read_bytes())

# Simulate unauthorized modification
with open(tampered, "a", encoding="utf-8") as f:
    f.write("\nUNAUTHORIZED MODIFICATION\n")

original_hash = None

for artifact in chain["artifacts"]:
    if artifact["artifact"] == "api_call_log.json":
        original_hash = artifact["sha256"]
        break

current_hash = sha256_file(tampered)

tampered_detected = original_hash != current_hash

report = {
    "test": "Tamper Detection",
    "original_artifact": "api_call_log.json",
    "tampered_artifact": "api_call_log_tampered.json",
    "original_sha256": original_hash,
    "tampered_sha256": current_hash,
    "tamper_detected": tampered_detected,
    "status": "TAMPERED" if tampered_detected else "NOT_DETECTED"
}

output = BASE / "tamper_report.json"

with open(output, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print("Tamper detection test completed.")
print(f"Original SHA-256 : {original_hash}")
print(f"Tampered SHA-256 : {current_hash}")
print(f"Tamper detected  : {tampered_detected}")
print(f"Status           : {report['status']}")
print(f"Report           : {output}")