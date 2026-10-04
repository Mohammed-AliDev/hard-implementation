  # UNIVERSAL SPECKIT HARD-IMPLEMENTATION WORKFLOW

Use the `hard-implementation` workflow for this entire implementation.

This prompt is intentionally:

* project-agnostic;
* technology-agnostic;
* framework-agnostic;
* language-agnostic;
* architecture-aware;
* workload-driven;
* SpecKit-oriented;
* local-first;
* multi-agent when available;
* evidence-driven;
* risk-based.

This workflow is technology-, language-, framework-, architecture-, and platform-agnostic.

Discover the actual repository before assigning work.

It must adapt to:

* client applications;
* backend services;
* libraries/CLIs;
* infrastructure;
* embedded systems;
* data/ML;
* monorepos;
* multi-platform systems;
* combinations of these.

Never assume a layer or technology that is not present.

==================================================
0. TARGET
==================================================

Repository:

Use the current repository/workspace unless an explicit repository path is provided.

Target feature:

Use the SpecKit feature explicitly identified by the user or current task.

If no explicit Spec identifier is given:

1. inspect the current branch;
2. inspect the SpecKit directories;
3. inspect recently active feature files;
4. inspect current task context.

Auto-select the feature only when the target is unambiguous.

If multiple active Specs are genuinely indistinguishable and choosing one would risk modifying the wrong feature, ask exactly one concise clarification.

Do not ask for tickets.

The target Spec's `tasks.md` is the execution queue.

==================================================
1. SOURCE-OF-TRUTH HIERARCHY
==================================================

The minimum expected authoritative SpecKit files are normally:

* `spec.md`
* `plan.md`
* `tasks.md`

Other SpecKit/project files may exist.

Discover them rather than assuming their names.

Examples may include:

* constitution/project principles;
* research notes;
* data models;
* API contracts;
* quickstarts;
* checklists;
* architecture documents;
* test plans;
* ADRs;
* repository instructions.

Use this authority order:

1. target Spec `spec.md`;
2. target Spec `plan.md`;
3. target Spec `tasks.md`;
4. repository-level instructions that explicitly govern implementation;
5. SpecKit constitution/project rules if present;
6. actual production architecture and existing implementation;
7. existing contracts/schema/generated-source conventions;
8. existing test/build/tool configuration;
9. relevant neighboring Specs/features;
10. historical documentation only when needed.

Important:

Do NOT require any custom project-specific governance files.

Do NOT assume the existence of files such as:

* `ENGINEERING_GATES.md`
* `ENGINEERING_PATTERNS.md`
* `FEATURE_MAP.md`
* `Decision_Log.md`
* `Future_Ideas.md`

If similar files happen to exist, they may be consulted when relevant, but they are OPTIONAL and must never be required for this workflow.

Never fail merely because such files do not exist.

==================================================
2. ABSOLUTE LOCAL-FIRST MODE
==================================================

This run is LOCAL FIRST unless the user explicitly overrides this section.

DO NOT:

* push;
* merge to the main/default branch;
* open a pull request;
* update a pull request;
* depend on remote CI;
* wait for remote CI;
* claim remote CI passed;
* use remote repository operations unless explicitly requested.

Normal local Git operations are allowed:

* `git status`
* `git diff`
* `git log`
* `git branch`
* `git switch`
* `git worktree`
* `git add`
* `git commit`

Local commits are allowed and encouraged.

At completion:

* leave the implementation reviewed locally;
* leave it on the feature branch;
* do not merge to main/default;
* do not push unless explicitly requested.

Remote repository work can happen later.

==================================================
3. START WITH A FRESH ORCHESTRATOR
==================================================

Immediately establish a fresh orchestrator context.

The orchestrator is primarily:

* coordinator;
* architect;
* integrator;
* dependency manager;
* reviewer scheduler;
* evidence manager.

The orchestrator SHOULD NOT implement the entire feature itself when safe delegation is available.

The orchestrator owns:

* repository baseline;
* Spec reconciliation;
* architecture discovery;
* technology discovery;
* capability discovery;
* dependency graph;
* work-unit creation;
* dynamic agent topology;
* file ownership;
* parallel execution;
* dependency tracking;
* reviewer allocation;
* findings aggregation;
* conflict prevention;
* local integration;
* test strategy;
* evidence tracking;
* final whole-feature review;
* local commits;
* final report.

Optimize simultaneously for:

1. correctness;
2. depth;
3. implementation quality;
4. maintainability;
5. execution speed.

Do not serialize work that can safely execute in parallel.

Do not use fake parallelism where tasks actually depend on one another.

==================================================
4. CAPABILITY DISCOVERY
==================================================

Before planning execution, determine what capabilities are actually available.

Discover whether the environment supports:

* sub-agents;
* parallel agents;
* isolated agent contexts;
* maximum useful/supported agent concurrency;
* terminal execution;
* code editing;
* test execution;
* browser/web access;
* database access;
* containers;
* emulators;
* simulators;
* GUI testing;
* worktrees;
* platform-specific build tools.

Never pretend a capability exists.

If multiple agents are unavailable:

preserve the same workflow sequentially using fresh implementation/review contexts where possible.

If only a small number of parallel agents are available:

adapt the execution graph accordingly.

If substantial concurrency is available:

use it when the dependency graph and file ownership make it safe and useful.

Never reduce correctness requirements merely because fewer agents are available.

Never create unnecessary agents merely because additional agent slots exist.

The workflow must degrade gracefully without changing correctness requirements.

==================================================
4A. EXECUTION DEPTH CLASSIFICATION
==================================================

Before constructing the full workflow, classify the target implementation:

TIER 1 — SMALL

Examples:

* localized bug fix;
* simple field;
* isolated UI behavior;
* small library change.

Use:

* minimal context discovery;
* one implementer;
* one review where appropriate;
* narrow tests;
* no unnecessary multi-agent orchestration;
* no clean-room rebuild unless risk justifies it.

TIER 2 — SUBSTANTIAL

Examples:

* multi-file feature;
* moderate domain changes;
* persistence or API integration;
* multiple independent work units.

Use:

