# app.py - Main Application Entry Point with Global Real-World Scenario Demos
# Place this file in the root directory of your repository.

import streamlit as st
import json
import os
import random

# Optional imports for modular extensions
try:
    from modules.auth import AuthManager
    from modules.dashboard import Dashboard
    from modules.student import StudentModule
    from modules.teacher import TeacherModule
    from modules.professional import ProfessionalModule
    from modules.business import BusinessModule
    from modules.agent import LearningAgent
    modules_available = True
except Exception:
    modules_available = False

# ==================== MOCK DATA & REAL-WORLD DEMO ENGINES ====================

MCQ_QUESTIONS = {
    "Mathematics (Adaptive Secondary Exam)": [
        {
            "id": 1,
            "question": "Solve for x: 2x + 5 = 15",
            "options": ["x = 3", "x = 5", "x = 7", "x = 10"],
            "correct": "x = 5",
            "explanation": "Subtract 5 from both sides: 2x = 10, then divide by 2: x = 5.",
            "socratic_hint": "What step reduces the constant term on the left side of the equation?"
        },
        {
            "id": 2,
            "question": "What is the interior angle sum of a polygon with 5 sides?",
            "options": ["360°", "540°", "720°", "180°"],
            "correct": "540°",
            "explanation": "The formula is (n - 2) * 180°. For n = 5: (5 - 2) * 180 = 540°.",
            "socratic_hint": "Remember how many triangles can be formed inside a 5-sided polygon from one vertex."
        }
    ],
    "General Science & Physics": [
        {
            "id": 3,
            "question": "Which process converts solar light directly into chemical energy in green plants?",
            "options": ["Respiration", "Photosynthesis", "Transpiration", "Fermentation"],
            "correct": "Photosynthesis",
            "explanation": "Photosynthesis turns light energy, CO2, and water into glucose and oxygen.",
            "socratic_hint": "Focus on the reaction taking place within the plant's chloroplasts."
        }
    ]
}

LEARNING_PATHS = {
    "Student": {
        "icon": "📚",
        "modules": [
            "Adaptive Exam Readiness & Step-by-Step Reasoning",
            "English Language Learning (ELL) Spoken/Written Track",
            "Competitive Entrance Exam Prep (Geography & GK)",
            "Socratic Problem-Solving & Verification Loops"
        ],
        "progress": 78
    },
    "Teacher": {
        "icon": "👨‍🏫",
        "modules": [
            "Universal Lesson & Rubric Builder",
            "Feedback Drafting Assistant (60% Time Savings)",
            "Classroom Ethics & Responsible AI Policy Integrator",
            "Localized Curriculum Overlay Mapping"
        ],
        "progress": 60
    },
    "Professional": {
        "icon": "💼",
        "modules": [
            "Applied AI Execution (Research Synthesis & Reports)",
            "Verifiable Artifact & Portfolio Generator",
            "Domain Focus: Business & Financial Analysis",
            "Enterprise Data Privacy & Prompt Guardrails"
        ],
        "progress": 45
    },
    "SME Business Owner": {
        "icon": "🏢",
        "modules": [
            "No-Code Customer Support Automation (WhatsApp/M-Pesa)",
            "Localized Marketing Content Generator",
            "Plain-Language Sales & Inventory Analytics",
            "Multi-Channel Automated Payment Receipts"
        ],
        "progress": 30
    }
}

# ==================== REAL-WORLD DEMO SCENARIO UI FUNCTIONS ====================

