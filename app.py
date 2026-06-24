# app.py - Main Application Entry Point
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

# Initialize modules
auth_manager = AuthManager()
dashboard = Dashboard()
student_module = StudentModule()
teacher_module = TeacherModule()
professional_module = ProfessionalModule()
business_module = BusinessModule()
learning_agent = LearningAgent()

# Sidebar navigation
def sidebar_navigation():
    st.sidebar.image("https://via.placeholder.com/150x50?text=AI+Shiksha", use_column_width=True)
    st.sidebar.title("AI Shiksha")
    st.sidebar.markdown("---")
    
    if not st.session_state.authenticated:
        menu = ["Home", "Login", "Register"]
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
        
        menu.append("Logout")
        choice = st.sidebar.selectbox("Navigation", menu)
        return choice

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
    
    # Navigation
    choice = sidebar_navigation()
    
    # Authentication pages
    if not st.session_state.authenticated:
        if choice == "Home" or st.session_state.page == "home":
            st.info("Welcome to AI Shiksha! Please login or register to start your AI learning journey.")
            
        elif choice == "Login" or st.session_state.page == "login":
            auth_manager.login_page()
            
        elif choice == "Register" or st.session_state.page == "register":
            auth_manager.register_page()
    
    else:
        # Authenticated user pages
        if choice == "Dashboard":
            dashboard.show_dashboard(st.session_state.user_data)
            
        elif choice == "Learning Path":
            if st.session_state.user_type == "student":
                student_module.show_learning_path()
            elif st.session_state.user_type == "teacher":
                teacher_module.show_learning_path()
            elif st.session_state.user_type == "professional":
                professional_module.show_learning_path()
            elif st.session_state.user_type == "business":
                business_module.show_learning_path()
                
        elif choice == "Progress":
            learning_agent.show_progress()
            
        elif choice == "Subjects" and st.session_state.user_type == "student":
            student_module.show_subjects()
            
        elif choice == "MCQ Practice" and st.session_state.user_type == "student":
            student_module.show_mcq_practice()
            
        elif choice == "Study Plan" and st.session_state.user_type == "student":
            student_module.show_study_plan()
            
        elif choice == "Lesson Planning" and st.session_state.user_type == "teacher":
            teacher_module.show_lesson_planning()
            
        elif choice == "Assessment" and st.session_state.user_type == "teacher":
            teacher_module.show_assessment()
            
        elif choice == "Student Feedback" and st.session_state.user_type == "teacher":
            teacher_module.show_feedback()
            
        elif choice == "Role-specific Training" and st.session_state.user_type == "professional":
            professional_module.show_training()
            
        elif choice == "Skill Assessment" and st.session_state.user_type == "professional":
            professional_module.show_skill_assessment()
            
        elif choice == "Business Tools" and st.session_state.user_type == "business":
            business_module.show_tools()
            
        elif choice == "Automation" and st.session_state.user_type == "business":
            business_module.show_automation()
            
        elif choice == "Settings":
            show_settings()
            
        elif choice == "Logout":
            auth_manager.logout()

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
