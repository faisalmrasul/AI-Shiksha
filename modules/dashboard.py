"""
Dashboard Module for AI Shiksha
Displays personalized dashboard based on user type
"""

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import json
import os

class Dashboard:
    def __init__(self):
        self.progress_file = "data/progress.json"
        self.users_file = "data/users.json"
        
    def show_dashboard(self, user_data):
        """
        Display personalized dashboard based on user type
        
        Args:
            user_data: Dictionary containing user information
        """
        user_type = user_data.get('user_type', 'student')
        email = user_data.get('email', '')
        
        # Welcome message with user name
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; 
                    border-radius: 10px; 
                    color: white;
                    margin-bottom: 2rem;'>
            <h1 style='margin: 0;'>👋 Welcome back, {user_data.get('name', 'User')}!</h1>
            <p style='margin: 0.5rem 0 0 0; opacity: 0.9;'>
                {self._get_welcome_message(user_type)}
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Load progress data
        progress_data = self._load_progress(email, user_type)
        
        # Display user-specific dashboard
        if user_type == "student":
            self._show_student_dashboard(progress_data)
        elif user_type == "teacher":
            self._show_teacher_dashboard(progress_data)
        elif user_type == "professional":
            self._show_professional_dashboard(progress_data)
        elif user_type == "business":
            self._show_business_dashboard(progress_data)
        
        # Quick actions
        self._show_quick_actions(user_type)
        
        # Recent activity
        self._show_recent_activity(progress_data)
    
    def _get_welcome_message(self, user_type):
        """Get personalized welcome message based on user type"""
        messages = {
            "student": "Continue your learning journey! Complete chapters and practice MCQs to master your subjects.",
            "teacher": "Empower your teaching with AI! Create lessons, assessments, and personalized feedback.",
            "professional": "Advance your career with role-specific AI skills. Complete modules and track your progress.",
            "business": "Transform your business with AI! Adopt tools and automations for growth."
        }
        return messages.get(user_type, "Welcome to AI Shiksha!")
    
    def _load_progress(self, email, user_type):
        """Load user progress from JSON file"""
        try:
            with open(self.progress_file, "r") as f:
                all_progress = json.load(f)
                key = f"{user_type}_progress"
                return all_progress.get(key, {}).get(email, {})
        except:
            return {}
    
    def _show_student_dashboard(self, progress):
        """Display student dashboard"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            completed = progress.get('completed_chapters', 0)
            total = progress.get('total_chapters', 20)
            st.metric("📚 Chapters", f"{completed}/{total}")
        
        with col2:
            mcq_avg = progress.get('mcq_average', 0)
            st.metric("🎯 MCQ Score", f"{mcq_avg:.1f}%")
        
        with col3:
            study_time = progress.get('study_time', 0)
            st.metric("⏱️ Study Time", f"{study_time}h")
        
        with col4:
            streak = progress.get('streak_days', 0)
            st.metric("🔥 Streak", f"{streak} days")
        
        # Weekly progress chart
        st.subheader("📊 Weekly Progress")
        weekly_data = progress.get('weekly_activity', {})
        if weekly_data:
            dates = []
            values = []
            for week, days in weekly_data.items():
                for day, value in days.items():
                    dates.append(f"{week} {day}")
                    values.append(value)
            
            if dates and values:
                df = pd.DataFrame({
                    'Day': dates[-7:],
                    'Activity': values[-7:]
                })
                st.bar_chart(df.set_index('Day'))
        else:
            st.info("Start learning to see your progress chart!")
    
    def _show_teacher_dashboard(self, progress):
        """Display teacher dashboard"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            lesson_plans = progress.get('lesson_plans', 0)
            st.metric("📝 Lesson Plans", lesson_plans)
        
        with col2:
            assessments = progress.get('assessments', 0)
            st.metric("📊 Assessments", assessments)
        
        with col3:
            feedback = progress.get('feedback_messages', 0)
            st.metric("💬 Feedback Sent", feedback)
        
        with col4:
            tools = len(progress.get('tools_used', {}))
            st.metric("🛠️ Tools Used", tools)
        
        # Tool usage breakdown
        st.subheader("🛠️ AI Tool Adoption")
        tools_used = progress.get('tools_used', {})
        if tools_used:
            for tool, count in tools_used.items():
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"**{tool}**")
                with col2:
                    st.write(f"{count} uses")
                st.progress(min(count / 20, 1.0))
        else:
            st.info("Start using AI tools to see adoption metrics here!")
    
    def _show_professional_dashboard(self, progress):
        """Display professional dashboard"""
        col1, col2, col3 = st.columns(3)
        
        with col1:
            courses = progress.get('courses_completed', 0)
            st.metric("📚 Courses", courses)
        
        with col2:
            skill_level = progress.get('skill_level', 0)
            st.metric("🎯 Skill Level", f"{skill_level}%")
        
        with col3:
            nudges = progress.get('nudges_completed', 0)
            total_nudges = progress.get('nudges_received', 0)
            st.metric("✅ Nudges", f"{nudges}/{total_nudges}")
        
        # Skill breakdown
        st.subheader("📊 Skill Breakdown")
        skills = progress.get('assessment_scores', {})
        if skills:
            for skill, score in skills.items():
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**{skill}**")
                with col2:
                    st.write(f"{score}%")
                st.progress(score / 100)
    
    def _show_business_dashboard(self, progress):
        """Display business dashboard"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            tools = progress.get('tools_adopted', 0)
            st.metric("🛠️ Tools Adopted", tools)
        
        with col2:
            automations = progress.get('automations', 0)
            st.metric("⚡ Automations", automations)
        
        with col3:
            roi = progress.get('roi', 0)
            st.metric("📈 ROI", f"{roi}%")
        
        with col4:
            metrics = progress.get('business_metrics', {})
            satisfaction = metrics.get('customer_satisfaction', 0)
            st.metric("⭐ Satisfaction", f"{satisfaction}%")
        
        # Business metrics
        st.subheader("📊 Business Performance")
        metrics = progress.get('business_metrics', {})
        if metrics:
            for metric, value in metrics.items():
                col1, col2 = st.columns([2, 1])
                with col1:
                    st.write(f"**{metric.replace('_', ' ').title()}**")
                with col2:
                    st.write(f"{value}%")
                st.progress(value / 100)
    
    def _show_quick_actions(self, user_type):
        """Display quick action buttons"""
        st.markdown("---")
        st.subheader("⚡ Quick Actions")
        
        actions = {
            "student": [
                ("📚 Continue Learning", "Continue where you left off"),
                ("📝 Practice MCQ", "Test your knowledge"),
                ("📅 View Study Plan", "Check your schedule")
            ],
            "teacher": [
                ("📝 Create Lesson Plan", "Use AI to plan lessons"),
                ("📊 Generate Assessment", "Create tests and quizzes"),
                ("💬 Send Feedback", "Provide student feedback")
            ],
            "professional": [
                ("🎓 Start Course", "Begin a new module"),
                ("📊 Skill Assessment", "Test your skills"),
                ("📈 Track Progress", "View your learning path")
            ],
            "business": [
                ("🛠️ Explore Tools", "Discover AI business tools"),
                ("⚡ Setup Automation", "Automate workflows"),
                ("📊 View Analytics", "Check business metrics")
            ]
        }
        
        cols = st.columns(len(actions.get(user_type, [])))
        for idx, (label, tooltip) in enumerate(actions.get(user_type, [])):
            with cols[idx]:
                if st.button(label, help=tooltip, use_container_width=True):
                    st.info(f"Action: {label}")
    
    def _show_recent_activity(self, progress):
        """Display recent activity"""
        st.markdown("---")
        st.subheader("📋 Recent Activity")
        
        last_active = progress.get('last_active')
        if last_active:
            try:
                last_active_date = datetime.fromisoformat(last_active)
                days_ago = (datetime.now() - last_active_date).days
                if days_ago == 0:
                    st.success("✅ Active today!")
                elif days_ago == 1:
                    st.info("📆 Last active yesterday")
                else:
                    st.info(f"📆 Last active {days_ago} days ago")
            except:
                st.info("Welcome! Start learning to track your activity.")
        else:
            st.info("No activity recorded yet. Start your learning journey!")
        
        # Show next recommended action
        self._show_recommendation(progress)
    
    def _show_recommendation(self, progress):
        """Show AI-powered recommendation"""
        st.info("💡 **AI Recommendation:**")
        
        # Simple recommendation logic
        if progress.get('mcq_average', 0) < 60:
            st.write("Practice more MCQs to improve your scores!")
        elif progress.get('completed_chapters', 0) < 5:
            st.write("Complete more chapters to advance your learning!")
        elif progress.get('study_time', 0) < 10:
            st.write("Increase your study time to see faster progress!")
        else:
            st.write("🌟 You're doing great! Keep up the excellent work!")
