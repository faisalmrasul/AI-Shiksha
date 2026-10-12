# AI Ethics & Governance Statement

**AI Shiksha** — Universal Core + Local Overlay Platform
**Status:** Prototype
**Last updated:** 2025

---

## 1. Purpose of This Document

This document explains how AI is used inside AI Shiksha, what design principles guide its behavior, and what the platform explicitly does **not** do. It is written for users (students, teachers, parents, professionals, SME owners), reviewers, and future collaborators.

AI Shiksha is a **prototype**. It uses the **EU AI Act (Regulation 2024/1689)** as a **design standard**, not as a legal status. AI Shiksha is not currently placed on the EU market and makes **no legal compliance claim**. The Act is used here because it is the world's most comprehensive AI governance framework, and building to its principles today prepares the platform for future regulatory alignment in any jurisdiction.

---

## 2. Why We Use the EU AI Act as a Design Standard

The EU AI Act classifies AI systems into four risk tiers:

| Tier | Meaning | Examples |
|------|---------|----------|
| **Prohibited** | Banned outright | Emotion recognition in education; subliminal manipulation |
| **High-risk** | Full compliance required | Evaluating learning outcomes; access to education |
| **Limited-risk** | Transparency duties | Chatbots; AI-generated content |
| **Minimal-risk** | No specific obligations | Productivity tools |

AI Shiksha operates primarily in the **High-risk** and **Limited-risk** tiers — because education is explicitly listed in Annex III of the Act. That means the platform's design must answer to real questions about fairness, oversight, transparency, and data protection.

We treat these as **design requirements**, not paperwork.

---

## 3. Registered AI Systems

Every AI system in AI Shiksha is declared with a risk tier, purpose, and oversight requirement. The registry is displayed inside the app on the **🛡️ AI Ethics** page.

| AI System | Risk Tier | Human Oversight | Transparency |
|-----------|-----------|-----------------|--------------|
| Student Mastery & Gap Analysis | High | ✅ Required | ✅ Disclosed |
| Batch Feedback Assistant | High | ✅ Required | ✅ Disclosed |
| Lesson Bundle Generator | Limited | ✅ Required | ✅ Disclosed |
| Socratic Guidance | Limited | — | ✅ Disclosed |
| SME Predictive Analytics | Limited | ✅ Required | ✅ Disclosed |
| Professional Research Engine | Limited | ✅ Required | ✅ Disclosed |

Each entry maps to a `AISystemRegistration` object in the codebase. Adding a new AI system requires registering it — there is no way to ship a new AI feature without declaring its tier and oversight requirement.

---

## 4. Design Principles

These principles apply across every engine, every segment, and every country overlay.

### 4.1 Transparency

Every AI-generated output carries an explicit disclosure. Users are told:

- That AI was involved
- Which registered system produced the output
- Its risk tier
- Whether human oversight is required
- That the platform is a prototype

The disclosure is attached at the moment of generation and travels with the output.

### 4.2 Human Oversight

High-risk outputs — such as student feedback drafts and mastery determinations — require a **named human approver** before they reach end users. This is enforced in code via a `HumanOversightGate` check. It is not optional, and it cannot be bypassed silently.

What this means in practice:

- AI **drafts** feedback; a teacher **approves** it
- AI **suggests** mastery; a human **confirms** it
- AI **recommends** actions; a human **decides**

### 4.3 Event Logging

High-risk AI decisions are logged to `compliance/events.jsonl` with:

- System ID and timestamp
- Segment (Student, Teacher, etc.)
- A hash of the input (not the raw input, for privacy)
- A short summary of the output
- The named approver, if any

Logs are append-only and used for auditability. They are not used for model training.

### 4.4 Deterministic Outputs

Forecasts (cash flow, churn, inventory, market data) use seeded pseudo-random number generators tied to the current date. This means:

- The same forecast is produced consistently within a single day
- Users see stable, reproducible results
- Auditors can reconstruct what the system showed on any given day

### 4.5 Content-Only Assessments

Voice input in AI Shiksha evaluates the **content** of spoken answers only. It does **not** infer:

- Emotional state
- Attention or focus
- Stress or affect
- Behavioural profile

This is a deliberate design choice aligned with the EU AI Act's prohibition on emotion recognition in educational settings.

### 4.6 Non-Manipulative Design

Habit and streak tracking is:

- **Opt-in** — disabled by default
- **Informational** — no rewards, no penalties, no loss framing
- **Non-shaming** — missing a day does not trigger guilt-inducing language
- **Capped** — no more than one notification per day

The platform does not use dark patterns, addictive loops, or loss-aversion triggers.

