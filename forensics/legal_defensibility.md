\# Legal Defensibility Statement



The forensic collection process is designed to preserve evidence integrity through a documented chain of custody. For each collected artifact, the system records the artifact identity, collection time, triggering collector, source system, storage location, and SHA-256 hash. The original hash provides an integrity reference that can be independently verified by re-hashing the stored artifact.



The verification process demonstrated that unchanged artifacts produce matching SHA-256 values. A controlled tampering test also demonstrated that modification changes the cryptographic hash and is detected as TAMPERED. This provides technical evidence that the collected artifacts were not silently modified after collection.



This chain-of-custody approach can support evidence handling in jurisdictions where electronically stored evidence is admissible when authenticity, integrity, and reliable handling procedures can be demonstrated. The exact admissibility requirements depend on the applicable jurisdiction, court, and investigation context; therefore, this technical record should be supplemented by organizational policies and appropriate legal procedures.



A defence attorney could challenge the evidence if the organization cannot prove who had access to the evidence after collection, whether the collection system itself was trustworthy, or whether the original source system and collection process were properly authenticated. Another potential gap is incomplete documentation of access history or custody transfers.



Therefore, the chain-of-custody record should be retained with the artifacts and access history, and all investigators or systems handling the evidence should be recorded.

