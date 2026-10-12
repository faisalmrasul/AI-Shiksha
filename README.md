# 🌍 AI Shiksha - Universal Core + Local Overlay Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-shiksha.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![EU AI Act Aligned](https://img.shields.io/badge/EU%20AI%20Act-Aligned%20(Prototype)-informational)](https://artificialintelligenceact.eu/)

**AI Shiksha** is a revolutionary, AI-powered educational platform built for global scalability with country-specific curriculum overlays. It serves four distinct user segments with specialized intelligence engines:

- 🎓 **Students** — Adaptive learning with spaced repetition, Socratic AI, and visual mastery tracking
- 👨‍🏫 **Teachers** — Lesson planning, assessment generation, and time-saving analytics
- 💼 **Professionals** — Research, portfolio analysis, and citation management
- 🏢 **SME Business Owners** — Growth automation, predictive analytics, and action-oriented task feeds

> **🧪 Prototype Notice**
> AI Shiksha is a **prototype**. Its governance architecture is **aligned with EU AI Act (Regulation 2024/1689) principles** as a design standard. It is not currently placed on the EU market and makes **no legal compliance claim**. The EU AI Act is used here as a design bar for a worldwide platform.

---

## 🚀 Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-shiksha.streamlit.app)

---

## ✨ Key Features

### 🎓 Student Intelligence Engine
- **Spaced Repetition Engine** — Memory-retention algorithms (SM-2 based) that trigger review prompts right before concept decay
- **Prerequisite Knowledge Graphs** — Visual node-based maps showing subject dependencies (e.g., Factoring → Quadratic Equations)
- **Multimodal OCR Processing** — Upload images of handwritten math, diagrams, or textbook pages
- **Socratic AI Guardrails** — Hints, analogies, and step-by-step guidance without giving direct answers
- **Dynamic Difficulty Balancer** — Breaks down sub-steps after wrong attempts, escalates challenges after win streaks
- **Voice-First Active Recall (Content-Only)** — Simulated speech-to-text that evaluates **answer content only** — never emotional state, attention, or affect
- **Visual Mastery Trees** — Interactive node-map interfaces tracking concept status (locked / in-progress / mastered)
- **Opt-In Habit Tracking** — Non-manipulative, informational streak tracking — no loss aversion, no shaming, no rewards tied to streaks
- **Instant Step Evaluation** — Line-by-line feedback on submitted work
- **Latent Knowledge Gap Tracking** — Measures solution speed, attempts, and confidence to surface hidden weaknesses
- **Zero Data Retention** — Student data is session-only and never used for AI training
- **Contextual Content Shields** — Blocks non-academic, cheating, or inappropriate prompts

### 👨‍🏫 Teacher Intelligence Engine
- **Multi-Asset Lesson Bundle Generator** — One-click generation of lesson plans, slide outlines, worksheets, and answer keys
- **Modular Block Editor** — Edit, swap, or regenerate individual lesson sections
- **One-Tap Accommodation Toggles** — IEP/504 modifications, sentence starters, ELL translations
- **Dynamic Lexile Adjuster** — Rewrite text at different reading levels (beginner to expert)
- **Rubric Generator** — Create tiered grading rubrics with customizable criteria and weightings
- **Quiz Generator** — Auto-generate quizzes with multiple question types
- **Batch Feedback Assistant** — Generate feedback drafts for multiple students with **mandatory human approval** before delivery
- **Time-Saved Dashboard** — Analytics tracking hours recovered on lesson planning, grading, and admin work
- **LMS Integration** — Connect to Google Classroom, Canvas, Schoology, and Microsoft Teams
- **Curriculum Standards Mapping** — Auto-tag content to Common Core, NGSS, TEKS, CBC, and NCTB standards
- **Parent & Sub-Plan Generators** — One-click drafting of parent updates and substitute teacher guides
- **PII Redaction Layer** — Client-side redaction of names and email addresses, with data-minimisation principles

