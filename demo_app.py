"""
AI Shiksha - Funding Prototype Demo
Complete interactive demo with all 4 key features
Run with: streamlit run demo_app.py
"""

import streamlit as st
import random
from datetime import datetime

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="AI Shiksha - Demo",
    page_icon="🎓",
    layout="wide"
)

# ==================== MOCK DATA ====================
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
        },
        {
            "id": 5,
            "question": "১০ - ৪ = কত?",
            "options": ["৪", "৫", "৬", "৭"],
            "correct": "৬",
            "explanation": "১০ - ৪ = ৬"
        }
    ],
    "বিজ্ঞান (Science)": [
        {
            "id": 3,
            "question": "পৃথিবীর নিকটতম নক্ষত্র কোনটি?",
            "options": ["চাঁদ", "সূর্য", "মঙ্গল", "শুক্র"],
            "correct": "সূর্য",
            "explanation": "সূর্য পৃথিবীর নিকটতম নক্ষত্র"
        },
        {
            "id": 6,
            "question": "মানুষের শরীরে কতটি হাড় আছে?",
            "options": ["১০০", "২০৬", "৩০০", "৪০০"],
            "correct": "২০৬",
            "explanation": "মানুষের শরীরে ২০৬টি হাড় আছে"
        }
    ],
    "ইংরেজি (English)": [
        {
            "id": 4,
            "question": "'Cat' এর বাংলা অর্থ কী?",
            "options": ["কুকুর", "বিড়াল", "পাখি", "মাছ"],
            "correct": "বিড়াল",
            "explanation": "'Cat' অর্থ বিড়াল"
        },
        {
            "id": 7,
            "question": "'Beautiful' এর বাংলা অর্থ কী?",
            "options": ["কুৎসিত", "সুন্দর", "বড়", "ছোট"],
            "correct": "সুন্দর",
            "explanation": "'Beautiful' অর্থ সুন্দর"
        }
    ]
}

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

# ==================== MOCK AI FUNCTIONS ====================
def mock_qa_response(question, language):
    """Generate mock responses for Q&A"""
    responses_bn = {
        "ai": "এআই হলো কৃত্রিম বুদ্ধিমত্তা যা মেশিনকে মানুষের মতো চিন্তা করতে শেখায়। এটি আমাদের দৈনন্দিন জীবনের অনেক অংশে ব্যবহৃত হয়।",
        "education": "এআই শিক্ষায় ব্যক্তিগতকৃত শেখার অভিজ্ঞতা, স্বয়ংক্রিয় গ্রেডিং এবং অভিযোজিত মূল্যায়ন সক্ষম করে।",
        "job": "এআই অনেক চাকরি পরিবর্তন করছে, কিন্তু নতুন সুযোগও তৈরি করছে। দক্ষতা বৃদ্ধি গুরুত্বপূর্ণ।",
        "default": f"আপনার প্রশ্নের উত্তরে: '{question}' - এটি একটি গুরুত্বপূর্ণ বিষয়। এআই শিখার মাধ্যমে আপনি আরও জানতে পারবেন। আমাদের প্ল্যাটফর্মে আরও অনেক কিছু আছে!"
    }
    
    responses_en = {
        "ai": "AI is artificial intelligence that enables machines to think like humans. It's used in many parts of our daily lives.",
        "education": "AI enables personalized learning, automated grading, and adaptive assessments in education.",
        "job": "AI is transforming jobs but also creating new opportunities. Upskilling is key to staying relevant.",
        "default": f"Answer to '{question}': This is an important topic. Learn more through AI Shiksha's comprehensive platform."
    }
    
    # Simple keyword matching
    keyword = "default"
    q_lower = question.lower()
    if "ai" in q_lower or "বুদ্ধিমত্তা" in question or "artificial" in q_lower:
        keyword = "ai"
    elif "শিক্ষা" in question or "education" in q_lower or "learn" in q_lower:
        keyword = "education"
    elif "চাকরি" in question or "job" in q_lower or "work" in q_lower:
        keyword = "job"
    
    if language == "বাংলা":
        return f"🤖 {responses_bn.get(keyword, responses_bn['default'])}\n\n📌 আরও জানতে আমাদের লার্নিং পাথে যোগ দিন!\n🔗 https://aishiksha.edu.bd"
    else:
        return f"🤖 {responses_en.get(keyword, responses_en['default'])}\n\n📌 Join our learning paths to know more!\n🔗 https://aishiksha.edu.bd"

def mock_simplify_text(complex_text):
    """Mock text simplification"""
    # If text is in Bengali (contains Bengali characters)
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