* DAG;
* ownership;
* adaptive parallel agents;
* risk-based review;
* checkpoint testing;
* final integration review.

TIER 3 — CRITICAL / CROSS-CUTTING

Examples:

* auth;
* payments;
* medical;
* financial;
* migrations;
* concurrency;
* offline synchronization;
* cross-service consistency;
* major architectural changes.

Use the complete hard-implementation workflow:

* full dependency DAG;
* maximal safe parallelism;
* dual high-risk reviewers;
* clean-room gate;
* specialist reviews;
* adversarial integration review;
* evidence matrix.

==================================================
5. TECHNOLOGY DISCOVERY — NEVER ASSUME THE STACK
==================================================

Before implementation, inspect the repository and build a concise TECHNOLOGY MAP.

Identify, where applicable:

* programming languages;
* frameworks;
* frontend technology;
* mobile technology;
* desktop technology;
* backend technology;
* database technology;
* ORM/query layer;
* package managers;
* monorepo tooling;
* build systems;
* API style;
* schema/contract systems;
* code-generation tools;
* state-management libraries;
* networking libraries;
* authentication system;
* authorization system;
* storage;
* queues/events;
* background workers;
* caches;
* native/platform integrations;
* test frameworks;
* integration-test infrastructure;
* E2E tooling;
* lint tools;
* formatters;
* static analyzers;
* type checkers;
* migration tooling;
* deployment-related config where relevant.

Inspect real repository files.

Examples include:

* `package.json`
* lockfiles;
* `pubspec.yaml`
* `Cargo.toml`
* `go.mod`
* `pyproject.toml`
* `requirements.txt`
* Gradle files;
* Maven files;
* `.csproj`;
* solution files;
* workspace files;
* Docker files;
* CI config;
* test configs;
* compiler configs;
* lint configs.

These are examples only.

Do not assume they exist.

Do not infer missing layers.

Examples:

If only a Flutter mobile application exists:

do not invent backend work.

If only a backend exists:

do not invent UI work.

If both mobile and desktop applications exist:

discover whether they share:

* domain code;
* contracts;
* generated clients;
* packages;
* business rules;

before assigning work.

==================================================
6. COMMAND DISCOVERY
==================================================

Build an internal COMMAND MATRIX from the project itself.

Determine the actual commands for:

* dependency installation;
* formatting;
* linting;
* type checking;
* compilation/build;
* code generation;
* migrations;
* migration rollback if supported;
* unit tests;
* integration tests;
* database tests;
* contract tests;
* UI tests;
* widget/component tests;
* E2E tests;
* security checks;
* static analysis;
* performance tests;
* packaging if locally available.

Prefer repository-defined scripts over invented commands.

Do NOT guess commands merely because a framework commonly uses them.

Inspect:

* scripts;
* Makefiles;
* task runners;
* project documentation;
* workspace configuration;
* package configuration.

If an expected command does not exist, record that fact.

Do not introduce a new tool solely to satisfy this workflow unless the Spec or repository architecture actually requires it.

==================================================
7. FAST CONTEXT BOOTSTRAP
==================================================

Before modifying production code, read:

1. target `spec.md`;
2. target `plan.md`;
3. target `tasks.md`;
4. applicable SpecKit/project constitution;
5. repository-level agent/development instructions;
6. relevant production implementation;
7. neighboring Specs that the target feature depends on;
8. relevant schema/contracts;
9. relevant generated-code conventions;
10. relevant test architecture;
11. latest migration/schema state where applicable.

Do NOT read the entire repository linearly.

Do NOT read every historical document.

Build a concise internal FEATURE CONTEXT containing:

* feature purpose;
* user-visible behavior;
* business invariants;
* domain entities;
* state transitions;
* persistence invariants;
* authorization boundaries;
* privacy/security boundaries;
* external dependencies;
* cross-feature dependencies;
* contract boundaries;
* generated-code rules;
* UI/runtime rules;
* expected failure behavior;
* concurrency requirements;
* idempotency requirements;
* recovery requirements;
* test requirements;
* acceptance criteria.

==================================================
8. REPOSITORY BASELINE
==================================================

Before modifications:

* record current branch;
* record HEAD SHA;
* inspect `git status`;
* inspect untracked files;
* preserve unrelated local modifications;
* inspect recent relevant history;
* identify relevant existing migrations/schema revisions;
* identify relevant tests;
* inspect actual runtime behavior around feature boundaries;
* run the smallest useful baseline checks.

Record pre-existing failures separately.

Never silently attribute an existing failure to the new feature.

Do not fix unrelated technical debt unless:

1. it blocks the target Spec;
2. the new feature would materially worsen it;
3. it violates an authoritative requirement needed by this implementation.

==================================================
9. DISCOVER CROSS-SPEC / CROSS-FEATURE DEPENDENCIES
==================================================

Do not assume feature numbers or neighboring Specs.

Discover dependencies from:

* the target Spec;
* plan;
* tasks;
* imports;
* schema relations;
* routes;
* services;
* shared models;
* contracts;
* state transitions;
* event flows;
* existing tests.

Build a dependency map such as:

TARGET FEATURE
    ↓
Feature/API/Module A
    ↓
Feature/Module B

For every dependency determine:

* who owns the source of truth;
* which feature may mutate it;
* which feature may only consume it;
* which invariants cross the boundary.

Do not duplicate another feature's responsibility silently.

==================================================
10. BUILD A DEPENDENCY DAG — NOT A LINEAR TODO LIST
==================================================

Treat `tasks.md` as the authoritative work queue.

Convert tasks into WORK UNITS.

A work unit may contain multiple task IDs when tightly coupled.

For every work unit identify:

* task IDs;
* intended claim/output;
* owned files;
* prerequisites;
* dependents;
* persistence impact;
* contract impact;
* generated-code impact;
* client impact;
* frontend/mobile/desktop impact where applicable;
* backend impact where applicable;
* infrastructure impact where applicable;
* platform/native impact where applicable;
* tests required;
* risk level;
* parallel safety;
* required reviewer expertise.

Create execution WAVES.

Generic example:

Wave A:
* architecture reconnaissance;
* domain analysis;
* persistence preparation;
* contract analysis;
* UI/client reconnaissance;
* platform integration reconnaissance.

Wave B:
* foundational state/schema changes;
* contracts/interfaces;
* shared abstractions.

Wave C:
* domain/runtime implementation;
* integration boundaries;
* generated consumers;
* platform-independent implementation.

Wave D:
* UI/client integration;
* platform integrations;
* recovery/error states;
* independent security/test work.

Wave E:
* system integration;
* hardening;
* evidence.

This is only a shape.

Derive the actual DAG from the repository and target Spec.

Do not force every project into these Waves.

==================================================
11. FILE OWNERSHIP
==================================================

Every active implementation agent must have explicit FILE OWNERSHIP.

Maintain an internal ownership map.

Only one active writer may own the same sensitive artifact at once.

Examples:

* same migration;
* same schema file;
* same contract file;
* same generated-output directory;
* same lockfile;
* same core transaction/function;
* same central state machine;
* same shared configuration;
* same evidence section.

If two tasks require the same core file:

* serialize them;
or
* assign one writer ownership.

Reviewers may inspect the same files concurrently.

Reviewers must not concurrently edit shared production files.

Directory ownership alone is insufficient when multiple agents can still modify the same shared files.

Explicitly account for shared/generated files.

==================================================
12. WORKLOAD-DRIVEN AGENT TOPOLOGY
==================================================

Do not map agents directly to application layers.

Derive agent roles from the target Spec's independent work units.

Agent and reviewer counts are demand-driven. Derive them from independent work units, risk domains, dependencies, ownership conflicts, and environment capability. Never create or preserve an agent role merely to reach a target count.

A single-platform project may still justify many parallel agents.

The number of platforms does NOT determine the number of useful agents.

The number of independent, safely parallelizable work units does.

Examples:

Mobile-only:

* UI/navigation;
* domain/state;
* networking;
* persistence/offline;
* platform integration;
* accessibility/localization;
* testing;
* security/performance review.

Backend-only:

* schema;
* domain;
* API/contracts;
* authorization;
* workers/events;
* caching;
* testing;
* concurrency/performance review.

Frontend-only:

* components;
* state;
* routing;
* API consumer;
* accessibility;
* performance;
* testing.

Desktop-only:

* UI/window lifecycle;
* state/domain;
* persistence;
* OS integrations;
* packaging/runtime behavior;
* accessibility;
* testing;
* performance/security review.

Library/package-only:

* public API;
* internal implementation;
* compatibility;
* serialization/contracts;
* platform compatibility;
* tests;
* performance;
* documentation/examples where required.

Embedded/firmware:

* hardware abstraction;
* control/state logic;
* communication;
* concurrency/timing;
* persistence/configuration;
* fault handling;
* test harness;
* hardware-boundary review.

Data/ML:

* ingestion;
* preprocessing;
* feature/data validation;
* model/training code;
* evaluation;
* reproducibility;
* serving/inference;
* data/privacy/performance review.

Multi-platform/full-stack:

derive work units from actual dependencies.

Do NOT automatically create:

* one mobile agent;
* one desktop agent;
* one backend agent;
* one database agent;

unless the Spec's actual independent work naturally divides that way.

For example, a mobile-only Spec might safely use six or more agents if independent work exists across:

* UI;
* state;
* persistence;
* networking;
* native integration;
* tests;
* accessibility;
* performance.

Likewise a full-stack feature might need only two agents if most work touches one shared transaction or one central contract.

The orchestrator must dynamically create agent roles based on actual work.

Agent roles may change between dependency waves.

An agent topology suitable for Wave A does not have to remain unchanged in Wave B or the final review.

==================================================
13. PARALLELISM POLICY — MAXIMUM SAFE AND USEFUL
==================================================

Use the maximum SAFE and USEFUL parallelism supported by the current environment.

Determine the environment's available concurrency/capability first.

Prefer approximately 4–6 concurrent agents for substantial feature work when enough independent work units exist.

This is a practical preference, NOT a hard limit.

Use fewer when:

* the feature is small;
* dependencies require serialization;
* several tasks modify the same critical files;
* one foundational contract must stabilize first;
* coordination cost would exceed parallelism benefit.

Use more than six when:

* the execution environment supports it;
* there are genuinely independent work units;
* file ownership is non-overlapping;
* dependency boundaries are clear;
* coordination overhead remains justified;
* enough meaningful work exists.

Never split one cohesive operation unnaturally merely to increase concurrency.

Never leave useful parallelism unused without a concrete dependency, ownership, or coordination reason.

Parallelism is demand-driven, not quota-driven.

The orchestrator must continuously reevaluate parallelism after each dependency wave.

Example:

Wave A may safely use 7 agents.

Wave B may require only 2 because a shared schema or contract is being stabilized.

Wave C may expand back to 5 independent implementers.

Final review may use a different set of specialist reviewers.

Do not assume the implementation-agent topology must equal the review-agent topology.

Possible allocation for one substantial feature might be:

* Implementer A — persistence/state;
* Implementer B — domain logic;
* Implementer C — contracts/integration;
* Implementer D — client/UI;
* Implementer E — platform/native integration;
* Test specialist F;
* Reviewer G — security/concurrency;
* Reviewer H — domain/contracts.

This is only an example.

Do not treat these roles as mandatory.

Adapt them dynamically to the discovered work units.

==================================================
14. RISK CLASSIFICATION
==================================================

Classify every work unit.

CRITICAL/HIGH examples:

* authentication;
* authorization;
* payments;
* financial transactions;
* medical data;
* personal data;
* destructive operations;
* database invariants;
* concurrency;
* idempotency;
* cryptography;
* permissions;
* state machines;
* migrations;
* cross-service consistency;
* data loss;
* audit/history;
* irreversible operations;
* synchronization;
* offline reconciliation;
* contract-breaking changes;
* security-sensitive native/platform integration.

HIGH/CRITICAL requires:

* implementation;
* focused tests;
* affected regressions;
* TWO independent reviewer perspectives before closure.

MEDIUM examples:

* ordinary controller/handler wiring;
* standard repository consumers;
* UI state handling;
* non-critical integrations;
* ordinary platform wiring.