def show_demo_student_engine():
    """Scenario 1: Practice & Score Tracking Engine"""
    st.header("📈 Student Engine: Practice & Score Tracking")
    st.markdown("*Real-World Scenario: Kenya National Exit Exam preparation with adaptive hints and visible parent dashboard progress.*")
    st.divider()

    tab1, tab2 = st.tabs(["✍️ Student Adaptive Practice Loop", "📊 Parent Progress Dashboard"])

    with tab1:
        subject = st.selectbox("Select Exam Track:", list(MCQ_QUESTIONS.keys()))
        questions = MCQ_QUESTIONS.get(subject, [])

        if "student_score" not in st.session_state:
            st.session_state.student_score = 54

        if questions:
            q = questions[0]
            st.markdown(f"### Question: {q['question']}")

            with st.expander("💡 Need a reasoning clue? (Socratic Prompt)"):
                st.info(f"**Guidance:** {q['socratic_hint']}")

            selected_opt = st.radio("Select your answer:", q['options'], key="student_opt")

            if st.button("Submit Answer", type="primary"):
                if selected_opt == q['correct']:
                    st.balloons()
                    st.success(f"✅ **Correct!** {q['explanation']}")
                    st.session_state.student_score = min(100, st.session_state.student_score + 8)
                else:
                    st.error(f"❌ Incorrect. The correct answer is {q['correct']}. Explanation: {q['explanation']}")

    with tab2:
        st.subheader("Parent View: Student Growth Metrics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Baseline Score (Week 1)", "54%")
        col2.metric("Current Score (Week 4)", f"{st.session_state.student_score}%", f"+{st.session_state.student_score - 54}%")
        col3.metric("Mastery Status", "Proficient")

        st.progress(st.session_state.student_score / 100)
        st.caption("Verified Skill Badges: Quadratic Equations, Basic Physics, Vocabulary Enhancement.")


def show_demo_teacher_engine():
    """Scenario 2: Universal Lesson & Rubric Builder"""
    st.header("📝 Teacher Engine: Universal Lesson & Rubric Builder")
    st.markdown("*Real-World Scenario: Middle school science teacher in Indonesia generating local curriculum compliant plans and rubrics.*")
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        topic = st.text_input("Lesson Subject/Topic:", "Photosynthesis & Leaf Extraction Lab")
        grade_level = st.selectbox("Grade Level:", ["Grade 6 (Middle School)", "Grade 8", "High School"])
        curriculum = st.selectbox("Curriculum Overlay:", ["Indonesia Kurikulum Merdeka", "GCSE Standard", "IB PYP", "Generic Core"])
    with col2:
        duration = st.slider("Lesson Duration (Minutes):", 30, 90, 45)
        rubric_tiers = st.slider("Rubric Grading Tiers:", 3, 5, 4)

    if st.button("✨ Generate Lesson Plan & Evaluation Rubric", type="primary"):
        with st.spinner("Compiling pedagogical structure..."):
            st.success("Plan & Rubric generated in 1.4 seconds!")
            
            t1, t2 = st.tabs(["📋 Lesson Structure", "📊 Assessment Rubric"])
            with t1:
                st.markdown(f"### Lesson Plan: {topic} ({curriculum})")
                st.markdown(f"**Target Level:** {grade_level} | **Duration:** {duration} mins")
                st.markdown("""
                - **00-05 mins (Warm-up):** Quick diagnostic question on plant energy sources.
                - **05-25 mins (Lab Experiment):** Hands-on leaf extraction using low-cost household materials.
                - **25-40 mins (Group Discussion):** Socratic debriefing on chlorophyll breakdown.
                - **40-45 mins (Exit Ticket):** Written summary verification prompt.
                """)
            
            with t2:
                st.markdown("### Evaluation Rubric")
                st.table([
                    {"Criteria": "Understanding Chlorophyll", "Needs Improvement": "Unable to define", "Developing": "Partial definition", "Proficient": "Accurate definition", "Exemplary": "Explains chemical reaction"},
                    {"Criteria": "Experimental Accuracy", "Needs Improvement": "Missed lab steps", "Developing": "Followed with help", "Proficient": "Followed all steps", "Exemplary": "Flawless lab execution"},
                    {"Criteria": "Observation Clarity", "Needs Improvement": "No written notes", "Developing": "Incomplete notes", "Proficient": "Clear written report", "Exemplary": "Detailed analysis"}
                ])


