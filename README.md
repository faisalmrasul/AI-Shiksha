# 🌍 AI Shiksha - Universal Core + Local Overlay Platform

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-shiksha.streamlit.app)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**AI Shiksha** is a revolutionary, AI-powered educational platform built for global scalability with country-specific curriculum overlays. It serves four distinct user segments with specialized intelligence engines:

- 🎓 **Students** - Adaptive learning with spaced repetition, Socratic AI, and visual mastery tracking
- 👨‍🏫 **Teachers** - Lesson planning, assessment generation, and time-saving analytics
- 💼 **Professionals** - Research, portfolio analysis, and citation management
- 🏢 **SME Business Owners** - Growth automation, predictive analytics, and action-oriented task feeds

## 🚀 Live Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ai-shiksha.streamlit.app)

## ✨ Key Features

### 🎓 Student Intelligence Engine
- **Spaced Repetition Engine**: Memory-retention algorithms (SM-2 based) that trigger review prompts right before concept decay
- **Prerequisite Knowledge Graphs**: Visual node-based maps showing subject dependencies (e.g., Factoring → Quadratic Equations)
- **Multimodal OCR Processing**: Upload images of handwritten math, diagrams, or textbook pages
- **Socratic AI Guardrails**: System prompts that prevent direct answers, providing hints, analogies, and step-by-step guidance
- **Dynamic Difficulty Balancer**: Breaks down sub-steps after wrong attempts, escalates challenges after win streaks
- **Voice-First Active Recall**: Simulated speech-to-text pipeline for verbal comprehension evaluation
- **Visual Mastery Trees**: Interactive node-map interfaces tracking concept status (locked, in-progress, mastered)
- **Habit & Streak Mechanics**: Daily streak tracking with repair buffer (1-day forgiveness)
- **Instant Step Evaluation**: Line-by-line feedback on submitted work
- **Latent Knowledge Gap Tracking**: Measures solution speed, attempts, and confidence to surface hidden weaknesses
- **COPPA/FERPA Data Isolation**: Zero data retention - student data never saved or used for AI training
- **Contextual Content Shields**: Blocks non-academic, cheating, or inappropriate prompts

### 👨‍🏫 Teacher Intelligence Engine
- **Multi-Asset Lesson Bundle Generator**: One-click generation of lesson plans, slide outlines, worksheets, and answer keys
- **Modular Block Editor**: Edit, swap, or regenerate individual lesson sections
- **One-Tap Accommodation Toggles**: IEP/504 modifications, sentence starters, ELL translations
- **Dynamic Lexile Adjuster**: Rewrite text at different reading levels (beginner to expert)
- **Rubric Generator**: Create tiered grading rubrics with customizable criteria and weightings
- **Quiz Generator**: Auto-generate quizzes with multiple question types
- **Batch Feedback Assistant**: Generate feedback for multiple students with approval workflow
- **Time-Saved Dashboard**: Analytics tracking hours recovered on lesson planning, grading, and admin work
- **LMS Integration**: Connect to Google Classroom, Canvas, Schoology, and Microsoft Teams
- **Curriculum Standards Mapping**: Auto-tag content to Common Core, NGSS, TEKS, CBC, and NCTB standards
- **Parent & Sub-Plan Generators**: One-click drafting of parent updates and substitute teacher guides
- **Zero-PII Compliance Layer**: Client-side redaction of student names and data isolation

### 💼 Professional Intelligence Engine
- **Hybrid Search Engine**: Vector + keyword (BM25) retrieval across documents
- **Audit-Linked Citation Engine**: Verify claims against source documents with page-level citations
- **Code-Executing Data Sandbox**: Run quantitative analysis in a sandboxed Python environment
- **Portfolio Intelligence**: Real-time portfolio tracking with sector exposure analysis
- **Macro Stress-Testing**: Simulate macroeconomic shocks against portfolios
- **24/7 Asset Watchdogs**: Automated agents scanning earnings, regulatory filings, and market news
- **One-Click Deliverable Generator**: Turn research notes into professional investment memos, client tear sheets, and research notes
- **Split-Screen Workspace**: Dual-pane interface with working notes and source documents
- **Automated Table Extraction**: Extract tables from PDFs into Excel-ready format

### 🏢 SME Growth Automation Engine
- **Predictive Analytics**: Cash flow forecasting, customer churn prediction, inventory depletion forecasts
- **Action-Oriented Task Feed**: Priority-ranked recommendations based on real-time business data
- **AI Business Assistant**: Natural language queries about business data (RAG)
- **Automation Solutions**: Industry-specific automation plans (retail, service, agriculture, manufacturing, tech)
- **API Connector Layer**: Connect to Stripe, QuickBooks, Shopify, Toast POS, and Jobber
- **Webhook Architecture**: Event-driven infrastructure for real-time AI actions
- **Proactive Push Delivery**: Automated digests and alerts via WhatsApp, SMS, and Email
- **Payment Integration**: Support for M-Pesa, bKash, PayPal, Stripe, and regional payment rails

## 🏗️ Architecture

### Universal Core
The platform is built on a **Universal Core** that provides foundational subjects and competencies portable across all educational systems:

- Mathematics, English Language, Basic Science, Geography, General Knowledge, Applied AI
- Critical Thinking, Communication, Collaboration, Creativity, Digital Literacy

### Local Curriculum Overlay
Country-specific overlays adapt the Universal Core to local educational systems:

- **Kenya**: CBC (Competency Based Curriculum) with KNEC/KICD boards
- **Bangladesh**: National Curriculum (NCTB) with multiple examination boards
- **USA**: Common Core State Standards with NGSS
- **UK**: National Curriculum for England with GCSE and A-Levels

### Intelligence Engines
Four specialized engines serve each user segment:

| Engine | Purpose | Key Technology |
|--------|---------|----------------|
| Student Outcome Engine | Adaptive learning & progress tracking | Spaced repetition, Knowledge graphs, Socratic AI |
| Teacher Intelligence Engine | Lesson planning & time savings | Bundle generation, LMS integration, Standards mapping |
| Professional Intelligence Engine | Research & portfolio management | Hybrid search, Citation tracking, Portfolio analytics |
| SME Growth Automation Engine | Business automation & analytics | Predictive AI, Webhooks, API connectors |

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

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ai-shiksha.git
cd ai-shiksha