### 4.7 Zero Retention for Students

Student data in AI Shiksha is session-only. It is:

- Never persisted to a database
- Never used for model training
- Never shared with third-party model vendors
- Redacted of names and emails before any processing that could leak PII

### 4.8 Security by Default

Features that introduce security risk are disabled in the prototype:

- Arbitrary code execution in the professional data sandbox is turned off
- Users see an explicit note that this is a security choice, not a missing feature
- Production will use an isolated subprocess sandbox

---

## 5. What AI Shiksha Does Not Do

To be explicit about boundaries:

- ❌ **Does not infer emotional state** from voice, text, or behaviour
- ❌ **Does not track attention or engagement** via biometrics
- ❌ **Does not make final grading decisions** without a human approver
- ❌ **Does not manipulate users** via streaks, notifications, or loss aversion
- ❌ **Does not share student data** with model training pipelines
- ❌ **Does not produce probabilistic outputs** that cannot be explained
- ❌ **Does not use predictive analytics** on minors for high-stakes decisions

If any of these ever change, this document will be updated first — and the change will be visible to users.

---

## 6. Country-Specific Framing

AI ethics is culturally situated. AI Shiksha adapts its ethics framing to each country overlay:

| Country | Framing |
|---------|---------|
| 🇰🇪 Kenya | Ubuntu ethics, community consent, Harambee data-sharing norms |
| 🇧🇩 Bangladesh | Digital Bangladesh 2041 goals, language equity in AI, worker data rights |
| 🇺🇸 USA | NIST AI RMF, civil rights frameworks, FERPA student privacy |
| 🇬🇧 UK | ICO AI guidance, Online Safety Act, Ofcom duties |

This is intentional. A globally portable platform should not impose one country's ethics on another. It should build common principles and let each context layer its own.

---

## 7. Data Handling Summary

| Data Type | Storage | Retention | Used for Training |
|-----------|---------|-----------|-------------------|
| Student learning data | Session only | Session duration | No |
| Teacher lesson plans | Session only | Session duration | No |
| Uploaded documents | In-memory | Session duration | No |
| AI event logs | Local file (`compliance/events.jsonl`) | Prototype duration | No |
| PII (names, emails) | Redacted before processing | Not stored | No |

In production, this table will be updated to reflect actual infrastructure choices. Any change will be published here before it takes effect.

---

## 8. Governance in Code

The governance layer is implemented in code and not just documented here:

| Component | Purpose |
|-----------|---------|
| `AIRiskTier` | Enum classifying every AI system |
| `AI_SYSTEM_REGISTRY` | Dict of all registered AI systems |
| `AISystemRegistration` | Dataclass for system metadata |
| `TransparencyLayer` | Attaches AI disclosure to every output |
| `HumanOversightGate` | Blocks high-risk outputs without named approver |
| `AIEventLogger` | Writes JSONL audit trail |

These are not optional. They are part of the platform's core, and removing them would break the app's governance contract.

---

## 9. What's Not Yet Done (Prototype Boundaries)

Being honest about limitations is part of ethical design. The following are **not** yet in place:

- ❌ No formal Annex IV technical dossier (planned for production)
- ❌ No third-party conformity assessment (planned if entering EU market)
- ❌ No EU authorised representative (not needed until EU market entry)
- ❌ No formal incident reporting workflow (planned for production)
- ❌ No bias audit pipeline (planned for production)
- ❌ No signed deployer agreements (planned for production)

These are production-phase requirements. In the prototype, the goal is **design discipline** — logging, oversight, transparency, and risk declaration — not legal paperwork.

---

## 10. Reporting Concerns

If you encounter behavior in AI Shiksha that seems inconsistent with this statement, please report it.

- **Students / Parents** — Contact your school administrator or the platform maintainer
- **Teachers** — Contact the platform maintainer via the repository
- **Professionals / SME Owners** — Contact the platform maintainer via the repository
- **Security / Ethics Researchers** — Open an issue in the GitHub repository

Every report is logged. Reports that indicate a design flaw are reviewed and, where warranted, result in a code change with a note in this document.

---

## 11. A Final Note

AI Shiksha is a prototype built in a spirit of honest engineering. The intent is not to claim compliance we haven't earned, nor to hide behind disclaimer language.

The intent is this:

> Build AI that a parent would trust with their child's learning. Build AI that a teacher would trust with their classroom. Build AI that a regulator would respect for its transparency. Do this from the first line of code, not as an afterthought.

If we ever drift from that, this document should be the first thing to change.

---

**AI Shiksha — aligned with EU AI Act principles as a design standard, not a legal status.**