# ==================== PAGE FUNCTIONS ====================
def show_home():
    st.markdown("""
    # 🎓 AI Shiksha - Education for All
    
    ### বাংলাদেশের প্রথম সমন্বিত AI লিটারেসি ট্রেনিং প্ল্যাটফর্ম
    ### Bangladesh's First Unified AI Literacy Training Platform
    
    ---
    """)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📚 মোট কোর্স", "২৪+", delta="নতুন")
    with col2:
        st.metric("👥 ব্যবহারকারী", "৫,০০০+", delta="বাড়ছে")
    with col3:
        st.metric("⭐ রেটিং", "৪.৮/৫", delta="চমৎকার")
    with col4:
        st.metric("🎯 সফলতা", "৯২%", delta="শিক্ষার্থী")
    
    st.markdown("""
    ---
    ### 🌟 আমাদের বৈশিষ্ট্যসমূহ / Our Features
    
    | বৈশিষ্ট্য | বিবরণ |
    |-----------|--------|
    | 🗣️ **স্থানীয় ভাষায় Q&A** | যেকোনো প্রশ্ন, সহজ উত্তর |
    | 🎯 **ব্যক্তিগতকৃত লার্নিং পাথ** | প্রতিটি ব্যবহারকারীর জন্য আলাদা |
    | 📝 **MCQ অনুশীলন** | তাত্ক্ষণিক ফিডব্যাক সহ |
    | 📄 **কনটেন্ট সিমপ্লিফায়ার** | জটিল টেক্সট, সহজ ভাষায় |
    """)
    
    st.info("👈 বাম পাশের মেনু থেকে যেকোনো ফিচার নির্বাচন করুন / Select any feature from the sidebar")

def show_local_qa():
    st.header("🗣️ স্থানীয় ভাষায় প্রশ্ন-উত্তর / Q&A in Local Language")
    st.markdown("*যেকোনো প্রশ্ন করুন, পরিষ্কার উত্তর পান / Ask anything, get clear answers*")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        language = st.radio("ভাষা / Language:", ["বাংলা", "English"], horizontal=True)
    with col2:
        st.caption(f"🕐 {datetime.now().strftime('%I:%M %p')}")
    
    st.divider()
    
    # Quick suggestion chips
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
    
    # Main Q&A input
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
        
        # Feedback
        st.caption("🔍 এই উত্তরটি কি সহায়ক ছিল? / Was this answer helpful?")
        col1, col2 = st.columns(2)
        with col1:
            st.button("👍 হ্যাঁ / Yes", key="feedback_yes")
        with col2:
            st.button("👎 না / No", key="feedback_no")
    elif ask_button and not question:
        st.warning("⚠️ অনুগ্রহ করে একটি প্রশ্ন লিখুন / Please type a question")

def show_learning_paths():
    st.header("🎯 ব্যক্তিগতকৃত লার্নিং পাথ / Personalized Learning Paths")
    st.markdown("*আপনার ভূমিকা অনুযায়ী কাস্টমাইজড শেখার পথ / Customized learning paths based on your role*")
    
    # Role selection
    selected_role = st.selectbox(
        "আপনি কে? / Who are you?",
        ["Student", "Teacher", "Professional", "Business Owner"]
    )
    
    if selected_role:
        path_data = LEARNING_PATHS[selected_role]
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader(f"{path_data['icon']} আপনার লার্নিং পাথ / Your Learning Path")
            
            # Progress bar
            st.progress(path_data['progress'] / 100, text=f"অগ্রগতি / Progress: {path_data['progress']}%")
            
            # Modules
            st.markdown("**📋 মডিউলসমূহ / Modules:**")
            for idx, module in enumerate(path_data['modules'], 1):
                col_a, col_b = st.columns([4, 1])
                with col_a:
                    st.write(f"{idx}. {module}")
                with col_b:
                    if st.button("শুরু করুন", key=f"start_{idx}_{selected_role}"):
                        st.success(f"✅ মডিউল {idx} শুরু হয়েছে! / Module {idx} started!")
        
        with col2:
            st.subheader("📊 পরিসংখ্যান / Statistics")
            completed = int(path_data['progress']/25)
            st.metric("✅ সম্পন্ন মডিউল", f"{completed}/{len(path_data['modules'])}")
            st.metric("⏱️ বাকি সময়", "~২.৫ ঘণ্টা")
            st.metric("🏆 অর্জিত স্কোর", f"{path_data['progress'] + 10}%")
            
            st.divider()
            st.caption("💡 *আপনার অগ্রগতি স্বয়ংক্রিয়ভাবে সংরক্ষিত হয়*")
            st.caption("💡 *Your progress is auto-saved*")

