# app.py - Main Application Entry Point with Complete Demo Features
# This file MUST be in the root directory of your project

import streamlit as st
from modules.auth import AuthManager
from modules.dashboard import Dashboard
from modules.student import StudentModule
from modules.teacher import TeacherModule
from modules.professional import ProfessionalModule
from modules.business import BusinessModule
from modules.agent import LearningAgent
import json
import os
import random
from datetime import datetime

# ==================== DEMO FEATURE IMPORTS ====================
# These are mock data and functions for the demo features
# In production, these would come from actual AI services

# Mock MCQ Questions
MCQ_QUESTIONS = {
    "গণিত (Math)": [
        {
            "id": 1,
            "question": "৫ + ৩ = কত?",
            "options": ["৫", "৭", "৮", "১০"],
            "correct": "৮",
            "explanation": "৫ + ৩ = ৮"
        },
        {
            "id": 2,
            "question": "একটি বর্গক্ষেত্রের কয়টি বাহু আছে?",
            "options": ["৩", "৪", "৫", "৬"],
            "correct": "৪",
            "explanation": "বর্গক্ষেত্রের ৪টি বাহু থাকে"
        }
    ],
    "বিজ্ঞান (Science)": [
        {
            "id": 3,
            "question": "পৃথিবীর নিকটতম নক্ষত্র কোনটি?",
            "options": ["চাঁদ", "সূর্য", "মঙ্গল", "শুক্র"],
            "correct": "সূর্য",
            "explanation": "সূর্য পৃথিবীর নিকটতম নক্ষত্র"
        }
    ],
    "ইংরেজি (English)": [
        {
            "id": 4,
            "question": "'Cat' এর বাংলা অর্থ কী?",
            "options": ["কুকুর", "বিড়াল", "পাখি", "মাছ"],
            "correct": "বিড়াল",
            "explanation": "'Cat' অর্থ বিড়াল"
        }
    ]
}

# Mock Learning Paths
LEARNING_PATHS = {
    "Student": {
        "icon": "📚",
        "modules": [
            "গণিত মৌলিক (Math Basics)",
            "বাংলা ব্যাকরণ (Bengali Grammar)",
            "বিজ্ঞান পরীক্ষা (Science Experiments)",
            "ইংরেজি শব্দভাণ্ডার (English Vocabulary)"
        ],
        "progress": 65
    },
    "Teacher": {
        "icon": "👨‍🏫",
        "modules": [
            "AI-পাওয়ার্ড লেশন প্ল্যান (AI Lesson Planning)",
            "স্বয়ংক্রিয় অ্যাসেসমেন্ট (Auto Assessment)",
            "শ্রেণি ব্যবস্থাপনা (Class Management)",
            "শিক্ষার্থী ফিডব্যাক (Student Feedback)"
        ],
        "progress": 40
    },
    "Professional": {
        "icon": "💼",
        "modules": [
            "স্বাস্থ্যসেবা AI (Healthcare AI)",
            "অর্থনীতি বিশ্লেষণ (Finance Analytics)",
            "ডিজিটাল মার্কেটিং (Digital Marketing)",
            "আইনি সহায়তা (Legal Assistance)"
        ],
        "progress": 25
    },
    "Business Owner": {
        "icon": "🏢",
        "modules": [
            "গ্রাহক সেবা অটোমেশন (Customer Service AI)",
            "AI-মার্কেটিং টুলস (AI Marketing)",
            "ইনভেন্টরি ম্যানেজমেন্ট (Inventory Mgmt)",
            "বাণিজ্যিক সিদ্ধান্ত সমর্থন (Business Analytics)"
        ],
        "progress": 15
    }
}

