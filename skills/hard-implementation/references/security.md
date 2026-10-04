# Universal Security Gate

This adds coverage to original sections 14, 15, 17, 24, 34, 35 and 38; it does not
replace their risk tiers, tests, independent review or completion rules.
Assess applicability before production edits. Use controls for the actual stack
and changed attack surfaces; do not demand irrelevant web/mobile/infrastructure controls.
For LOW-risk documentation-only work, a brief applicability rationale is sufficient.
For security-sensitive work, record the following in existing feature evidence or
the checkpoint; do not create a competing task queue or copy secrets into evidence.

## Threat model and control selection

- Identify protected assets, data classification, confidentiality/integrity/availability
  impact, actors, attacker-controlled inputs, entry points and external services.
- Map trust boundaries, privileged operations and realistic abuse cases, including
  cross-user/tenant access, compromised integrations and unintended resource use.
- For each meaningful threat record the attack path, affected asset, existing and
  required controls, verification method, result and residual risk.
- Select applicable categories below. Record a reason for exclusions; unknown
  applicability is an investigation item, not evidence that a control is unnecessary.

## Applicable security controls

1. **Authentication and sessions:** cover creation/expiry, fixation, logout invalidation,
   refresh rotation/reuse, revocation, concurrent/device sessions and remember-me.
   Review reset/recovery and email/phone verification; cookies, CSRF and token audience/
   issuer/signature validation apply where that architecture requires them.
2. **Authorization:** enforce server/domain checks for every object, property and
   privileged action; test IDOR/BOLA, horizontal/vertical escalation, tenant isolation,
   revoked users and cross-account access. UI visibility is not access control.
3. **Input and output:** validate schemas, types, sizes and business constraints at
   trust boundaries; use contextual encoding and parameterized APIs. Check applicable
   XSS, HTML/template, SQL/NoSQL/LDAP/header/command injection, XXE/deserialization,
   mass assignment, parameter pollution, regex DoS, unsafe URLs and open redirects.
4. **Data protection and privacy:** minimize collection/retention, protect storage,
   backups/caches and deletion/export paths; keep sensitive data out of examples,
   client bundles, test fixtures, analytics, crash reports and error responses.
5. **Secrets lifecycle:** identify secret sources/readers; separate dev/test/prod,
   use least privilege, protect .env/CI/runtime storage and assess rotation/revocation.
   Check new diffs/artifacts for exposure; inspect relevant history if leakage is
   suspected. Do not rewrite history or rotate production credentials without authorization.
6. **Cryptography:** use maintained libraries and appropriate established algorithms;
   check password hashing, secure randomness, key generation/storage/rotation,
   nonce/IV reuse and encryption needs. Do not invent cryptography or disable verification.
7. **Network and transport:** require appropriate TLS/certificate validation; examine
   cleartext traffic, mixed content, WebSockets, proxy trust and platform network
   settings. Certificate pinning needs a justified platform and recovery strategy.
8. **SSRF and outbound requests:** validate schemes/destinations and every redirect;
   cover DNS rebinding and private/loopback/link-local/metadata-service targets.
   Apply appropriate egress policy, timeouts and response limits; URL syntax checks alone fail.
9. **Abuse and resource limits:** test brute force/enumeration, OTP/SMS/email/reset
   abuse and sensitive business-flow automation. Bound quotas, payloads, pagination,
   uploads, concurrency and expensive operations at appropriate identities/boundaries.
10. **Third-party trust:** runtime-validate external responses/IDs and failure modes;
    verify webhook signatures over the correct bytes, timestamps/replays and
    idempotency. Bound retries/redirects and reject malformed or unauthenticated events.
11. **Dependencies and supply chain:** review new/transitive packages, source/provenance,
    names/typosquatting, lockfile changes and install/build scripts before executing them.
    Use available relevant vulnerability/provenance checks; triage findings, tool
    limitations and affected versions instead of treating a clean scan as proof of safety.
12. **Files and uploads:** treat names, extensions and MIME claims as untrusted;
    constrain paths, actual content/type, size/count and archive expansion/symlinks.
    Store with appropriate access/execution restrictions; apply scanning where justified.
13. **Platform security:** apply relevant web headers/CORS/CSP and safe rendering.
    For mobile/desktop, review Keychain/Keystore, local DB/backup, clipboard/screen
    leakage, deep links, WebViews, exported components/intents and tampering assumptions.
14. **Infrastructure and configuration:** examine production defaults, debug/admin
    exposure, IAM/service privileges, CI/workflow permissions and deployment boundaries.
    Keep environments separated; configuration/IaC changes require relevant verification.
15. **Logging and audit:** verify useful, access-controlled audit records without secret/
    payload leakage in logs, traces, metrics or reports; cover retention and failure behavior.

## Verification and closure

Add focused negative/abuse tests and affected regressions for selected threats;
inspect actual implementation/configuration, not just checklist words or pattern scans.
Apply the original risk-based independent review obligations and disclose missing
fresh-context/tool support. Record PASS/FAIL/unavailable distinctly with command/result
and relevant revision; an unrun applicable check cannot justify LOCAL_CLEAN_GATE = PASS.
Unresolved material security findings block clean closure; describe blockers/residual
risk and any required external action honestly. Do not assign numerical security
ratings, claim certification, or authorize production attacks/secret changes by this gate.

Use [OWASP ASVS](https://owasp.org/projects/asvs) and [API Security](https://api-security.owasp.org/editions/2023/en/0x11-t10/)
for applicable web/API controls, [MASVS](https://mas.owasp.org/MASVS/) for mobile, and
[NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final) for secure development/supply chain.
If referencing specific requirements, record the standard/version actually consulted.