### 💼 Professional Intelligence Engine
- **Hybrid Search Engine** — Vector + keyword (BM25) retrieval across documents
- **Audit-Linked Citation Engine** — Verify claims against source documents with page-level citations
- **Data Sandbox (Security-First)** — Code execution is disabled in the prototype for security reasons; production will use an isolated subprocess sandbox
- **Portfolio Intelligence** — Real-time portfolio tracking with sector exposure analysis
- **Macro Stress-Testing** — Simulate macroeconomic shocks against portfolios
- **24/7 Asset Watchdogs** — Automated agents scanning earnings, regulatory filings, and market news
- **One-Click Deliverable Generator** — Turn research notes into professional investment memos, client tear sheets, and research notes
- **Split-Screen Workspace** — Dual-pane interface with working notes and source documents
- **Automated Table Extraction** — Extract tables from PDFs into Excel-ready format

### 🏢 SME Growth Automation Engine
- **Predictive Analytics** — Cash flow forecasting, customer churn prediction, inventory depletion forecasts
- **Deterministic Forecasts** — Seeded RNG ensures the same forecast within a day — auditable and reproducible
- **Action-Oriented Task Feed** — Priority-ranked recommendations based on real-time business data
- **AI Business Assistant** — Natural language queries about business data (RAG)
- **Automation Solutions** — Industry-specific automation plans (retail, service, agriculture, manufacturing, tech)
- **API Connector Layer** — Connect to Stripe, QuickBooks, Shopify, Toast POS, and Jobber
- **Webhook Architecture** — Event-driven infrastructure for real-time AI actions
- **Proactive Push Delivery** — Automated digests and alerts via WhatsApp, SMS, and Email
- **Payment Integration** — Support for M-Pesa, bKash, PayPal, Stripe, and regional payment rails

---

## 🛡️ AI Ethics & Governance

AI Shiksha uses the **EU AI Act (Regulation 2024/1689)** as a **design standard** — not as a legal status. This reflects a commitment to responsible AI at the prototype stage and prepares the platform for future regulatory alignment in any jurisdiction.

For the full statement, see [AI_ETHICS.md](./AI_ETHICS.md).

### Registered AI Systems

Every AI system in the platform is registered with a declared risk tier and purpose. The **🛡️ AI Ethics** page in the app displays this registry transparently.

| AI System | Risk Tier | Human Oversight | Transparency |
|-----------|-----------|-----------------|--------------|
| Student Mastery & Gap Analysis | High | ✅ Required | ✅ Disclosed |
| Batch Feedback Assistant | High | ✅ Required | ✅ Disclosed |
| Lesson Bundle Generator | Limited | ✅ Required | ✅ Disclosed |
| Socratic Guidance | Limited | — | ✅ Disclosed |
| SME Predictive Analytics | Limited | ✅ Required | ✅ Disclosed |
| Professional Research Engine | Limited | ✅ Required | ✅ Disclosed |

### Design Principles

- ✅ **Transparency** — Every AI-generated output carries an explicit AI disclosure
- ✅ **Human Oversight** — High-risk outputs require a named human approver before reaching end users
- ✅ **Event Logging** — High-risk AI decisions are logged to `compliance/events.jsonl` for auditability
- ✅ **Deterministic Outputs** — Forecasts use seeded RNG for reproducibility
- ✅ **Content-Only Assessments** — Voice input evaluates content, never emotion or affect
- ✅ **Non-Manipulative Design** — No loss aversion, no guilt framing, no rewards tied to streaks
- ✅ **Zero Retention for Students** — Student data is session-only and never used for training

### What AI Shiksha Does Not Do

- ❌ Infer emotional state from voice, text, or behaviour
- ❌ Track attention or engagement via biometrics
- ❌ Make final grading decisions without a human approver
- ❌ Manipulate users via streaks, notifications, or loss aversion
- ❌ Share student data with model training pipelines

---

## 🏗️ Architecture

### Universal Core

The platform is built on a **Universal Core** that provides foundational subjects and competencies portable across all educational systems:

- Mathematics, English Language, Basic Science, Geography, General Knowledge, Applied AI, **AI Ethics**
- Critical Thinking, Communication, Collaboration, Creativity, Digital Literacy, Ethical Reasoning

### Local Curriculum Overlay

Country-specific overlays adapt the Universal Core to local educational systems, including country-specific AI ethics framing:

