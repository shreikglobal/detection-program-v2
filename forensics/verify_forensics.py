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

print("Forensic verification started.")

all_verified = True

for artifact in chain["artifacts"]:
    path = EVIDENCE / artifact["artifact"]

    original_hash = artifact["sha256"]
    current_hash = sha256_file(path)

    verified = original_hash == current_hash

    print(
        f"{artifact['artifact']} | "
        f"Original: {original_hash} | "
        f"Current: {current_hash} | "
        f"Verified: {verified}"
    )

    if not verified:
        all_verified = False

report = {
    "case_id": chain["case_id"],
    "verification_status": "VERIFIED" if all_verified else "TAMPERED",
    "artifacts_verified": len(chain["artifacts"]),
    "all_hashes_match": all_verified
}

output = BASE / "verification_report.json"

with open(output, "w", encoding="utf-8") as f:
    json.dump(report, f, indent=2)

print()
print("Verification completed.")
print(f"Overall status: {report['verification_status']}")
print(f"Verification report: {output}")