import streamlit as st
import json
import pandas as pd
from datetime import datetime, timedelta

class LearningAgent:
    def __init__(self):
        self.progress_file = "data/progress.json"
        self.ensure_data_files()
        
    def ensure_data_files(self):
        """Ensure data files exist"""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        if not os.path.exists(self.progress_file):
            with open(self.progress_file, "w") as f:
                json.dump({
                    "student_progress": {},
                    "teacher_usage": {},
                    "professional_progress": {},
                    "business_adoption": {}
                }, f)
    
    def show_progress(self):
        """Show learning progress"""
        st.markdown("<h2 class='sub-header'>📈 Your Progress</h2>", unsafe_allow_html=True)
        
        user_type = st.session_state.user_type
        email = st.session_state.user_data.get('email', '')
        
        # Load progress data
        try:
            with open(self.progress_file, "r") as f:
                progress_data = json.load(f)
        except:
            progress_data = {}
        
        # Get user progress based on type
        user_progress = progress_data.get(f"{user_type}_progress", {}).get(email, {})
        
        if user_type == "student":
            self.show_student_progress(user_progress)
        elif user_type == "teacher":
            self.show_teacher_progress(user_progress)
        elif user_type == "professional":
            self.show_professional_progress(user_progress)
        elif user_type == "business":
            self.show_business_progress(user_progress)
        
        # AI Agent Insights
        self.show_agent_insights(user_type, user_progress)
    
    def show_student_progress(self, progress):
        """Show student progress"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            completed = progress.get('completed_chapters', 0)
            total = progress.get('total_chapters', 20)
            st.metric("📚 Chapters Completed", f"{completed}/{total}")
        
        with col2:
            mcq_score = progress.get('mcq_average', 0)
            st.metric("🏆 MCQ Average", f"{mcq_score:.1f}%")
        
        with col3:
            study_time = progress.get('study_time', 0)
            st.metric("⏱️ Study Time", f"{study_time}h")
        
        # Weekly progress chart
        st.subheader("Weekly Progress")
        dates = pd.date_range(end=datetime.now(), periods=7)
        values = [progress.get(f'day_{i}', 0) for i in range(7)]
        
        # Simulate chart data
        chart_data = pd.DataFrame({
            'Date': dates,
            'Activity': values
        })
        st.line_chart(chart_data.set_index('Date'))
    
    def show_teacher_progress(self, progress):
        """Show teacher progress"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📝 Lesson Plans Created", progress.get('lesson_plans', 0))
        with col2:
            st.metric("📊 Assessments Generated", progress.get('assessments', 0))
        with col3:
            st.metric("💬 Feedback Sent", progress.get('feedback_messages', 0))
        
        # Tool adoption
        st.subheader("AI Tool Adoption")
        tools = progress.get('tools_used', {})
        for tool, count in tools.items():
            st.progress(min(count / 10, 1.0))
            st.write(f"{tool}: {count} uses")
    
    def show_professional_progress(self, progress):
        """Show professional progress"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📚 Courses Completed", progress.get('courses_completed', 0))
        with col2:
            st.metric("🏆 Skill Assessment", f"{progress.get('skill_level', 0)}%")
        with col3:
            st.metric("📈 Weekly Nudge", "✅ Completed")
    
    def show_business_progress(self, progress):
        """Show business progress"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🛠️ Tools Adopted", progress.get('tools_adopted', 0))
        with col2:
            st.metric("⚡ Automation Setup", progress.get('automations', 0))
        with col3:
            st.metric("📊 ROI Increase", f"{progress.get('roi', 0)}%")
    
    def show_agent_insights(self, user_type, progress):
        """Show AI agent insights"""
        st.markdown("---")
        st.markdown("<h3>🤖 AI Agent Insights</h3>", unsafe_allow_html=True)
        
        insights = []
        
        if user_type == "student":
            if progress.get('mcq_average', 0) < 60:
                insights.append("📚 Consider reviewing basics - your MCQ scores suggest need for foundation building.")
            elif progress.get('study_time', 0) < 10:
                insights.append("⏰ Increase study time to 1 hour daily for optimal progress.")
            else:
                insights.append("🌟 Great progress! You're on track to achieve your learning goals.")
                
        elif user_type == "teacher":
            if progress.get('lesson_plans', 0) < 5:
                insights.append("💡 Try creating more AI-powered lesson plans to save time and improve quality.")
            else:
                insights.append("👍 Excellent adoption of AI tools! Your students will benefit greatly.")
                
        elif user_type == "professional":
            if progress.get('skill_level', 0) < 50:
                insights.append("📈 Focus on completing more courses to improve your AI skills.")
            else:
                insights.append("🎯 You're developing valuable AI skills for your career.")
                
        elif user_type == "business":
            if progress.get('tools_adopted', 0) < 3:
                insights.append("🚀 Consider adopting more AI tools to transform your business operations.")
            else:
                insights.append("🏢 Your business is becoming an AI-driven enterprise!")
        
        # Display insights
        for insight in insights:
            st.info(insight)
        
        # Weekly recommendation
        st.subheader("📋 Weekly Recommendation")
        if user_type == "student":
            st.write("Recommended focus: Mathematics - Linear Equations (2 hours)")
        elif user_type == "teacher":
            st.write("Recommended: Create 3 AI-powered lesson plans this week")
        elif user_type == "professional":
            st.write("Recommended: Complete Module 2 - Data Analysis with AI")
        elif user_type == "business":
            st.write("Recommended: Set up AI customer support chatbot")
