import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
import subprocess

BASE = Path(__file__).parent
EVIDENCE = BASE / "evidence"
EVIDENCE.mkdir(exist_ok=True)

def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()

# Process list
process_file = EVIDENCE / "process_list.txt"
result = subprocess.run(
    ["tasklist"],
    capture_output=True,
    text=True,
    shell=True
)
process_file.write_text(result.stdout, encoding="utf-8")

# API call log - controlled test artifact
api_file = EVIDENCE / "api_call_log.json"
api_data = {
    "event": "API_CALL_TEST",
    "service": "Detection-Test-Service",
    "action": "GetObject",
    "timestamp": datetime.now(timezone.utc).isoformat()
}
api_file.write_text(json.dumps(api_data, indent=2), encoding="utf-8")

# Memory snapshot placeholder for the lab evidence package
memory_file = EVIDENCE / "memory_snapshot.txt"
memory_file.write_text(
    "LAB MEMORY SNAPSHOT PLACEHOLDER\n"
    "This controlled artifact represents the memory snapshot evidence item.\n",
    encoding="utf-8"
)

# Chain of custody
collector = "automated-forensics-collector"
collected_at = datetime.now(timezone.utc).isoformat()

artifacts = []

for path in [memory_file, process_file, api_file]:
    artifacts.append({
        "artifact": path.name,
        "triggered_by": collector,
        "collected_at": collected_at,
        "source_system": "local-test-system",
        "sha256": sha256_file(path),
        "storage_location": str(path)
    })

record = {
    "case_id": "CASE-001",
    "collection_status": "COMPLETED",
    "collector": collector,
    "artifacts": artifacts
}

output = BASE / "chain_of_custody.json"
output.write_text(json.dumps(record, indent=2), encoding="utf-8")

print("Forensic collection completed.")
print(f"Artifacts collected: {len(artifacts)}")
print(f"Chain of custody: {output}")