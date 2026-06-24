"""
Authentication Module for AI Shiksha
Handles user registration, login, and session management
"""

import streamlit as st
import json
import hashlib
import os
import re
from datetime import datetime
from typing import Dict, Optional, Tuple

class AuthManager:
    def __init__(self):
        self.users_file = "data/users.json"
        self.ensure_data_directory()
        
    def ensure_data_directory(self):
        """Ensure data directory and users file exist"""
        if not os.path.exists("data"):
            os.makedirs("data")
        if not os.path.exists(self.users_file):
            with open(self.users_file, "w") as f:
                json.dump({}, f)
    
    def hash_password(self, password: str) -> str:
        """
        Hash password using SHA-256
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password string
        """
        return hashlib.sha256(password.encode()).hexdigest()
    
    def load_users(self) -> Dict:
        """
        Load users from JSON file
        
        Returns:
            Dictionary of users
        """
        try:
            with open(self.users_file, "r", encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
    
    def save_users(self, users: Dict) -> bool:
        """
        Save users to JSON file
        
        Args:
            users: Dictionary of users
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with open(self.users_file, "w", encoding='utf-8') as f:
                json.dump(users, f, indent=2, ensure_ascii=False)
            return True
        except Exception:
            return False
    
    def validate_email(self, email: str) -> bool:
        """
        Validate email format
        
        Args:
            email: Email string to validate
            
        Returns:
            True if valid, False otherwise
        """
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_phone(self, phone: str) -> bool:
        """
        Validate Bangladeshi phone number format
        
        Args:
            phone: Phone number string to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Bangladeshi phone numbers: +8801XXXXXXXXX or 01XXXXXXXXX
        pattern = r'^(?:\+8801|01)[0-9]{9}$'
        return bool(re.match(pattern, phone))
    
    def validate_password(self, password: str) -> Tuple[bool, str]:
        """
        Validate password strength
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, message)
        """
        if len(password) < 6:
            return False, "Password must be at least 6 characters long"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number"
        return True, "Password is valid"
    
    def register_user(
        self,
        name: str,
        email: str,
        phone: str,
        password: str,
        user_type: str,
        preferences: Optional[Dict] = None
    ) -> Tuple[bool, str]:
        """
        Register a new user
        
        Args:
            name: Full name
            email: Email address
            phone: Phone number
            password: Password
            user_type: Type of user (student, teacher, professional, business)
            preferences: User preferences (optional)
            
        Returns:
            Tuple of (success, message)
        """
        # Validate inputs
        if not name or not email or not phone or not password:
            return False, "Please fill in all required fields"
        
        if not self.validate_email(email):
            return False, "Please enter a valid email address"
        
        if not self.validate_phone(phone):
            return False, "Please enter a valid Bangladeshi phone number (e.g., 01712345678 or +8801712345678)"
        
        is_valid, password_msg = self.validate_password(password)
        if not is_valid:
            return False, password_msg
        
        if user_type not in ["student", "teacher", "professional", "business"]:
            return False, "Invalid user type selected"
        
        # Check if user already exists
        users = self.load_users()
        if email in users:
            return False, "A user with this email already exists"
        
        # Create new user
        new_user = {
            "name": name,
            "email": email,
            "phone": phone,
            "password": self.hash_password(password),
            "user_type": user_type,
            "registered_at": datetime.now().isoformat(),
            "last_login": None,
            "is_active": True,
            "progress": {
                "completed_chapters": 0,
                "total_chapters": 20,
                "mcq_average": 0,
                "study_time": 0,
                "streak_days": 0,
                "last_active": None
            },
            "preferences": preferences or {
                "daily_study_time": 30,
                "learning_pace": "Beginner",
                "language": "Bilingual",
                "notification_preferences": {
                    "email": True,
                    "sms": False
                }
            }
        }
        
        # Add user type specific fields
        if user_type == "student":
            new_user["progress"]["subjects"] = {
                "mathematics": {"progress": 0, "score": 0},
                "science": {"progress": 0, "score": 0},
                "english": {"progress": 0, "score": 0}
            }
        elif user_type == "teacher":
            new_user["progress"]["tools_used"] = {}
            new_user["progress"]["lesson_plans"] = 0
            new_user["progress"]["assessments"] = 0
            new_user["progress"]["feedback_messages"] = 0
        elif user_type == "professional":
            new_user["progress"]["courses_completed"] = 0
            new_user["progress"]["skill_level"] = 0
            new_user["progress"]["role"] = "Not specified"
            new_user["progress"]["assessment_scores"] = {}
        elif user_type == "business":
            new_user["progress"]["tools_adopted"] = 0
            new_user["progress"]["automations"] = 0
            new_user["progress"]["roi"] = 0
            new_user["progress"]["business_metrics"] = {
                "customer_satisfaction": 0,
                "operational_efficiency": 0,
                "cost_reduction": 0
            }
        
        # Save user
        users[email] = new_user
        if self.save_users(users):
            return True, "Registration successful! Please login."
        else:
            return False, "Registration failed. Please try again."
    
    def login_user(self, email: str, password: str) -> Tuple[bool, str, Optional[Dict]]:
        """
        Login a user
        
        Args:
            email: Email address
            password: Password
            
        Returns:
            Tuple of (success, message, user_data)
        """
        if not email or not password:
            return False, "Please enter email and password", None
        
        users = self.load_users()
        
        if email not in users:
            return False, "Invalid email or password", None
        
        user = users[email]
        
        # Check if user is active
        if not user.get('is_active', True):
            return False, "Your account has been deactivated. Please contact support.", None
        
        # Verify password
        if user["password"] != self.hash_password(password):
            return False, "Invalid email or password", None
        
        # Update last login
        user["last_login"] = datetime.now().isoformat()
        users[email] = user
        self.save_users(users)
        
        # Set session state
        st.session_state.authenticated = True
        st.session_state.user_type = user["user_type"]
        st.session_state.user_data = user
        st.session_state.user_data["email"] = email
        
        return True, "Login successful!", user
    
    def logout_user(self):
        """Logout current user"""
        st.session_state.authenticated = False
        st.session_state.user_type = None
        st.session_state.user_data = {}
        
        # Clear any other session variables
        for key in list(st.session_state.keys()):
            if key not in ['authenticated', 'user_type', 'user_data']:
                del st.session_state[key]
    
    def update_user_profile(self, email: str, updates: Dict) -> Tuple[bool, str]:
        """
        Update user profile information
        
        Args:
            email: User email
            updates: Dictionary of updates
            
        Returns:
            Tuple of (success, message)
        """
        users = self.load_users()
        
        if email not in users:
            return False, "User not found"
        
        # Update allowed fields
        allowed_fields = ['name', 'phone', 'preferences']
        for field, value in updates.items():
            if field in allowed_fields:
                users[email][field] = value
        
        if self.save_users(users):
            # Update session data
            if st.session_state.user_data.get('email') == email:
                st.session_state.user_data.update(updates)
            return True, "Profile updated successfully!"
        else:
            return False, "Failed to update profile"
    
    def update_progress(self, email: str, progress_updates: Dict) -> Tuple[bool, str]:
        """
        Update user progress
        
        Args:
            email: User email
            progress_updates: Dictionary of progress updates
            
        Returns:
            Tuple of (success, message)
        """
        users = self.load_users()
        
        if email not in users:
            return False, "User not found"
        
        user = users[email]
        for key, value in progress_updates.items():
            if key in user['progress']:
                if isinstance(user['progress'][key], dict):
                    user['progress'][key].update(value)
                else:
                    user['progress'][key] = value
        
        user['progress']['last_active'] = datetime.now().isoformat()
        users[email] = user
        
        if self.save_users(users):
            return True, "Progress updated successfully!"
        else:
            return False, "Failed to update progress"
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """
        Get user data by email
        
        Args:
            email: User email
            
        Returns:
            User data dictionary or None
        """
        users = self.load_users()
        return users.get(email)
    
    def get_all_users(self) -> Dict:
        """
        Get all users
        
        Returns:
            Dictionary of all users
        """
        return self.load_users()
    
    def delete_user(self, email: str) -> Tuple[bool, str]:
        """
        Delete a user account
        
        Args:
            email: User email
            
        Returns:
            Tuple of (success, message)
        """
        users = self.load_users()
        
        if email not in users:
            return False, "User not found"
        
        del users[email]
        
        if self.save_users(users):
            return True, "User deleted successfully!"
        else:
            return False, "Failed to delete user"
    
    def register_page(self):
        """Display registration page"""
        st.markdown("""
        <h2 style='color: #1f77b4; text-align: center; margin-bottom: 2rem;'>
            📝 Register for AI Shiksha
        </h2>
        """, unsafe_allow_html=True)
        
        with st.form("register_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input(
                    "Full Name *",
                    placeholder="Enter your full name",
                    help="Your full name as it appears on official documents"
                )
                
                email = st.text_input(
                    "Email *",
                    placeholder="Enter your email address",
                    help="We'll send important notifications to this email"
                )
                
                phone = st.text_input(
                    "Phone Number *",
                    placeholder="01XXXXXXXXX or +8801XXXXXXXXX",
                    help="Enter a valid Bangladeshi phone number"
                )
            
            with col2:
                password = st.text_input(
                    "Password *",
                    type="password",
                    placeholder="Enter a strong password",
                    help="At least 6 characters with uppercase, lowercase, and numbers"
                )
                
                confirm_password = st.text_input(
                    "Confirm Password *",
                    type="password",
                    placeholder="Re-enter your password"
                )
                
                user_type = st.selectbox(
                    "I am a: *",
                    options=[
                        ("Student", "student"),
                        ("Teacher", "teacher"),
                        ("Professional", "professional"),
                        ("Business Owner", "business")
                    ],
                    format_func=lambda x: x[0],
                    help="Select the role that best describes you"
                )
            
            # Additional fields based on user type
            if user_type[1] == "student":
                education_level = st.selectbox(
                    "Education Level",
                    ["Secondary School", "Higher Secondary", "University", "Other"]
                )
                st.caption("🎓 We'll customize your learning path based on your education level")
            
            elif user_type[1] == "teacher":
                teaching_level = st.selectbox(
                    "Teaching Level",
                    ["Primary School", "Secondary School", "Higher Secondary", "University"]
                )
                subjects_taught = st.text_input(
                    "Subjects Taught",
                    placeholder="e.g., Mathematics, Science, English"
                )
                st.caption("👨‍🏫 We'll provide AI tools tailored to your teaching needs")
            
            elif user_type[1] == "professional":
                profession = st.selectbox(
                    "Profession",
                    ["Healthcare", "Finance", "Marketing", "Legal", "Technology", "Other"]
                )
                experience_years = st.number_input(
                    "Years of Experience",
                    min_value=0,
                    max_value=50,
                    value=0
                )
                st.caption("💼 We'll provide role-specific AI training for your profession")
            
            elif user_type[1] == "business":
                business_size = st.selectbox(
                    "Business Size",
                    ["Solo", "2-10 employees", "11-50 employees", "51+ employees"]
                )
                business_type = st.text_input(
                    "Business Industry",
                    placeholder="e.g., Retail, Healthcare, Technology"
                )
                st.caption("🏢 We'll suggest AI tools and automation for your business")
            
            # Terms and conditions
            st.markdown("---")
            agree_terms = st.checkbox(
                "I agree to the Terms of Service and Privacy Policy *",
                help="You must agree to the terms to register"
            )
            
            submit = st.form_submit_button("🚀 Create Account", use_container_width=True)
            
            if submit:
                # Validate all required fields
                if not all([name, email, phone, password, confirm_password]):
                    st.error("Please fill in all required fields marked with *")
                    return
                
                if password != confirm_password:
                    st.error("Passwords do not match")
                    return
                
                if not agree_terms:
                    st.error("Please agree to the Terms of Service and Privacy Policy")
                    return
                
                # Register user
                success, message = self.register_user(
                    name=name,
                    email=email,
                    phone=phone,
                    password=password,
                    user_type=user_type[1]
                )
                
                if success:
                    st.success(message)
                    st.balloons()
                    st.info("🎉 You can now login with your credentials!")
                    
                    # Show login button
                    if st.button("Go to Login"):
                        st.session_state.page = "login"
                        st.rerun()
                else:
                    st.error(message)
        
        # Login link for existing users
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <p style='text-align: center;'>
                Already have an account? 
                <a href='#' onclick='window.location.reload();'>Login here</a>
            </p>
            """, unsafe_allow_html=True)
            
            if st.button("⬅️ Back to Login", use_container_width=True):
                st.session_state.page = "login"
                st.rerun()
    
    def login_page(self):
        """Display login page"""
        st.markdown("""
        <h2 style='color: #1f77b4; text-align: center; margin-bottom: 2rem;'>
            🔐 Login to AI Shiksha
        </h2>
        """, unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input(
                "Email *",
                placeholder="Enter your registered email",
                help="Use the email you registered with"
            )
            
            password = st.text_input(
                "Password *",
                type="password",
                placeholder="Enter your password",
                help="Enter your account password"
            )
            
            col1, col2 = st.columns([1, 1])
            with col1:
                remember_me = st.checkbox("Remember me", value=False)
            with col2:
                st.markdown("[Forgot Password?](#)")
            
            submit = st.form_submit_button("🔑 Login", use_container_width=True)
            
            if submit:
                if not email or not password:
                    st.error("Please enter both email and password")
                    return
                
                success, message, user_data = self.login_user(email, password)
                
                if success:
                    st.success(message)
                    st.balloons()
                    st.rerun()
                else:
                    st.error(message)
        
        # Registration link for new users
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <p style='text-align: center;'>
                Don't have an account? 
                <a href='#' onclick='window.location.reload();'>Register here</a>
            </p>
            """, unsafe_allow_html=True)
            
            if st.button("📝 Create New Account", use_container_width=True):
                st.session_state.page = "register"
                st.rerun()
    
    def logout(self):
        """Logout user from the application"""
        self.logout_user()
        st.success("You have been logged out successfully!")
        st.rerun()
    
    def check_session(self) -> bool:
        """
        Check if user session is valid
        
        Returns:
            True if authenticated, False otherwise
        """
        if not st.session_state.get('authenticated', False):
            return False
        
        # Verify user still exists in database
        email = st.session_state.user_data.get('email')
        if email:
            user = self.get_user_by_email(email)
            if not user:
                self.logout_user()
                return False
            
            # Update session data with latest user data
            st.session_state.user_data = user
        
        return True
    
    def require_auth(self):
        """
        Decorator-like function to require authentication
        Redirects to login if not authenticated
        """
        if not self.check_session():
            st.warning("⚠️ Please login to access this page")
            self.login_page()
            st.stop()