MEDIUM requires:

* implementation;
* affected tests;
* ONE independent reviewer.

LOW examples:

* factual documentation updates;
* naming;
* evidence bookkeeping;
* non-runtime refactoring.

LOW requires:

* targeted validation.

Risk may be raised whenever implementation reveals hidden complexity.

==================================================
15. IMPLEMENTATION LOOP
==================================================

For each work unit:

"Fresh context" means an independent context that has not participated in the implementation when the environment supports it.

If true isolated contexts are unavailable, emulate independence by withholding implementer conclusions and providing only authoritative artifacts, diff, code, and tests.

------------------------------
A. FRESH IMPLEMENTER
------------------------------

Assign a fresh implementation context.

Provide:

* task IDs;
* relevant Spec sections;
* relevant Plan sections;
* repository conventions;
* dependency outputs;
* owned files;
* required tests;
* required evidence.

The implementer must inspect existing production code before editing.

Then:

1. understand existing behavior;
2. implement the minimal correct design;
3. preserve project architecture unless change is justified;
4. add tests with the implementation;
5. run narrow relevant tests immediately;
6. run directly affected regressions;
7. report:
   - files changed;
   - invariants implemented;
   - tests added;
   - tests executed;
   - assumptions;
   - known risks.

For high-risk work:

do not allow "implementation now, tests much later."

------------------------------
B. INDEPENDENT SPECIALIST REVIEW
------------------------------

For HIGH/CRITICAL work use TWO independent reviewer perspectives.

Run them concurrently where safe and supported.

Reviewer perspective 1 should emphasize where applicable:

DATA / CONCURRENCY / SECURITY

Check:

* transaction boundaries;
* atomicity;
* constraints;
* foreign keys;
* uniqueness;
* races;
* locking;
* deadlocks;
* isolation;
* idempotency;
* authorization;
* tenant/account isolation;
* insecure direct object references;
* sensitive data;
* durable state validation;
* retry behavior;
* lost responses;
* restart semantics;
* rollback behavior.

Reviewer perspective 2 should emphasize where applicable:

DOMAIN / CONTRACT / PRODUCT / TEST QUALITY

Check:

* Spec/Plan/Tasks parity;
* business semantics;
* state machine;
* feature ownership;
* cross-feature boundaries;
* API/runtime parity;
* generated consumers;
* source of truth;
* client truthfulness;
* test validity;
* edge cases;
* limits;
* pagination;
* bounds;
* error behavior;
* scope creep.

For UI-heavy work, one reviewer may instead specialize in:

UX / ACCESSIBILITY / PLATFORM LIFECYCLE.

For platform-native work, one reviewer may specialize in:

* Android lifecycle;
* iOS lifecycle;
* desktop OS behavior;
* permissions;
* background execution;
* hardware/device behavior;

as appropriate.

Reviewers MUST inspect actual:

* diff;
* implementation;
* tests;
* configuration.

Do not trust implementer summaries.

------------------------------
C. FINDINGS AGGREGATION
------------------------------

Deduplicate findings by ROOT CAUSE.

Classify findings:

* BLOCKER
* CRITICAL
* HIGH
* MEDIUM
* LOW
* NOTE

BLOCKER

Implementation cannot safely proceed or feature cannot be validated.

CRITICAL

Likely security breach, data loss, financial/medical integrity failure, or catastrophic correctness failure.

HIGH

Material user-visible correctness/security/reliability failure under realistic conditions.

MEDIUM

Real defect with bounded impact that should be fixed before feature closure when relevant to the target.

LOW

Non-blocking maintainability, clarity, robustness, or polish issue.

NOTE

Observation with no required change.

A MEDIUM finding is closure-blocking when it:

* violates a Spec requirement;
* affects the target feature's correctness;
* creates a realistic regression;
* weakens a required security/privacy boundary;
* invalidates required evidence.

Pure maintainability suggestions may remain open if documented.

Closure blockers:

* BLOCKER;
* CRITICAL;
* HIGH;
* closure-blocking MEDIUM.

Do not force reviewers to invent findings.

A reviewer may return:

`NO_IMPORTANT_FINDINGS`

------------------------------
D. DESIGNATED FIXER
------------------------------

Assign ONE designated fixer for a finding set affecting shared code.

The fixer must:

* correct the root cause;
* add/update regression coverage;
* strengthen enforcement where practical;
* run affected tests.

Avoid several agents concurrently applying overlapping fixes.

------------------------------
E. RE-REVIEW
------------------------------

For HIGH/CRITICAL corrections:

use fresh review context after fixes.

Exit the work unit only with:

* 0 blocker;
* 0 critical;
* 0 high;
* 0 unresolved closure-blocking MEDIUM.

Do not create infinite loops for cosmetic LOW findings.

==================================================
16. ROOT-CAUSE PREVENTION
==================================================

Whenever a defect is found classify it as:

* NEW ROOT CAUSE;
or
* REPEATED ROOT CAUSE.

For repeated causes ask:

"Why was the existing prevention unable to stop this?"

Prefer fixing the problem at the strongest practical layer:

human review
→ automated regression
→ static analysis/lint
→ local validation gate
→ compiler/type system
→ contract/schema validation
→ persistence/database constraint
→ architecture that makes the invalid state impossible.

Do not merely patch repeated symptoms.

If automation is impractical, document why.

==================================================
17. STATIC / PATTERN SCANS — ADAPT TO THE TECHNOLOGY
==================================================

Before a work unit is considered clean, inspect relevant production code for risky patterns appropriate to the discovered stack.

Examples include:

* unsafe type casts;
* unchecked deserialization;
* trusting persisted JSON without runtime validation;
* duplicate handwritten contract models;
* bypassing generated clients;
* raw SQL interpolation;
* command injection;
* path traversal;
* hard-coded credentials;
* insecure token handling;
* sensitive-data logging;
* unbounded queries;
* unchecked pagination;
* missing authorization;
* client-authored authoritative state;
* client clock used as server/domain authority;
* production imports of mocks/fakes;
* TODO/FIXME in required runtime paths;
* swallowed exceptions;
* generic state/status mutation APIs;
* direct mutation that bypasses domain invariants;
* lifecycle resource leaks;
* unsafe platform permission handling;
* insecure local storage where sensitive data exists.