def show_mcq_practice():
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
        # Show question counter
        current_q = st.session_state.mcq_index % len(questions)
        st.caption(f"প্রশ্ন {current_q + 1} / {len(questions)}")
        
        q = questions[current_q]
        
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b;">
            <h4>📌 {q['question']}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Display options
        selected_option = st.radio(
            "আপনার উত্তর নির্বাচন করুন / Select your answer:",
            q['options'],
            key=f"mcq_{q['id']}_{current_q}"
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
        
        # Score tracking
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

def show_content_simplifier():
    st.header("📄 কনটেন্ট সিমপ্লিফায়ার / Content Simplifier")
    st.markdown("*যেকোনো জটিল টেক্সট পেস্ট করুন, সহজ ভাষায় ব্যাখ্যা পান / Paste any text, get plain explanation*")
    
    st.info("💡 **উদাহরণ টেক্সট / Sample Text:** নিচের বাটন ক্লিক করে টেস্ট করুন / Click buttons below to test")
    
    # Sample texts
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📘 বাংলা টেক্সট / Bengali Text", use_container_width=True):
            st.session_state.simplifier_text = """
কৃত্রিম বুদ্ধিমত্তা (AI) হলো কম্পিউটার বিজ্ঞানের একটি শাখা যা মেশিনকে মানুষের মতো চিন্তা, সিদ্ধান্ত গ্রহণ এবং সমস্যা সমাধানের ক্ষমতা দেয়। এটি মেশিন লার্নিং, ডিপ লার্নিং এবং ন্যাচারাল ল্যাঙ্গুয়েজ প্রসেসিংয়ের মতো উপ-ক্ষেত্র নিয়ে গঠিত। এই প্রযুক্তি আমাদের দৈনন্দিন জীবনের অনেক অংশে ব্যবহৃত হচ্ছে।
            """
    with col2:
        if st.button("🇬🇧 English Text", use_container_width=True):
            st.session_state.simplifier_text = """
Artificial Intelligence (AI) is a branch of computer science that enables machines to think, make decisions, and solve problems like humans. It consists of subfields such as machine learning, deep learning, and natural language processing. This technology is being used in many parts of our daily lives.
            """
    
    # Main input
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
            
            # Display side by side comparison
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
            
            # Additional features
            st.divider()
            st.subheader("📌 আরও যা করতে পারেন / You can also:")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.button("🔊 অডিও শুনুন / Listen Audio", use_container_width=True)
            with col2:
                st.button("📥 PDF ডাউনলোড করুন / Download PDF", use_container_width=True)
            with col3:
                st.button("📤 শেয়ার করুন / Share", use_container_width=True)
        else:
            st.warning("⚠️ অনুগ্রহ করে কিছু টেক্সট পেস্ট করুন / Please paste some text")

# ==================== MAIN APP ====================
def main():
    # Sidebar navigation
    with st.sidebar:
        st.title("🎓 AI Shiksha")
        st.caption("ভার্সন / Version 2.0 (Demo)")
        
        st.divider()
        
        # Navigation
        st.markdown("### 📌 মেনু / Menu")
        pages = {
            "🏠 হোম / Home": show_home,
            "🗣️ Q&A (স্থানীয় ভাষা)": show_local_qa,
            "🎯 লার্নিং পাথ": show_learning_paths,
            "📝 MCQ অনুশীলন": show_mcq_practice,
            "📄 কনটেন্ট সিমপ্লিফায়ার": show_content_simplifier
        }
        
        selection = st.radio(
            "পৃষ্ঠা নির্বাচন করুন / Select Page",
            list(pages.keys()),
            index=0,
            label_visibility="collapsed"
        )
        
        st.divider()
        
        # User info
        st.caption("👤 ডেমো ব্যবহারকারী / Demo User")
        st.caption("📧 demo@aishiksha.edu.bd")
        
        # Demo mode badge
        st.markdown("""
        <div style="background-color: #ffd700; padding: 10px; border-radius: 5px; text-align: center; margin: 10px 0;">
            🚀 <strong>ডেমো মোড</strong><br>
            <span style="font-size: 12px;">Demo Mode</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.caption("📞 সহায়তার জন্য / Support:")
        st.caption("support@aishiksha.edu.bd")
        st.caption("🔗 https://aishiksha.edu.bd")
    
    # Page content
    pages[selection]()

if __name__ == "__main__":
    main()