# Mock AI Functions
def mock_qa_response(question, language):
    """Generate mock responses for Q&A"""
    responses_bn = {
        "ai": "এআই হলো কৃত্রিম বুদ্ধিমত্তা যা মেশিনকে মানুষের মতো চিন্তা করতে শেখায়। এটি আমাদের দৈনন্দিন জীবনের অনেক অংশে ব্যবহৃত হয়।",
        "education": "এআই শিক্ষায় ব্যক্তিগতকৃত শেখার অভিজ্ঞতা, স্বয়ংক্রিয় গ্রেডিং এবং অভিযোজিত মূল্যায়ন সক্ষম করে।",
        "job": "এআই অনেক চাকরি পরিবর্তন করছে, কিন্তু নতুন সুযোগও তৈরি করছে। দক্ষতা বৃদ্ধি গুরুত্বপূর্ণ।",
        "default": f"আপনার প্রশ্নের উত্তরে: '{question}' - এটি একটি গুরুত্বপূর্ণ বিষয়। এআই শিখার মাধ্যমে আপনি আরও জানতে পারবেন।"
    }
    
    responses_en = {
        "ai": "AI is artificial intelligence that enables machines to think like humans. It's used in many parts of our daily lives.",
        "education": "AI enables personalized learning, automated grading, and adaptive assessments in education.",
        "job": "AI is transforming jobs but also creating new opportunities. Upskilling is key to staying relevant.",
        "default": f"Answer to '{question}': This is an important topic. Learn more through AI Shiksha."
    }
    
    keyword = "default"
    q_lower = question.lower()
    if "ai" in q_lower or "বুদ্ধিমত্তা" in question:
        keyword = "ai"
    elif "শিক্ষা" in question or "education" in q_lower:
        keyword = "education"
    elif "চাকরি" in question or "job" in q_lower:
        keyword = "job"
    
    if language == "বাংলা":
        return f"🤖 {responses_bn.get(keyword, responses_bn['default'])}\n\n📌 আরও জানতে আমাদের লার্নিং পাথে যোগ দিন!"
    else:
        return f"🤖 {responses_en.get(keyword, responses_en['default'])}\n\n📌 Join our learning paths to know more!"

def mock_simplify_text(complex_text):
    """Mock text simplification"""
    if any('\u0980' <= char <= '\u09FF' for char in complex_text):
        return f"""
✨ **সহজ সংস্করণ (Simplified):**

{complex_text[:150]}...

📌 **মূল পয়েন্ট (Key Points):**
• এই টেক্সটটির মূল বিষয় হল এআই এবং শিক্ষা
• এটি শিক্ষার্থীদের জন্য সহজ করে বোঝানো হয়েছে
• আরও বিস্তারিত জানতে আমাদের প্ল্যাটফর্ম ব্যবহার করুন

🔗 **শিখুন আরও:** https://aishiksha.edu.bd
        """
    else:
        return f"""
✨ **Plain English Version:**

{complex_text[:150]}...

📌 **Key Takeaways:**
• This text focuses on AI and education
• Simplified for better understanding
• Use our platform for more details

🔗 **Learn More:** https://aishiksha.edu.bd
        """