These are examples.

Do NOT mechanically scan only TypeScript patterns in a Rust project or Flutter patterns in a Python service.

Use technology-appropriate equivalents.

Explicitly justify meaningful exceptions.

==================================================
18. DOMAIN-BOUND CONSISTENCY REVIEW
==================================================

Compare related limits and cardinalities across layers.

Examples:

* UI limits vs API limits;
* API limits vs database constraints;
* pagination vs possible row counts;
* text limits vs storage limits;
* client enum vs server enum;
* timeout vs retry policy;
* cache lifetime vs state lifetime;
* version identity vs mutable dependencies;
* upload limit vs server/storage limit;
* queue size vs worker behavior;
* local state vs authoritative remote state;
* platform limitations vs product assumptions.

Never assume an upstream value is bounded unless it is actually enforced.

==================================================
19. DURABLE DATA VALIDATION
==================================================

Any persisted state that will later be trusted must have appropriate validation.

Examples:

* JSON;
* JSONB;
* local persistent storage;
* snapshots;
* idempotency replay;
* cached server payloads;
* recovery state;
* serialized events;
* job payloads;
* offline synchronization data;
* configuration files;
* device-local persistent state.

Static typing alone is not runtime validation.

Malformed durable state should fail safely using stable project-appropriate error behavior.

==================================================
20. DATABASE / PERSISTENCE REVIEW — WHEN APPLICABLE
==================================================

If the feature modifies persistent state, identify for every high-risk mutation:

* stores/tables/files touched;
* transaction/atomicity boundary;
* lock order where applicable;
* isolation expectations;
* invariants read;
* invariants written;
* audit/history behavior;
* idempotency behavior;
* error behavior;
* retry behavior;
* rollback behavior.

Where correctness depends on database concurrency:

use the real database engine whenever practical.

Race tests must use genuine concurrent execution.

Do not claim concurrency safety from sequential mocks.

If a project does NOT use a database:

adapt this section to its actual persistence/state mechanism.

Examples:

* local device storage;
* filesystem;
* key-value store;
* browser storage;
* embedded flash;
* in-memory state;
* remote API state.

Do not invent a database merely because this section exists.

==================================================
21. CONTRACT-FIRST — WHEN THE PROJECT HAS CONTRACTS
==================================================

Discover whether the project uses:

* OpenAPI;
* GraphQL schema;
* Protobuf;
* JSON Schema;
* generated SDKs;
* typed RPC;
* interface-definition files;
* another contract source of truth.

If contract-owned changes exist, follow the repository's actual source-of-truth flow.

Generic pattern:

contract source
→ validate/lint
→ generate if applicable
→ compile generated consumers
→ runtime parity
→ production consumer tests.

Never hand-edit generated artifacts unless the repository explicitly treats them as editable source.

Only one agent should own generation for the same generated tree at one time.

If the project has no generated contract system:

do not invent one solely for this feature unless the Spec requires it.

==================================================
22. CLIENT / UI IMPLEMENTATION — WHEN APPLICABLE
==================================================

Discover the actual client technology.

Examples:

* Flutter;
* React Native;
* web;
* native mobile;
* desktop;
* terminal UI.

Use the project's existing:

* architecture;
* state management;
* networking;
* navigation;
* design system;
* error handling;
* dependency injection;
* localization;
* accessibility conventions.

Where applicable test:

* initial loading;
* hydration;
* empty state;
* success;
* pending state;
* retry;
* failure;
* stale data;
* reconnect;
* restart/resume;
* optimistic behavior;
* server rejection;
* malformed responses;
* authorization failure;
* race/double submission;
* offline behavior;
* accessibility;
* keyboard behavior;
* focus;
* semantics;
* localization;
* RTL;
* mixed-direction text where relevant;
* text scaling;
* minimum supported viewport/device size;
* lifecycle behavior;
* background/foreground transition where relevant.

Do not show authoritative success before the authoritative operation succeeds unless the product explicitly defines safe optimistic behavior.

==================================================
23. PLATFORM / NATIVE INTEGRATION — WHEN APPLICABLE
==================================================

If the project interacts with platform/native functionality, discover the real platform boundaries.

Examples:

* camera;
* microphone;
* GPS/location;
* Bluetooth;
* NFC;
* filesystem;
* notifications;
* background tasks;
* biometric auth;
* deep links;
* app links;
* desktop OS APIs;
* hardware sensors;
* USB/serial;
* platform permissions.

Review where applicable:

* permission denied;
* permission permanently denied;
* unavailable hardware;
* unsupported OS/version;
* lifecycle interruptions;
* cancellation;
* background/foreground changes;
* resource cleanup;
* platform-specific errors;
* privacy behavior;
* fallback behavior.

Do not assume native integration exists merely because the project is mobile or desktop.

==================================================
24. SECURITY / PRIVACY
==================================================

Determine the data classification and trust boundaries from the feature.

Where applicable test:

* authentication;
* authorization;
* tenant/workspace/project isolation;
* guessed IDs;
* horizontal privilege escalation;
* vertical privilege escalation;
* inactive/revoked users;
* cross-account access;
* unsafe direct object references;
* secrets;
* logs;
* metrics;
* traces;
* errors;
* analytics;
* audit data;
* caches;
* snapshots;
* local storage;
* generated examples;
* test artifacts.

Never log secrets or sensitive payloads merely for debugging convenience.

Authorization must not exist only in the UI.

Server/backend/domain enforcement must exist where the architecture requires it.

If there is no backend in the current repository:

do not invent backend authorization work.

Instead assess the trust boundary that actually exists.

==================================================
25. CONCURRENCY / RETRY / RECOVERY
==================================================

Identify operations vulnerable to:

* double submit;
* duplicate request;
* lost response;
* retry after commit;
* retry before commit;
* stale version;
* two-device mutation;
* restart;
* network reconnect;
* process crash;
* app termination;
* background suspension;
* partial failure;
* competing terminal state changes;
* out-of-order events.