- **Kenya** — CBC (Competency Based Curriculum) with KNEC/KICD boards — Ubuntu ethics, community consent
- **Bangladesh** — National Curriculum (NCTB) with multiple examination boards — Digital Bangladesh 2041 goals
- **USA** — Common Core State Standards with NGSS — NIST AI RMF, FERPA student privacy
- **UK** — National Curriculum for England with GCSE and A-Levels — ICO AI guidance, Online Safety Act

### Intelligence Engines

| Engine | Purpose | Key Technology |
|--------|---------|----------------|
| Student Outcome Engine | Adaptive learning & progress tracking | Spaced repetition, Knowledge graphs, Socratic AI |
| Teacher Intelligence Engine | Lesson planning & time savings | Bundle generation, LMS integration, Standards mapping |
| Professional Intelligence Engine | Research & portfolio management | Hybrid search, Citation tracking, Portfolio analytics |
| SME Growth Automation Engine | Business automation & analytics | Predictive AI, Webhooks, API connectors |

### Governance Layer

A cross-cutting governance layer applies to all engines:

| Component | Purpose |
|-----------|---------|
| `AIRiskTier` + `AI_SYSTEM_REGISTRY` | Declares risk tier and purpose for each AI system |
| `TransparencyLayer` | Attaches AI disclosure to every AI-generated output |
| `HumanOversightGate` | Requires named approver for high-risk outputs |
| `AIEventLogger` | Writes JSONL audit trail for high-risk decisions |

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| Framework | Streamlit |
| Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Visualization | NetworkX, Matplotlib (optional) |
| Document Processing | PyPDF2, python-docx |
| Data Models | Dataclasses, Enums |
| Analytics | Custom AI/ML algorithms |
| Governance | Custom EU AI Act-aligned layer |

---

## 📦 Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/ai-shiksha.git
cd ai-shiksha
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
streamlit run app.py
```

### Optional: Enable Visual Knowledge Graphs

```bash
pip install networkx matplotlib
```

---

## 📁 Project Structure

```
ai-shiksha/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── AI_ETHICS.md                # AI ethics and governance statement
├── LICENSE                     # MIT license
├── compliance/
│   ├── ai_governance.py        # Governance layer (risk registry, transparency, oversight, logging)
│   └── events.jsonl            # Generated audit trail (created at runtime)
└── .streamlit/
    └── config.toml             # Streamlit configuration
```

---

## 🗺️ Roadmap

### Prototype (current)

- [x] Four segment-specific intelligence engines
- [x] Universal Core + Local Overlay (Kenya, Bangladesh, USA, UK)
- [x] EU AI Act-aligned governance layer
- [x] AI Ethics page per role
- [x] Deterministic forecasts
- [x] Opt-in non-manipulative streak tracking
- [x] Content-only voice assessment

### Production (planned)

- [ ] Deployer agreements for schools and teachers
- [ ] LLM vendor addendum (Art. 25 cooperation)
- [ ] Annex IV-style technical dossier per high-risk engine
- [ ] Post-market monitoring plan
- [ ] Subprocess sandbox for quantitative code execution
- [ ] Real LMS integrations (currently stubbed)
- [ ] Real payment rails (currently stubbed)
- [ ] Multi-language UI
- [ ] Mobile-responsive design

### Future (if entering EU market)

- [ ] EU authorised representative
- [ ] Conformity assessment (internal or third-party)
- [ ] EU Declaration of Conformity
- [ ] CE marking
- [ ] EU AI database registration

---

## 🤝 Contributing

Contributions are welcome. For AI-related contributions, please ensure:

1. New AI systems are registered in `AI_SYSTEM_REGISTRY` with a declared risk tier.
2. AI-generated outputs are wrapped with `TransparencyLayer.attach()`.
3. High-risk outputs route through `HumanOversightGate.check()`.
4. Deterministic seeds are used for any randomised outputs.

---

## 📄 License

MIT License — see the [LICENSE](./LICENSE) file for details.

---

## 🙏 Acknowledgements

- The EU AI Act (Regulation 2024/1689) — used as a design standard
- The Streamlit team for an excellent rapid-prototyping framework
- The open-source community for Pandas, NumPy, NetworkX, and Matplotlib

---

**Built with ❤️ for learners everywhere.**
**Prototype — aligned with EU AI Act principles as a design standard, not a legal status.**