# ==================== DEMO PAGE FUNCTIONS ====================
def show_demo_qa():
    """Demo: Q&A in Local Language"""
    st.header("🗣️ স্থানীয় ভাষায় প্রশ্ন-উত্তর / Q&A in Local Language")
    st.markdown("*যেকোনো প্রশ্ন করুন, পরিষ্কার উত্তর পান / Ask anything, get clear answers*")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        language = st.radio("ভাষা / Language:", ["বাংলা", "English"], horizontal=True)
    with col2:
        st.caption(f"🕐 {datetime.now().strftime('%I:%M %p')}")
    
    st.divider()
    
    st.subheader("দ্রুত প্রশ্ন / Quick Questions")
    quick_questions = {
        "বাংলা": ["এআই কি?", "এআই কিভাবে কাজ করে?", "শিক্ষায় এআই এর ভূমিকা?", "এআই কি চাকরি নেবে?"],
        "English": ["What is AI?", "How does AI work?", "AI in education?", "Will AI take jobs?"]
    }
    
    cols = st.columns(4)
    for idx, col in enumerate(cols):
        if idx < len(quick_questions[language]):
            if col.button(quick_questions[language][idx], use_container_width=True):
                st.session_state.qa_question = quick_questions[language][idx]
    
    st.divider()
    
    if "qa_question" not in st.session_state:
        st.session_state.qa_question = ""
    
    question = st.text_area(
        "আপনার প্রশ্ন লিখুন / Type your question:",
        value=st.session_state.qa_question,
        height=100,
        placeholder="যেমন: এআই কিভাবে শিক্ষাকে পরিবর্তন করছে? / Eg: How is AI transforming education?"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        ask_button = st.button("💬 জিজ্ঞাসা করুন / Ask", type="primary", use_container_width=True)
    with col2:
        clear_button = st.button("🗑️ মুছুন / Clear", use_container_width=True)
    
    if clear_button:
        st.session_state.qa_question = ""
        st.rerun()
    
    if ask_button and question:
        with st.spinner("🤔 উত্তর তৈরি হচ্ছে / Generating answer..."):
            import time
            time.sleep(1.5)
            response = mock_qa_response(question, language)
        
        st.success("✅ উত্তর প্রস্তুত / Answer Ready!")
        st.info(response)
    elif ask_button and not question:
        st.warning("⚠️ অনুগ্রহ করে একটি প্রশ্ন লিখুন / Please type a question")

def show_demo_learning_paths():
    """Demo: Personalized Learning Paths"""
    st.header("🎯 ব্যক্তিগতকৃত লার্নিং পাথ / Personalized Learning Paths")
    st.markdown("*আপনার ভূমিকা অনুযায়ী কাস্টমাইজড শেখার পথ / Customized learning paths based on your role*")
    
    selected_role = st.selectbox(
        "আপনি কে? / Who are you?",
        ["Student", "Teacher", "Professional", "Business Owner"]
    )
    
    if selected_role:
        path_data = LEARNING_PATHS[selected_role]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"{path_data['icon']} আপনার লার্নিং পাথ / Your Learning Path")
            st.progress(path_data['progress'] / 100, text=f"অগ্রগতি / Progress: {path_data['progress']}%")
            
            st.markdown("**📋 মডিউলসমূহ / Modules:**")
            for idx, module in enumerate(path_data['modules'], 1):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.write(f"{idx}. {module}")
                with col_b:
                    if st.button("শুরু করুন", key=f"demo_start_{idx}_{selected_role}"):
                        st.success(f"✅ মডিউল {idx} শুরু হয়েছে! / Module {idx} started!")
        
        with col2:
            st.subheader("📊 পরিসংখ্যান / Statistics")
            completed = int(path_data['progress']/25)
            st.metric("✅ সম্পন্ন মডিউল", f"{completed}/{len(path_data['modules'])}")
            st.metric("⏱️ বাকি সময়", "~২.৫ ঘণ্টা")
            st.metric("🏆 অর্জিত স্কোর", f"{path_data['progress'] + 10}%")