Test these where relevant.

Do not invent concurrency requirements that the feature cannot encounter.

But do not ignore concurrency simply because the happy path works.

For local-only applications, concurrency may still occur through:

* multiple UI events;
* multiple isolates/threads;
* async callbacks;
* background workers;
* native callbacks;
* filesystem access;
* app lifecycle events.

==================================================
26. TEST STRATEGY — FAST FIRST, EXPENSIVE LAST
==================================================

During implementation:

run narrow tests first.

Examples:

* one unit test file;
* one package;
* one integration suite;
* one component/widget test.

At WORK UNIT closure:

run directly affected regression groups.

At CHECKPOINT closure:

run larger category gates.

Run the entire relevant project suite only:

1. at major integration checkpoints;
2. before final local completion.

Do not rerun hundreds or thousands of tests after every trivial edit.

Optimize iteration speed without reducing final confidence.

==================================================
27. TEST THE TESTS
==================================================

For important invariants verify that the tests genuinely prove the claim.

Ask:

* does the production path execute?
* does the test use the real implementation?
* does a generated client really participate where required?
* does the real persistence system participate where required?
* does the race actually execute concurrently?
* did the mutation actually commit/persist?
* does lost-response testing lose the response at the correct point?
* does restart use persisted state?
* would the test fail if the invariant were deliberately broken?
* are important tests skipped?
* did the expected suite actually run?
* is the test accidentally asserting mock behavior rather than production behavior?

Use mutation-style verification selectively for HIGH/CRITICAL behavior.

Never weaken assertions merely to make the suite green.

==================================================
28. MIGRATIONS / SCHEMA CHANGES — WHEN APPLICABLE
==================================================

If migrations exist:

verify where practical:

* migration applies;
* rollback/revert if supported;
* migration reapplies;
* fresh persistence path;
* realistic upgrade path;
* application compatibility;
* generated schema drift where applicable.

Inspect existing migration naming/order conventions.

Do not invent migration numbering conventions.

Do not modify an old production migration unless project policy explicitly allows it.

If migrations do not exist:

skip this section.

==================================================
29. PERFORMANCE — WHEN RELEVANT
==================================================

Identify performance-sensitive paths.

Review where applicable:

* N+1 queries;
* full-table scans;
* unbounded reads;
* unnecessary rebuilds/renders;
* repeated network calls;
* oversized payloads;
* excessive serialization;
* memory growth;
* expensive loops;
* blocking I/O;
* startup regression;
* bundle/package growth;
* unnecessary code generation;
* battery/network impact on mobile;
* excessive background work;
* unnecessary disk writes;
* UI jank;
* event-loop blocking.

Measure rather than speculate when practical.

Do not optimize irrelevant micro-details.

==================================================
30. ACCESSIBILITY / LOCALIZATION — WHEN APPLICABLE
==================================================

For user-facing interfaces inspect where applicable:

* semantics/accessibility labels;
* keyboard navigation;
* focus order;
* screen reader behavior;
* dynamic text scaling;
* contrast conventions;
* touch target behavior;
* locale formatting;
* translated strings;
* RTL;
* mixed RTL/LTR content;
* overflow with longer translations;
* minimum supported viewport.

Use the project's existing accessibility/localization architecture.

Do not introduce localization infrastructure if the project intentionally does not have it and the Spec does not require it.

==================================================
31. MAINTAINABILITY
==================================================

Do not refactor merely because a file is large.

Flag architecture problems when:

* responsibilities are genuinely mixed;
* reasoning becomes materially difficult;
* testing becomes materially difficult;
* transaction ownership is unclear;
* feature ownership is ambiguous;
* new integration substantially worsens the design.

Prefer minimal architecture changes necessary for correct implementation.

Avoid aesthetic refactoring unrelated to the Spec.

==================================================
32. EVIDENCE MATRIX
==================================================

Maintain implementation evidence proportionally to the execution tier.

For TIER 1:

evidence may remain in the final report.

For TIER 2:

create an acceptance matrix when tasks/requirements are numerous or traceability adds value.

For TIER 3:

an acceptance matrix is required unless repository policy defines an equivalent artifact.

When an acceptance matrix is created, the preferred location is:

`<target-spec-directory>/evidence/acceptance-matrix.md`

If repository policy defines another evidence location, follow it.

Record for relevant requirements/tasks:

* requirement/task ID;
* exact claim;
* implementation location;
* validation command;
* environment;
* suite/test count where available;
* skipped count;
* result;
* artifact/file;
* limitations.

Never fabricate evidence.

Local evidence proves only what was actually executed locally.

Do not claim:

* remote CI;
* production acceptance;
* staging validation;
* external device validation;
* legal approval;
* security certification;
* store acceptance;
* real-user acceptance;

unless they were actually performed.

==================================================
33. CHECKPOINTS
==================================================

Use major checkpoints appropriate to the project.

Example:

CHECKPOINT A
Architecture and context understood.

CHECKPOINT B
Foundational state/schema/contracts stable.

CHECKPOINT C
Core domain/runtime behavior implemented.

CHECKPOINT D
Client/platform/integration slices implemented.

CHECKPOINT E
Security/concurrency/recovery hardened.

CHECKPOINT F
Full feature integrated.

Not every project requires every example checkpoint.

Adapt them.

At each checkpoint:

* reconcile Spec/Plan/Tasks;
* inspect remaining dependency graph;
* reevaluate agent topology;
* reevaluate safe parallelism;
* update evidence;
* run appropriate test gates;
* confirm no hidden blocker.

==================================================
34. LOCAL CLEAN-ROOM GATE
==================================================

Before declaring the feature locally complete:

create/use an isolated clean worktree or equivalent reproducible local environment where practical.

Verify applicable items discovered earlier.

Potential checks include:

* clean dependency install;
* dependency restore;
* formatting;
* lint;
* type check;
* build;
* code generation;
* generated drift;
* migration apply;
* migration rollback/reapply;
* unit tests;
* contract tests;
* integration tests;
* persistence/database tests;
* race tests;
* security tests;
* E2E tests;
* UI/component/widget tests;
* platform analysis;
* native platform tests;
* performance tests;
* config validation;
* `git diff --check`;
* critical skipped tests = 0.

