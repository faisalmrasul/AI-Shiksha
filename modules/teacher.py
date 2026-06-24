import streamlit as st
import json
import random
from datetime import datetime

class TeacherModule:
    def __init__(self):
        self.templates_file = "data/teacher_templates.json"
        self.ensure_data_files()
        
    def ensure_data_files(self):
        """Ensure teacher template files exist"""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(self.templates_file):
            templates = {
                "lesson_templates": [
                    {
                        "id": "lesson_1",
                        "title": "Introduction to AI",
                        "grade": "9-12",
                        "duration": "45 minutes",
                        "objectives": [
                            "Understand what AI is",
                            "Identify AI applications in daily life",
                            "Discuss ethical implications of AI"
                        ],
                        "activities": [
                            "Icebreaker: AI in daily life",
                            "AI video demonstration",
                            "Group discussion on AI ethics"
                        ],
                        "assessment": "MCQ quiz on AI basics"
                    },
                    {
                        "id": "lesson_2",
                        "title": "Machine Learning Basics",
                        "grade": "11-12",
                        "duration": "60 minutes",
                        "objectives": [
                            "Define machine learning",
                            "Differentiate between supervised and unsupervised learning",
                            "Understand the training process"
                        ],
                        "activities": [
                            "Interactive ML demo",
                            "Hands-on classification exercise",
                            "Real-world ML application examples"
                        ],
                        "assessment": "Project: Build a simple classifier"
                    }
                ],
                "assessment_templates": [
                    {
                        "id": "assess_1",
                        "title": "AI Basics Quiz",
                        "subject": "Computer Science",
                        "questions": [
                            {
                                "question": "What does AI stand for?",
                                "options": ["Artificial Intelligence", "Automated Intelligence", "Advanced Intelligence", "Applied Intelligence"],
                                "correct": 0
                            },
                            {
                                "question": "Which is an example of AI application?",
                                "options": ["Spell Checker", "Smart Speaker", "Calculator", "All of the above"],
                                "correct": 3
                            }
                        ]
                    }
                ],
                "feedback_templates": [
                    {
                        "id": "feedback_1",
                        "title": "General Feedback Template",
                        "template": "Dear {student_name},\n\nI'm pleased to share feedback on your recent performance.\n\nStrengths:\n- {strength_1}\n- {strength_2}\n\nAreas for Improvement:\n- {improvement_1}\n- {improvement_2}\n\nOverall Progress: {overall_grade}\n\nNext Steps:\n- {next_step_1}\n- {next_step_2}\n\nKeep up the great work!\n\nSincerely,\n{teacher_name}"
                    }
                ]
            }
            
            with open(self.templates_file, "w") as f:
                json.dump(templates, f, indent=2)
    
    def show_learning_path(self):
        """Display teacher learning path"""
        st.markdown("<h2 class='sub-header'>👨‍🏫 Teacher AI Training Path</h2>", unsafe_allow_html=True)
        
        st.info("""
        **AI for Teachers**: Learn to use AI for:
        - 📝 Lesson planning and content creation
        - 📊 Automated assessment generation
        - 💬 Personalized student feedback
        - 🏫 Classroom administration
        """)
        
        modules = [
            {
                "title": "Module 1: AI Basics for Educators",
                "status": "✅ Completed",
                "description": "Understanding AI fundamentals and their applications in education"
            },
            {
                "title": "Module 2: AI-Powered Lesson Planning",
                "status": "🔄 In Progress",
                "description": "Using AI tools to create engaging lesson plans"
            },
            {
                "title": "Module 3: Automated Assessment",
                "status": "📝 Pending",
                "description": "Generate and grade assessments using AI"
            },
            {
                "title": "Module 4: Personalized Student Feedback",
                "status": "📝 Pending",
                "description": "Provide individualized feedback at scale"
            }
        ]
        
        for module in modules:
            with st.expander(f"{module['status']} - {module['title']}"):
                st.write(module['description'])
                if "In Progress" in module['status']:
                    st.progress(0.65)
                    st.write("65% complete")
                elif "Pending" in module['status']:
                    if st.button("Start Module", key=f"start_{module['title']}"):
                        st.success("Module started!")
    
    def show_lesson_planning(self):
        """Display lesson planning tools"""
        st.markdown("<h2 class='sub-header'>📝 AI-Powered Lesson Planning</h2>", unsafe_allow_html=True)
        
        # Load templates
        try:
            with open(self.templates_file, "r") as f:
                templates = json.load(f)
        except:
            templates = {}
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Create New Lesson Plan")
            
            with st.form("lesson_plan_form"):
                subject = st.text_input("Subject")
                grade = st.text_input("Grade Level")
                topic = st.text_input("Topic")
                duration = st.number_input("Duration (minutes)", min_value=15, max_value=180, value=45)
                
                objectives = st.text_area("Learning Objectives (one per line)")
                activities = st.text_area("Activities (one per line)")
                
                if st.form_submit_button("Generate Lesson Plan"):
                    # Create a structured lesson plan
                    lesson_plan = {
                        "subject": subject,
                        "grade": grade,
                        "topic": topic,
                        "duration": duration,
                        "objectives": [obj.strip() for obj in objectives.split('\n') if obj.strip()],
                        "activities": [act.strip() for act in activities.split('\n') if act.strip()],
                        "generated_at": datetime.now().isoformat()
                    }
                    
                    st.session_state.current_lesson_plan = lesson_plan
                    st.success("Lesson plan created! View it on the right.")
        
        with col2:
            st.subheader("Lesson Plan Preview")
            
            if 'current_lesson_plan' in st.session_state:
                plan = st.session_state.current_lesson_plan
                st.markdown(f"**Subject:** {plan['subject']}")
                st.markdown(f"**Grade:** {plan['grade']}")
                st.markdown(f"**Topic:** {plan['topic']}")
                st.markdown(f"**Duration:** {plan['duration']} minutes")
                
                st.markdown("**Objectives:**")
                for obj in plan['objectives']:
                    st.write(f"- {obj}")
                
                st.markdown("**Activities:**")
                for act in plan['activities']:
                    st.write(f"- {act}")
                
                if st.button("💾 Save Lesson Plan"):
                    st.success("Lesson plan saved to your library!")
            else:
                st.info("Create a lesson plan to see preview here")
            
            # Show template suggestions
            st.subheader("📚 Template Suggestions")
            if templates.get('lesson_templates'):
                selected_template = st.selectbox(
                    "Choose a template:",
                    [t['title'] for t in templates['lesson_templates']]
                )
                
                for template in templates['lesson_templates']:
                    if template['title'] == selected_template:
                        with st.expander("Preview Template"):
                            st.write(f"**Grade:** {template['grade']}")
                            st.write(f"**Duration:** {template['duration']}")
                            st.write(f"**Objectives:** {', '.join(template['objectives'])}")
                            st.write(f"**Activities:** {', '.join(template['activities'])}")
    
    def show_assessment(self):
        """Display assessment generation tools"""
        st.markdown("<h2 class='sub-header'>📊 AI-Powered Assessment Generator</h2>", unsafe_allow_html=True)
        
        with st.form("assessment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                subject = st.text_input("Subject")
                topic = st.text_input("Topic")
                num_questions = st.number_input("Number of Questions", min_value=5, max_value=30, value=10)
                
            with col2:
                difficulty = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
                question_type = st.multiselect("Question Types", ["MCQ", "True/False", "Short Answer", "Essay"])
                
            if st.form_submit_button("Generate Assessment"):
                st.success(f"Assessment generated with {num_questions} questions for {subject} - {topic}")
                
                # Show sample questions
                st.subheader("Sample Questions")
                for i in range(min(3, num_questions)):
                    with st.container():
                        st.markdown(f"**Q{i+1}:** Sample question about {topic} (Generated by AI)")
                        st.markdown(f"- A. Option A")
                        st.markdown(f"- B. Option B")
                        st.markdown(f"- C. Option C")
                        st.markdown(f"- D. Option D")
                        st.markdown("---")
                
                if st.button("Download Assessment"):
                    st.info("Assessment downloaded as PDF!")
    
    def show_feedback(self):
        """Display student feedback tools"""
        st.markdown("<h2 class='sub-header'>💬 Personalized Student Feedback</h2>", unsafe_allow_html=True)
        
        # Student selection
        student_name = st.text_input("Student Name")
        student_performance = st.selectbox(
            "Performance Level",
            ["Excellent", "Good", "Average", "Needs Improvement", "Struggling"]
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            strengths = st.text_area("Strengths (one per line)")
            improvements = st.text_area("Areas for Improvement (one per line)")
            
        with col2:
            overall_grade = st.selectbox("Overall Grade", ["A", "B", "C", "D", "F"])
            next_steps = st.text_area("Next Steps (one per line)")
            
        if st.button("Generate Personalized Feedback"):
            # Generate feedback
            feedback = f"""
Dear {student_name},

I'm pleased to provide feedback on your recent performance.

Strengths:
{chr(10).join(['- ' + s for s in strengths.split('\n') if s.strip()])}

Areas for Improvement:
{chr(10).join(['- ' + i for i in improvements.split('\n') if i.strip()])}

Overall Progress: {overall_grade}

Next Steps:
{chr(10).join(['- ' + n for n in next_steps.split('\n') if n.strip()])}

Keep up the great work!

Sincerely,
[Teacher Name]
"""
            st.subheader("Generated Feedback")
            st.markdown(feedback)
            
            if st.button("Send Feedback"):
                st.success(f"Feedback sent to {student_name}")