def show_demo_professional_engine():
    """Scenario 3: Applied AI Workflow Track"""
    st.header("💼 Professional Engine: Applied AI Workflow Track")
    st.markdown("*Real-World Scenario: Mid-level marketing manager executing automated research synthesis and client reports.*")
    st.divider()

    st.subheader("Interactive Task: Weekly Client Status Automation")
    
    step1_input = st.text_area(
        "Step 1: Raw Client Feedback & KPI Logs",
        "Ad Spend: $1,200 | Click-Through Rate: 3.4% (up 1.1%) | Leads: 42 | Client Note: Wants faster response time on leads."
    )

    if st.button("⚡ Execute Workflow Macro", type="primary"):
        with st.spinner("Running Applied Workflow..."):
            st.markdown("---")
            st.markdown("### Generated Work Products (Artifacts)")

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**1. Executive Research & KPI Summary**")
                st.info("""
                • Ad campaign performance improved (+1.1% CTR).
                • Total leads captured: 42 conversion points.
                • Identified bottleneck: Lead response velocity.
                """)

            with col2:
                st.markdown("**2. Automated Client Email Draft**")
                st.success(f"""
                **Subject:** Weekly Performance Summary & Action Items

                Dear Client,

                Here is your automated campaign recap:
                - CTR increased to 3.4% with total spend at $1,200.
                - Generated 42 qualified leads this week.

                Next Action: Optimizing response workflow for immediate lead engagement.
                """)


def show_demo_sme_engine():
    """Scenario 4: No-Code Customer Support Automation"""
    st.header("🏢 SME Engine: No-Code Support Automation")
    st.markdown("*Real-World Scenario: Clothing retailer in Nigeria receiving automated WhatsApp messages linked to regional payment rails (M-Pesa/Flutterwave).*")
    st.divider()

    st.subheader("Simulated Customer WhatsApp Query")
    message = st.text_input("Incoming Customer Message:", "Do you have the blue jacket in Medium, and can I pay via M-Pesa?")

    col1, col2 = st.columns(2)
    with col1:
        payment_rail = st.selectbox("Integrated Payment Rail:", ["M-Pesa", "Stripe", "Flutterwave", "Local SMS Gateway"])
    with col2:
        channel = st.selectbox("Communication Channel:", ["WhatsApp Business API", "Regional SMS", "Web Chat"])

    if st.button("🤖 Process Automated Response"):
        st.markdown("### Automated Platform Actions")
        
        st.markdown(f"**Step 1:** Queried local database inventory for *'Blue Jacket - Medium'*. (Status: **In Stock - 3 left**)")
        st.markdown(f"**Step 2:** Generated custom payment link using **{payment_rail}**.")
        
        st.markdown("### Outgoing Message to Customer:")
        st.success(f"""
        📱 **{channel} Response:**
        "Yes! We have 3 blue jackets left in Medium. 
        You can complete your order directly using {payment_rail} here: https://pay.aishiksha.io/checkout/item-8823
        Once paid, your tracking receipt will be sent automatically via SMS!"
        """)

# ==================== MAIN NAVIGATION & APP STRUCTURE ====================

st.set_page_config(
    page_title="AI Shiksha - Global AI Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.sidebar.title("🤖 AI Shiksha Global")
    st.sidebar.caption("Outcome-Driven AI Platform")
    
    menu_options = [
        "🌐 Home & Overview",
        "🎓 Student Engine (Score Prep)",
        "👨‍🏫 Teacher Engine (Lesson Builder)",
        "💼 Professional Engine (Workflow Lab)",
        "🏢 SME Engine (Growth Automation)"
    ]
    
    choice = st.sidebar.radio("Navigate Sections:", menu_options)
    
    if choice == "🌐 Home & Overview":
        st.title("🤖 AI Shiksha: Global Edition")
        st.subheader("Outcomes People Already Pay For — Delivered Through AI in Any Underserved Language")
        
        st.markdown("""
        AI Shiksha delivers tangible, high-value outcomes directly to students, teachers, professionals, and small business owners.
        """)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Students", "Grade Boosts", "Socratic Guidance")
        c2.metric("Teachers", "Hours Saved", "Auto Rubrics")
        c3.metric("Professionals", "Career Ready", "Workflow Macros")
        c4.metric("SMEs", "Revenue Growth", "Multi-Rail Payments")

        st.divider()
        st.markdown("### Explore Real-World Demo Modules from the Sidebar")
        
    elif choice == "🎓 Student Engine (Score Prep)":
        show_demo_student_engine()
        
    elif choice == "👨‍🏫 Teacher Engine (Lesson Builder)":
        show_demo_teacher_engine()
        
    elif choice == "💼 Professional Engine (Workflow Lab)":
        show_demo_professional_engine()
        
    elif choice == "🏢 SME Engine (Growth Automation)":
        show_demo_sme_engine()

if __name__ == "__main__":
    main()