Only run checks relevant to the actual project.

Do NOT invent missing technologies.

Record:

`LOCAL_CLEAN_GATE = PASS`

only if every locally required applicable check passes.

Otherwise:

`LOCAL_CLEAN_GATE = FAIL`

and state exactly why.

==================================================
35. FINAL PARALLEL SPECIALIST REVIEW
==================================================

After implementation appears complete:

do NOT rely on a single reviewer for a substantial feature.

Use the maximum SAFE and USEFUL number of independent fresh reviewers supported by:

* feature complexity;
* independent review domains;
* environment capabilities.

Approximately 4–6 reviewers is often useful for a substantial cross-cutting feature.

Use fewer when the feature has fewer meaningful risk domains.

Use more when:

* the feature genuinely spans more independent risk areas;
* the environment supports the concurrency;
* reviewers can work independently;
* additional review has useful coverage rather than duplication.

Select reviewer domains dynamically.

Candidate domains:

R1 — Product / Domain / State Machine

R2 — Persistence / Transactions / Concurrency

R3 — Security / Privacy / Authorization

R4 — Contracts / Integrations / Generated Code

R5 — Client / UX / Accessibility / Platform Lifecycle

R6 — Tests / Evidence / Performance / Maintainability

Additional reviewer domains may include:

* mobile/native platform behavior;
* desktop/runtime behavior;
* distributed systems;
* offline/synchronization;
* embedded/hardware;
* data/ML reproducibility;
* networking/protocols;
* infrastructure/IaC;
* backward compatibility;
* public API/library compatibility.

Replace irrelevant reviewers.

Examples:

No UI:
replace UI review with another relevant specialist.

No database:
replace persistence/transaction review with:

* filesystem;
* cache;
* distributed state;
* firmware;
* local persistence;
* networking;
* architecture;

as appropriate.

Mobile-only:
reviewers might cover:

* state/domain;
* UI/accessibility;
* persistence/offline;
* networking;
* platform lifecycle;
* tests/performance/security.

Backend-only:
reviewers might cover:

* domain;
* data/concurrency;
* API/contracts;
* authorization;
* workers/cache;
* tests/performance.

Embedded system:
use firmware/hardware/concurrency reviewer.

Data/ML project:
use data-pipeline/model-reproducibility reviewer.

Infrastructure project:
use deployment/IaC/security reviewer.

Each reviewer receives:

* authoritative Spec;
* Plan;
* Tasks;
* applicable project instructions;
* actual full feature diff;
* relevant implementation;
* tests/evidence.

Do NOT give reviewers implementer conclusions as truth.

Each reviewer should return structured findings:

ID  
Severity  
Root cause  
Evidence  
Affected paths  
Required fix  
Regression required

Deduplicate by root cause.

Assign fixes by ownership.

After fixes:

rerun affected tests.

Re-review only affected risk areas.

Do not rerun every reviewer because of one isolated cosmetic correction.

==================================================
36. FINAL ADVERSARIAL INTEGRATION REVIEW
==================================================

After specialist reviews are clean, use ONE fresh final integration reviewer.

The goal is NOT another line-by-line review.

Look specifically for interaction bugs:

* individually correct modules that conflict;
* cross-feature state mismatches;
* incompatible lifecycle assumptions;
* stale version domains;
* snapshot inconsistencies;
* contract/runtime divergence;
* client/server eligibility mismatch;
* local/remote state mismatch;
* retry/restart interactions;
* pagination against mutable data;
* cache invalidation problems;
* immutable identity reuse;
* old history blocking new operations;
* partial transaction behavior;
* rollback/audit inconsistencies;
* authorization differences between layers;
* offline/server conflicts;
* generated consumer/runtime mismatch;
* platform lifecycle interacting badly with domain state.

Mandatory question:

"What mutable inputs can change this result, state, projection, eligibility, or decision, and is every relevant mutable dependency represented by the version/snapshot/transaction/cache/state identity protecting it?"

Exit only with:

* 0 blocker;
* 0 critical;
* 0 high;
* 0 unresolved closure-blocking MEDIUM.

==================================================
37. TASK COMPLETENESS AUDIT
==================================================

Before completion, reconcile every task from `tasks.md`.

Every task must be classified exactly as:

* COMPLETED_AND_VERIFIED;
* COMPLETED_BUT_EXTERNAL_VERIFICATION_REQUIRED;
* INTENTIONALLY_OPEN;
* BLOCKED_BY_PRODUCT_DECISION;
* NOT_APPLICABLE_WITH_JUSTIFICATION.

No task may silently disappear.

Do not mark a task complete merely because adjacent functionality exists.

Verify the exact acceptance claim.

==================================================
38. SPEC / PLAN / IMPLEMENTATION PARITY
==================================================

Perform a final three-way comparison:

SPEC
↔ PLAN
↔ IMPLEMENTATION

Look for:

* Spec requirement not implemented;
* planned behavior not required by Spec;
* implementation behavior absent from Spec;
* task marked complete without evidence;
* forgotten error state;
* inconsistent terminology;
* state transition mismatch;
* undocumented constraint;
* accidental scope expansion.

The Spec remains final product truth unless an explicitly authoritative newer project decision exists.

Never silently invent product behavior.

==================================================
39. LOCAL COMMITS
==================================================

Commit locally in logical reviewed units.

Possible grouping:

* schema/contracts;
* core domain;
* integrations;
* client/UI;
* platform/native integration;
* tests/hardening;
* review fixes;
* evidence/docs.

Adapt grouping to the actual feature.

A project with no schema should not create a schema commit.

A mobile-only project may naturally use commits such as:

* domain/state;
* UI/navigation;
* offline/networking;
* native integration;
* tests/hardening.

Avoid one gigantic unreadable commit where practical.

Before every commit:

* inspect diff;
* ensure unrelated user changes are not included;
* run appropriate narrow verification.

Do not push.

Do not merge to main/default.

==================================================
40. FINAL LOCAL REPORT
==================================================

At completion produce ONE final report containing:

