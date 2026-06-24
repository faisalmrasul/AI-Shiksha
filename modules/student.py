import streamlit as st
import json
import random
from datetime import datetime, timedelta

class StudentModule:
    def __init__(self):
        self.content_file = "data/content.json"
        self.progress_file = "data/progress.json"
        self.ensure_data_files()
        
    def ensure_data_files(self):
        """Ensure data files exist with sample content"""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Sample content for students
        if not os.path.exists(self.content_file):
            sample_content = {
                "subjects": {
                    "mathematics": {
                        "chapters": [
                            {
                                "id": "math_ch1",
                                "title": "Algebra",
                                "topics": ["Linear Equations", "Quadratic Equations", "Polynomials"],
                                "simplified": "Algebra is the study of mathematical symbols and rules for manipulating these symbols.",
                                "mcqs": [
                                    {
                                        "question": "What is the solution to 2x + 3 = 7?",
                                        "options": ["x = 2", "x = 3", "x = 4", "x = 5"],
                                        "correct": 0,
                                        "explanation": "2x + 3 = 7 → 2x = 4 → x = 2"
                                    },
                                    {
                                        "question": "What is the value of x in x² = 25?",
                                        "options": ["5", "-5", "±5", "25"],
                                        "correct": 2,
                                        "explanation": "x² = 25 → x = ±5"
                                    }
                                ]
                            },
                            {
                                "id": "math_ch2",
                                "title": "Geometry",
                                "topics": ["Triangles", "Circles", "Coordinate Geometry"],
                                "simplified": "Geometry is the branch of mathematics concerned with shapes, sizes, and properties of space.",
                                "mcqs": [
                                    {
                                        "question": "What is the sum of angles in a triangle?",
                                        "options": ["90°", "180°", "270°", "360°"],
                                        "correct": 1,
                                        "explanation": "The sum of interior angles in a triangle is always 180°"
                                    }
                                ]
                            }
                        ]
                    },
                    "science": {
                        "chapters": [
                            {
                                "id": "sci_ch1",
                                "title": "Physics Basics",
                                "topics": ["Motion", "Force", "Energy"],
                                "simplified": "Physics is the study of matter, energy, and their interactions.",
                                "mcqs": [
                                    {
                                        "question": "What is Newton's first law of motion?",
                                        "options": ["F = ma", "Every action has an equal and opposite reaction", "An object in motion stays in motion", "Energy cannot be created or destroyed"],
                                        "correct": 2,
                                        "explanation": "Newton's first law states that an object at rest stays at rest and an object in motion stays in motion unless acted upon by an external force."
                                    }
                                ]
                            }
                        ]
                    },
                    "english": {
                        "chapters": [
                            {
                                "id": "eng_ch1",
                                "title": "Grammar Fundamentals",
                                "topics": ["Parts of Speech", "Tenses", "Sentence Structure"],
                                "simplified": "English grammar helps us communicate effectively and clearly.",
                                "mcqs": [
                                    {
                                        "question": "Which of these is a verb?",
                                        "options": ["Run", "Book", "Table", "Apple"],
                                        "correct": 0,
                                        "explanation": "'Run' is an action word, making it a verb."
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
            
            with open(self.content_file, "w") as f:
                json.dump(sample_content, f, indent=2)
    
    def show_learning_path(self):
        """Display learning path for students"""
        st.markdown("<h2 class='sub-header'>🎓 Your Learning Path</h2>", unsafe_allow_html=True)
        
        # Load user progress
        progress = self.load_progress()
        subjects = self.get_subjects()
        
        # Show progress summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📚 Subjects", len(subjects.keys()))
        with col2:
            completed_chapters = sum(1 for s in subjects for c in s.get('chapters', []) 
                                   if progress.get('completed_chapters', {}).get(c['id'], False))
            total_chapters = sum(len(s.get('chapters', [])) for s in subjects.values())
            st.metric("📖 Chapters Completed", f"{completed_chapters}/{total_chapters}")
        with col3:
            avg_score = progress.get('avg_mcq_score', 0)
            st.metric("🏆 Avg MCQ Score", f"{avg_score:.1f}%")
        
        st.markdown("---")
        
        # Display subjects with progress
        for subject_name, subject_data in subjects.items():
            with st.expander(f"📘 {subject_name.title()}"):
                for chapter in subject_data.get('chapters', []):
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        is_completed = progress.get('completed_chapters', {}).get(chapter['id'], False)
                        status = "✅" if is_completed else "📝"
                        st.write(f"{status} **{chapter['title']}**")
                    with col2:
                        if st.button("Study", key=f"study_{chapter['id']}"):
                            st.session_state.current_chapter = chapter
                            st.session_state.current_subject = subject_name
                            st.rerun()
                    with col3:
                        if st.button("Practice MCQ", key=f"mcq_{chapter['id']}"):
                            self.show_mcq_practice(chapter)
    
    def show_subjects(self):
        """Display all subjects"""
        st.markdown("<h2 class='sub-header'>📚 Subjects</h2>", unsafe_allow_html=True)
        
        subjects = self.get_subjects()
        for subject_name, subject_data in subjects.items():
            with st.container():
                st.markdown(f"### {subject_name.title()}")
                for chapter in subject_data.get('chapters', []):
                    st.markdown(f"- **{chapter['title']}**")
                    st.markdown(f"  *Topics: {', '.join(chapter['topics'])}*")
                    if st.button(f"📖 Read Simplified Version", key=f"simplify_{chapter['id']}"):
                        with st.expander("Simplified Explanation", expanded=True):
                            st.write(chapter['simplified'])
                st.markdown("---")
    
    def show_mcq_practice(self, chapter=None):
        """Display MCQ practice"""
        st.markdown("<h2 class='sub-header'>📝 MCQ Practice</h2>", unsafe_allow_html=True)
        
        if chapter is None:
            chapter = st.session_state.get('current_chapter', None)
            
        if not chapter:
            st.info("Select a chapter to practice")
            return
            
        st.write(f"Practicing: **{chapter['title']}**")
        
        # Get MCQ questions
        mcqs = chapter.get('mcqs', [])
        if not mcqs:
            st.info("No MCQs available for this chapter")
            return
            
        # Initialize session state for MCQ
        mcq_key = f"mcq_{chapter['id']}"
        if mcq_key not in st.session_state:
            st.session_state[mcq_key] = {
                'current': 0,
                'answers': [],
                'score': 0,
                'submitted': False
            }
        
        mcq_state = st.session_state[mcq_key]
        
        # Display current MCQ
        if mcq_state['current'] < len(mcqs):
            current_mcq = mcqs[mcq_state['current']]
            st.markdown(f"**Question {mcq_state['current'] + 1} of {len(mcqs)}**")
            st.write(current_mcq['question'])
            
            # Display options
            answer = st.radio(
                "Select your answer:",
                current_mcq['options'],
                key=f"radio_{chapter['id']}_{mcq_state['current']}"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Submit Answer", key=f"submit_{chapter['id']}_{mcq_state['current']}"):
                    selected_index = current_mcq['options'].index(answer)
                    is_correct = selected_index == current_mcq['correct']
                    
                    mcq_state['answers'].append({
                        'question': current_mcq['question'],
                        'selected': answer,
                        'correct': current_mcq['options'][current_mcq['correct']],
                        'is_correct': is_correct
                    })
                    
                    if is_correct:
                        mcq_state['score'] += 1
                    
                    mcq_state['current'] += 1
                    mcq_state['submitted'] = True
                    st.rerun()
            
            with col2:
                if st.button("Skip", key=f"skip_{chapter['id']}_{mcq_state['current']}"):
                    mcq_state['current'] += 1
                    mcq_state['submitted'] = True
                    st.rerun()
                    
            # Show explanation if submitted
            if mcq_state.get('submitted', False) and mcq_state['answers']:
                last_answer = mcq_state['answers'][-1]
                if last_answer['is_correct']:
                    st.success("✅ Correct! " + current_mcq['explanation'])
                else:
                    st.error("❌ Incorrect. " + current_mcq['explanation'])
        
        else:
            # Show results
            total = len(mcqs)
            score = mcq_state['score']
            percentage = (score / total) * 100
            
            st.markdown("### 🎯 Practice Complete!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Questions", total)
            col2.metric("Correct Answers", score)
            col3.metric("Score", f"{percentage:.1f}%")
            
            # Show detailed answers
            with st.expander("Review Answers"):
                for i, ans in enumerate(mcq_state['answers']):
                    status = "✅" if ans['is_correct'] else "❌"
                    st.write(f"{status} Q{i+1}: {ans['question']}")
                    st.write(f"Your answer: {ans['selected']}")
                    st.write(f"Correct answer: {ans['correct']}")
                    st.markdown("---")
            
            if st.button("Retry Practice"):
                del st.session_state[mcq_key]
                st.rerun()
    
    def show_study_plan(self):
        """Display study plan"""
        st.markdown("<h2 class='sub-header'>📅 Study Plan</h2>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Weekly Study Schedule")
            
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            subjects = self.get_subjects().keys()
            
            study_plan = {}
            for day in days:
                with st.expander(day):
                    selected_subjects = st.multiselect(
                        f"Select subjects for {day}",
                        list(subjects),
                        key=f"plan_{day}",
                        default=list(subjects)[:2] if day in ["Monday", "Wednesday", "Friday"] else list(subjects)[2:]
                    )
                    study_plan[day] = selected_subjects
                    duration = st.slider(f"Study duration (minutes)", 15, 120, 30, key=f"duration_{day}")
                    st.write(f"📚 Planned study time: {duration} minutes")
        
        with col2:
            st.subheader("AI Recommendations")
            st.info("Based on your progress, we recommend focusing on:")
            st.write("📘 **Mathematics** - Algebra (2 hours needed)")
            st.write("📗 **Science** - Physics Basics (1.5 hours needed)")
            st.write("📙 **English** - Grammar Fundamentals (1 hour needed)")
            
            if st.button("Generate Personalized Study Plan"):
                st.success("Study plan generated! Check your email.")
    
    def load_progress(self):
        """Load user progress"""
        if os.path.exists(self.progress_file):
            with open(self.progress_file, "r") as f:
                return json.load(f)
        return {}
    
    def get_subjects(self):
        """Get all subjects"""
        try:
            with open(self.content_file, "r") as f:
                data = json.load(f)
                return data.get('subjects', {})
        except:
            return {}