def show_demo_mcq():
    """Demo: MCQ Practice"""
    st.header("📝 MCQ অনুশীলন / MCQ Practice")
    st.markdown("*তাত্ক্ষণিক ফিডব্যাক সহ / With instant feedback*")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        subject = st.selectbox("বিষয় নির্বাচন করুন / Select Subject:", list(MCQ_QUESTIONS.keys()))
    with col2:
        if st.button("🔄 নতুন প্রশ্ন / New Question", use_container_width=True):
            st.session_state.mcq_index = 0
            st.rerun()
    
    if "mcq_index" not in st.session_state:
        st.session_state.mcq_index = 0
    
    questions = MCQ_QUESTIONS.get(subject, [])
    if questions:
        current_q = st.session_state.mcq_index % len(questions)
        st.caption(f"প্রশ্ন {current_q + 1} / {len(questions)}")
        
        q = questions[current_q]
        
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
            <h4>📌 {q['question']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        selected_option = st.radio(
            "আপনার উত্তর নির্বাচন করুন / Select your answer:",
            q['options'],
            key=f"demo_mcq_{q['id']}_{current_q}"
        )
        
        col1, col2 = st.columns(2)
        with col1:
            check_btn = st.button("✅ চেক করুন / Check", type="primary", use_container_width=True)
        with col2:
            next_btn = st.button("⏭️ পরবর্তী / Next", use_container_width=True)
        
        if check_btn:
            if selected_option == q['correct']:
                st.balloons()
                st.success(f"✅ সঠিক! / Correct! 🎉\n\n📖 {q['explanation']}")
            else:
                st.error(f"❌ ভুল উত্তর। সঠিক উত্তর: {q['correct']}\n\n📖 {q['explanation']}")
        
        if next_btn:
            st.session_state.mcq_index += 1
            st.rerun()
        
        st.divider()
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📊 মোট প্রশ্ন", len(questions))
        with col2:
            st.metric("✅ সঠিক", random.randint(1, 5))
        with col3:
            st.metric("📈 স্কোর", f"{random.randint(60, 95)}%")
    else:
        st.warning("এই বিষয়ে কোন প্রশ্ন নেই / No questions for this subject")

def show_demo_simplifier():
    """Demo: Content Simplifier"""
    st.header("📄 কনটেন্ট সিমপ্লিফায়ার / Content Simplifier")
    st.markdown("*যেকোনো জটিল টেক্সট পেস্ট করুন, সহজ ভাষায় ব্যাখ্যা পান / Paste any text, get plain explanation*")
    
    st.info("💡 **উদাহরণ টেক্সট / Sample Text:** নিচের বাটন ক্লিক করে টেস্ট করুন / Click buttons below to test")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📘 বাংলা টেক্সট / Bengali Text", use_container_width=True):
            st.session_state.simplifier_text = """
কৃত্রিম বুদ্ধিমত্তা (AI) হলো কম্পিউটার বিজ্ঞানের একটি শাখা যা মেশিনকে মানুষের মতো চিন্তা, সিদ্ধান্ত গ্রহণ এবং সমস্যা সমাধানের ক্ষমতা দেয়। এটি মেশিন লার্নিং, ডিপ লার্নিং এবং ন্যাচারাল ল্যাঙ্গুয়েজ প্রসেসিংয়ের মতো উপ-ক্ষেত্র নিয়ে গঠিত।
            """
    with col2:
        if st.button("🇬🇧 English Text", use_container_width=True):
            st.session_state.simplifier_text = """
Artificial Intelligence (AI) is a branch of computer science that enables machines to think, make decisions, and solve problems like humans. It consists of subfields such as machine learning, deep learning, and natural language processing.
            """
    
    if "simplifier_text" not in st.session_state:
        st.session_state.simplifier_text = ""
    
    complex_text = st.text_area(
        "জটিল টেক্সট পেস্ট করুন / Paste complex text:",
        value=st.session_state.simplifier_text,
        height=150,
        placeholder="যেমন: একটি জটিল প্রবন্ধ, আইনি নথি, বা প্রযুক্তিগত ডকুমেন্টেশন"
    )
    
    if st.button("✨ সরলীকরণ করুন / Simplify", type="primary", use_container_width=True):
        if complex_text:
            with st.spinner("⏳ সরলীকরণ হচ্ছে / Simplifying..."):
                import time
                time.sleep(1.5)
                simplified = mock_simplify_text(complex_text)
            
            st.success("✅ সরলীকরণ সম্পন্ন! / Simplified Successfully!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📄 মূল টেক্সট / Original Text**")
                st.markdown(f"""
                <div style="background-color: #fff0f0; padding: 15px; border-radius: 10px; border-left: 5px solid #ff4b4b; height: 250px; overflow-y: scroll;">
                    {complex_text}
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("**✨ সরলীকৃত সংস্করণ / Simplified Version**")
                st.markdown(f"""
                <div style="background-color: #f0fff0; padding: 15px; border-radius: 10px; border-left: 5px solid #00cc66; height: 250px; overflow-y: scroll;">
                    {simplified}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("⚠️ অনুগ্রহ করে কিছু টেক্সট পেস্ট করুন / Please paste some text")

# ==================== ORIGINAL APP CODE (Modified) ====================

# Page configuration
st.set_page_config(
    page_title="AI Shiksha - AI Learning Platform",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .feature-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .bangla-text {
        font-family: 'Noto Sans Bengali', sans-serif;
    }
    .demo-badge {
        background-color: #ffd700;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        display: inline-block;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_type' not in st.session_state:
    st.session_state.user_type = None
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}
if 'page' not in st.session_state:
    st.session_state.page = "home"
if 'show_demo' not in st.session_state:
    st.session_state.show_demo = True  # Show demo features by default

# Initialize modules (only if original modules exist)
try:
    auth_manager = AuthManager()
    dashboard = Dashboard()
    student_module = StudentModule()
    teacher_module = TeacherModule()
    professional_module = ProfessionalModule()
    business_module = BusinessModule()
    learning_agent = LearningAgent()
    modules_available = True
except Exception as e:
    modules_available = False
    st.warning("⚠️ Some modules are not available. Running in demo-only mode.")

# Sidebar navigation
def sidebar_navigation():
    st.sidebar.image("https://via.placeholder.com/150x50?text=AI+Shiksha", use_column_width=True)
    st.sidebar.title("AI Shiksha")
    
    # Demo mode indicator
    if st.session_state.show_demo:
        st.sidebar.markdown('<span class="demo-badge">🚀 DEMO MODE</span>', unsafe_allow_html=True)
        st.sidebar.markdown("---")
    
    if not st.session_state.authenticated:
        menu = ["Home", "Login", "Register"]
        # Add demo features to menu for unauthenticated users
        if st.session_state.show_demo:
            menu.extend(["🎯 Demo Features"])
        choice = st.sidebar.selectbox("Navigation", menu)
        return choice
    else:
        user_type = st.session_state.user_type
        menu = ["Dashboard", "Learning Path", "Progress", "Settings"]
        
        if user_type == "student":
            menu.extend(["Subjects", "MCQ Practice", "Study Plan"])
        elif user_type == "teacher":
            menu.extend(["Lesson Planning", "Assessment", "Student Feedback"])
        elif user_type == "professional":
            menu.extend(["Role-specific Training", "Skill Assessment"])
        elif user_type == "business":
            menu.extend(["Business Tools", "Automation"])
        
        # Add demo features for authenticated users too
        if st.session_state.show_demo:
            menu.extend(["🎯 Demo Features"])
        
        menu.append("Logout")
        choice = st.sidebar.selectbox("Navigation", menu)
        return choice

# Demo features sub-navigation
def demo_sub_navigation():
    st.markdown("---")
    st.subheader("📌 Demo Features")
    
    demo_pages = {
        "🗣️ Q&A (Local Language)": show_demo_qa,
        "🎯 Learning Paths": show_demo_learning_paths,
        "📝 MCQ Practice": show_demo_mcq,
        "📄 Content Simplifier": show_demo_simplifier
    }
    
    demo_choice = st.radio(
        "Select Demo Feature:",
        list(demo_pages.keys()),
        key="demo_choice"
    )
    
    st.markdown("---")
    return demo_pages[demo_choice]

# Main content
def main():
    # Welcome banner for unauthenticated users
    if not st.session_state.authenticated:
        st.markdown("<h1 class='main-header'>🤖 AI Shiksha</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; font-size: 1.2rem;'>Bangladesh's First AI Literacy Training Platform</p>", unsafe_allow_html=True)
        
        # Show feature highlights
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class='feature-card'>
                <h3>🎓 Students</h3>
                <p>Practical AI skills for secondary and university students</p>
                <ul>
                    <li>Subject-specific Q&A</li>
                    <li>MCQ practice with feedback</li>
                    <li>Chapter simplification</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col2:
            st.markdown("""
            <div class='feature-card'>
                <h3>👨‍🏫 Teachers</h3>
                <p>AI-powered teaching tools for educators</p>
                <ul>
                    <li>Lesson planning</li>
                    <li>Assessment generation</li>
                    <li>Student feedback automation</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col3:
            st.markdown("""
            <div class='feature-card'>
                <h3>💼 Professionals</h3>
                <p>Role-specific AI training for working professionals</p>
                <ul>
                    <li>Healthcare</li>
                    <li>Finance</li>
                    <li>Marketing</li>
                    <li>Legal & more</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        with col4:
            st.markdown("""
            <div class='feature-card'>
                <h3>🏢 Small Businesses</h3>
                <p>Hands-on AI training for SME owners</p>
                <ul>
                    <li>Customer service automation</li>
                    <li>AI-assisted marketing</li>
                    <li>Inventory management</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Demo features preview
        if st.session_state.show_demo:
            st.markdown("---")
            st.markdown("### 🚀 Try Our Demo Features")
            st.markdown("Experience AI Shiksha's core features without logging in:")
            
            demo_col1, demo_col2, demo_col3, demo_col4 = st.columns(4)
            with demo_col1:
                if st.button("🗣️ Q&A Demo", use_container_width=True):
                    st.session_state.page = "demo_qa"
                    st.rerun()
            with demo_col2:
                if st.button("🎯 Learning Paths", use_container_width=True):
                    st.session_state.page = "demo_paths"
                    st.rerun()
            with demo_col3:
                if st.button("📝 MCQ Practice", use_container_width=True):
                    st.session_state.page = "demo_mcq"
                    st.rerun()
            with demo_col4:
                if st.button("📄 Simplifier", use_container_width=True):
                    st.session_state.page = "demo_simplifier"
                    st.rerun()
    
    # Navigation
    choice = sidebar_navigation()
    
    # Check if we're in demo mode (unauthenticated)
    if not st.session_state.authenticated and st.session_state.show_demo:
        # Handle demo page routing
        if st.session_state.page == "demo_qa":
            show_demo_qa()
            return
        elif st.session_state.page == "demo_paths":
            show_demo_learning_paths()
            return
        elif st.session_state.page == "demo_mcq":
            show_demo_mcq()
            return
        elif st.session_state.page == "demo_simplifier":
            show_demo_simplifier()
            return
        elif choice == "🎯 Demo Features":
            # Show demo sub-navigation
            demo_page = demo_sub_navigation()
            demo_page()
            return
    
    # Authentication pages
    if not st.session_state.authenticated:
        if choice == "Home" or st.session_state.page == "home":
            # Home already shown above
            pass
            
        elif choice == "Login" or st.session_state.page == "login":
            if modules_available:
                auth_manager.login_page()
            else:
                st.info("🔐 Login module not available. Please register first.")
            
        elif choice == "Register" or st.session_state.page == "register":
            if modules_available:
                auth_manager.register_page()
            else:
                st.info("📝 Registration module not available. Please run with full installation.")
    
    else:
        # Authenticated user pages
        if not modules_available:
            st.warning("⚠️ Full modules not available. Some features may be limited.")
        
        if choice == "Dashboard":
            if modules_available:
                dashboard.show_dashboard(st.session_state.user_data)
            else:
                st.info("📊 Dashboard module not available.")
            
        elif choice == "Learning Path":
            if modules_available:
                if st.session_state.user_type == "student":
                    student_module.show_learning_path()
                elif st.session_state.user_type == "teacher":
                    teacher_module.show_learning_path()
                elif st.session_state.user_type == "professional":
                    professional_module.show_learning_path()
                elif st.session_state.user_type == "business":
                    business_module.show_learning_path()
            else:
                # Fallback to demo learning paths
                show_demo_learning_paths()
                
        elif choice == "Progress":
            if modules_available:
                learning_agent.show_progress()
            else:
                st.info("📈 Progress tracking module not available.")
            
        elif choice == "Subjects" and st.session_state.user_type == "student":
            if modules_available:
                student_module.show_subjects()
            else:
                st.info("📚 Subjects module not available.")
            
        elif choice == "MCQ Practice" and st.session_state.user_type == "student":
            if modules_available:
                student_module.show_mcq_practice()
            else:
                show_demo_mcq()
            
        elif choice == "Study Plan" and st.session_state.user_type == "student":
            if modules_available:
                student_module.show_study_plan()
            else:
                st.info("📋 Study plan module not available.")
            
        elif choice == "Lesson Planning" and st.session_state.user_type == "teacher":
            if modules_available:
                teacher_module.show_lesson_planning()
            else:
                st.info("📝 Lesson planning module not available.")
            
        elif choice == "Assessment" and st.session_state.user_type == "teacher":
            if modules_available:
                teacher_module.show_assessment()
            else:
                st.info("📊 Assessment module not available.")
            
        elif choice == "Student Feedback" and st.session_state.user_type == "teacher":
            if modules_available:
                teacher_module.show_feedback()
            else:
                st.info("💬 Feedback module not available.")
            
        elif choice == "Role-specific Training" and st.session_state.user_type == "professional":
            if modules_available:
                professional_module.show_training()
            else:
                st.info("🎯 Training module not available.")
            
        elif choice == "Skill Assessment" and st.session_state.user_type == "professional":
            if modules_available:
                professional_module.show_skill_assessment()
            else:
                st.info("📈 Skill assessment module not available.")
            
        elif choice == "Business Tools" and st.session_state.user_type == "business":
            if modules_available:
                business_module.show_tools()
            else:
                st.info("🔧 Business tools module not available.")
            
        elif choice == "Automation" and st.session_state.user_type == "business":
            if modules_available:
                business_module.show_automation()
            else:
                st.info("⚡ Automation module not available.")
            
        elif choice == "Settings":
            show_settings()
            
        elif choice == "🎯 Demo Features":
            # Show demo sub-navigation for authenticated users too
            demo_page = demo_sub_navigation()
            demo_page()
            
        elif choice == "Logout":
            if modules_available:
                auth_manager.logout()
            else:
                # Simple logout
                for key in ['authenticated', 'user_type', 'user_data']:
                    if key in st.session_state:
                        st.session_state[key] = None
                st.rerun()

def show_settings():
    st.markdown("<h2 class='sub-header'>⚙️ Settings</h2>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Profile Settings")
        st.text_input("Full Name", value=st.session_state.user_data.get('name', ''))
        st.text_input("Email", value=st.session_state.user_data.get('email', ''))
        st.text_input("Phone", value=st.session_state.user_data.get('phone', ''))
        st.selectbox("Preferred Language", ["English", "Bengali", "Bilingual"])
        
        if st.button("Update Profile"):
            st.success("Profile updated successfully!")
    
    with col2:
        st.subheader("Learning Preferences")
        st.slider("Daily Study Time (minutes)", 10, 120, 30)
        st.selectbox("Learning Pace", ["Beginner", "Intermediate", "Advanced"])
        st.multiselect("Interested Topics", ["AI Basics", "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Robotics"])
        st.selectbox("Notification Preferences", ["Email", "SMS", "Both", "None"])
        
        if st.button("Save Preferences"):
            st.success("Preferences saved successfully!")

if __name__ == "__main__":
    main()