STATUS

* overall implementation status;
* target Spec;
* repository;
* branch;
* initial HEAD;
* final local HEAD.

CAPABILITY DISCOVERY

* parallel-agent capability;
* effective concurrency used;
* important unavailable capabilities;
* how workflow adapted.

TECHNOLOGY DISCOVERY

* languages;
* frameworks;
* architecture;
* platforms;
* persistence;
* contracts;
* generated code;
* test frameworks;
* package/build tooling.

AGENT EXECUTION

* work units;
* dependency waves;
* agent roles used;
* maximum useful concurrency reached;
* areas intentionally serialized and why.

TASKS

* completed;
* verified;
* intentionally open;
* externally gated;
* blocked items.

IMPLEMENTATION

* production files changed;
* migrations/schema changes;
* contracts changed;
* generated artifacts changed;
* UI/client changes;
* platform/native changes;
* integration changes.

COMMITS

* local commit SHAs;
* short purpose of each.

TESTS

* commands executed;
* suite counts;
* test counts;
* skipped counts;
* failures;
* pre-existing failures;
* final result.

REVIEWS

* reviewer roles used;
* important findings;
* root causes;
* fixes;
* regressions added.

SECURITY

* authorization findings;
* privacy findings;
* secrets/logging findings;
* unresolved risks.

CONCURRENCY / RECOVERY

* races reviewed;
* idempotency/retry behavior;
* restart/lost-response behavior;
* lifecycle recovery where applicable;
* unresolved risks.

PERFORMANCE

* checks performed;
* measurements where available;
* limitations.

CROSS-FEATURE REGRESSION

* neighboring features/modules checked;
* relevant regression results.

EVIDENCE

* acceptance matrix location;
* evidence limitations.

FINAL GATE

`LOCAL_CLEAN_GATE = PASS|FAIL`

REMOTE STATUS

`REMOTE_CI_STATUS = NOT_CHECKED_BY_DESIGN`

EXTERNAL GATES

Clearly list anything local execution cannot prove.

HANDOFF

Give exact local commands useful for the next stage, such as:

* inspecting commits;
* reviewing diff;
* pushing later;
* opening a PR later;
* running optional external tests later.

Do not execute remote operations.

==================================================
41. NON-NEGOTIABLE RULES
==================================================

* No push unless explicitly requested.
* No merge to main/default.
* No hidden failing tests.
* No hiding pre-existing failures.
* No critical skipped tests.
* No weakening tests to obtain green.
* No fabricated evidence.
* No silent product decisions.
* No hand-editing generated code unless repository policy explicitly allows it.
* No trusting durable external data solely through static casts.
* No UI-only authorization when backend/domain enforcement is required.
* No fake concurrency claims.
* No claiming tests that did not run.
* No claiming remote CI was checked.
* No destructive unrelated cleanup.
* No overwriting unrelated user changes.
* No unnecessary architecture rewrites.
* No full-suite rerun after every trivial edit.
* No forced reviewer findings.
* No infinite review loops for cosmetic issues.
* No mapping agents mechanically to application layers.
* No artificial task fragmentation just to create more parallel agents.
* No unused safe parallelism without a concrete reason.
* Use real project architecture.
* Use real project commands.
* Use real project conventions.
* Derive agents from independent work units.
* Use maximum safe and useful parallelism.
* Preserve file ownership.
* Review based on risk.
* Fix root causes, not symptoms.
* Test the tests for critical claims.
* Keep the Spec, Plan, Tasks, implementation, and evidence synchronized.

==================================================
42. AUTONOMY RULE
==================================================

Start immediately.

Do not ask the user to provide individual tickets.

Use `tasks.md` as the execution queue.

Do not repeatedly request intermediate approval.

Continue autonomously through everything that can safely be determined from:

* Spec;
* Plan;
* Tasks;
* repository architecture;
* existing production behavior;
* tests;
* project conventions.

Ask the user only when there is a TRUE unresolved PRODUCT DECISION where:

1. the Spec does not answer it;
2. the Plan does not answer it;
3. Tasks do not answer it;
4. repository conventions do not answer it;
5. existing behavior does not establish the intended rule;
6. choosing arbitrarily would change product behavior.

Technical implementation decisions should normally be resolved by engineering reasoning rather than user interruption.

Agent allocation is a technical execution decision.

Do NOT ask the user:

* how many agents to use;
* which agent should implement which layer;
* whether UI/backend/database agents should exist;

unless the execution environment itself requires explicit user action.

Determine these dynamically from:

* available capability;
* dependency graph;
* risk;
* ownership;
* workload.

==================================================
43. ADAPTIVE EXECUTION PRINCIPLE
==================================================

This workflow must fit the project.

The project must NOT be forced to fit this workflow.

For every section ask:

"Is this applicable to the actual repository, target Spec, technology, and risk?"

If YES:

apply it deeply.

If NO:

skip it explicitly or treat it as not applicable.

Do not create artificial requirements.

Examples:

Small library:

may need only:

* API implementation;
* compatibility;
* tests;
* review.

Large single-platform application:

may legitimately require more than six concurrent agents if the work units are independent and the environment supports it.

The architecture determines the workflow topology.

The agent count does not determine the architecture.

==================================================
44. SUCCESS CONDITION
==================================================

The goal is not:

"write code until tests pass."

The goal is:

UNDERSTAND
→ DISCOVER CAPABILITIES
→ DISCOVER TECHNOLOGY
→ MAP WORK UNITS
→ BUILD DEPENDENCY DAG
→ ALLOCATE SAFE PARALLELISM
→ IMPLEMENT
→ TEST
→ INDEPENDENTLY REVIEW
→ FIX ROOT CAUSES
→ RE-TEST
→ INTEGRATE
→ ADVERSARIALLY REVIEW
→ VERIFY IN CLEAN LOCAL ENVIRONMENT
→ COMMIT LOCALLY
→ REPORT EVIDENCE

Complete the target Spec locally to the strongest level that the actual repository and available environment can prove.

Use the maximum safe and useful execution capability available.

Do not waste concurrency.

Do not manufacture concurrency.

Then stop before remote repository operations.