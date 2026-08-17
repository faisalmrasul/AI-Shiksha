# app.py - AI Shiksha Global Platform with Universal Core + Local Overlay Architecture
# Built for global scalability with country-specific curriculum overlays

import streamlit as st
import json
import os
import random
import pandas as pd
from datetime import datetime
import hashlib
import time

# ==================== PAGE CONFIG ====================
st.set_page_config(
    page_title="AI Shiksha - Universal Core + Local Overlay",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================== CUSTOM CSS ====================
def apply_custom_css():
    st.markdown("""
    <style>
    /* Main container */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
    .stButton > button:disabled {
        opacity: 0.5;
        cursor: not-allowed;
    }
    
    /* Badge styling */
    .country-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
        margin: 4px;
        font-size: 0.8rem;
    }
    .achievement-badge {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        display: inline-block;
        margin: 4px;
        animation: pulse 2s infinite;
    }
    
    /* Card containers */
    .universal-core {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
    }
    .local-overlay {
        background: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #f5576c;
    }
    .metric-card {
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    
    /* Animations */
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Success/Error messages */
    .success-box {
        background: #d4edda;
        color: #155724;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #28a745;
    }
    .error-box {
        background: #f8d7da;
        color: #721c24;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #dc3545;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .stButton > button {
            padding: 8px 16px;
            font-size: 0.9rem;
        }
        .metric-card {
            padding: 10px;
        }
    }
    
    /* Loading spinner */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #667eea;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    /* Context input styling */
    .context-input {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin: 10px 0;
    }
    .context-input textarea {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #ced4da;
        padding: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# ==================== SESSION STATE MANAGEMENT ====================

def init_session_state():
    """Initialize all session state variables"""
    defaults = {
        'user_role': None,
        'country_code': 'kenya',
        'student_score': 54,
        'completed_lessons': [],
        'achievements': [],
        'streak': 0,
        'weak_areas': [],
        'domain': 'business',
        'business_type': 'retail',
        'preferred_language': 'English',
        'question_history': [],
        'last_activity': datetime.now().isoformat(),
        'session_start': datetime.now().isoformat(),
        'total_questions_answered': 0,
        'correct_answers': 0,
        'lesson_generation_count': 0,
        'workflow_generation_count': 0,
        # Context storage for various engines
        'student_context': {},
        'teacher_context': {},
        'professional_context': {},
        'sme_context': {},
        'generated_plans': [],
        'generated_workflows': [],
        'generated_automations': []
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ==================== UNIVERSAL CORE ENGINE ====================

class UniversalCore:
    """Portable core curriculum that works across all education systems"""
    
    # Universal subjects that exist in every education system
    UNIVERSAL_SUBJECTS = {
        'mathematics': {
            'topics': ['Arithmetic', 'Algebra', 'Geometry', 'Statistics', 'Calculus'],
            'skills': ['Problem Solving', 'Logical Reasoning', 'Pattern Recognition']
        },
        'english_language': {
            'topics': ['Reading', 'Writing', 'Speaking', 'Listening', 'Grammar'],
            'skills': ['Communication', 'Critical Analysis', 'Creative Expression']
        },
        'basic_science': {
            'topics': ['Biology', 'Chemistry', 'Physics', 'Earth Science'],
            'skills': ['Scientific Method', 'Observation', 'Experimentation']
        },
        'geography': {
            'topics': ['Physical Geography', 'Human Geography', 'Map Skills', 'Climate'],
            'skills': ['Spatial Awareness', 'Cultural Understanding', 'Environmental Awareness']
        },
        'general_knowledge': {
            'topics': ['History', 'Current Events', 'Civics', 'Economics'],
            'skills': ['Critical Thinking', 'Awareness', 'Global Understanding']
        },
        'applied_ai': {
            'topics': ['AI Fundamentals', 'Prompt Engineering', 'Workflow Automation', 'Ethics'],
            'skills': ['AI Literacy', 'Automation', 'Problem Solving']
        }
    }
    
    # Universal competencies across all systems
    UNIVERSAL_COMPETENCIES = {
        'critical_thinking': 'Analyze, evaluate, and synthesize information',
        'communication': 'Express ideas clearly in multiple formats',
        'collaboration': 'Work effectively with others',
        'creativity': 'Generate innovative solutions',
        'digital_literacy': 'Use technology effectively and responsibly'
    }

# ==================== LOCAL OVERLAY ENGINE ====================

class LocalCurriculumOverlay:
    """Country/board-specific content overlay - no core rewrite required"""
    
    # Country-specific curriculum mappings
    CURRICULUM_OVERLAYS = {
        'kenya': {
            'code': 'KE',
            'system': 'CBC (Competency Based Curriculum)',
            'boards': ['KNEC', 'KICD'],
            'subjects': {
                'mathematics': 'Mathematics (including Financial Literacy)',
                'english_language': 'English (with Kiswahili as second language)',
                'basic_science': 'Integrated Science',
                'geography': 'Geography and Social Studies'
            },
            'national_exams': ['KCPE', 'KCSE'],
            'language': 'English/Kiswahili',
            'grade_levels': ['PP1', 'PP2', 'Grade 1-9', 'Form 1-4'],
            'currency': 'KES',
            'timezone': 'EAT'
        },
        'bangladesh': {
            'code': 'BD',
            'system': 'National Curriculum (NCTB)',
            'boards': ['Dhaka Board', 'Rajshahi Board', 'Chittagong Board', 'Barisal Board', 'Sylhet Board'],
            'subjects': {
                'mathematics': 'Mathematics (গণিত)',
                'english_language': 'English (ইংরেজি)',
                'basic_science': 'Science (বিজ্ঞান)',
                'geography': 'Geography and Environment (ভূগোল ও পরিবেশ)'
            },
            'national_exams': ['PSC', 'JSC', 'SSC', 'HSC'],
            'language': 'Bengali/English',
            'grade_levels': ['Class 1-5', 'Class 6-8', 'Class 9-10', 'Class 11-12'],
            'currency': 'BDT',
            'timezone': 'BST'
        },
        'usa': {
            'code': 'US',
            'system': 'Common Core State Standards',
            'boards': ['State-specific', 'College Board'],
            'subjects': {
                'mathematics': 'Mathematics (Common Core)',
                'english_language': 'English Language Arts',
                'basic_science': 'Science (NGSS)',
                'geography': 'Social Studies'
            },
            'national_exams': ['SAT', 'ACT', 'AP'],
            'language': 'English/Spanish',
            'grade_levels': ['K-5', '6-8', '9-12'],
            'currency': 'USD',
            'timezone': 'EST/CST/PST'
        },
        'uk': {
            'code': 'UK',
            'system': 'National Curriculum for England',
            'boards': ['AQA', 'Edexcel', 'OCR', 'WJEC'],
            'subjects': {
                'mathematics': 'Mathematics',
                'english_language': 'English',
                'basic_science': 'Science (Combined/Triple)',
                'geography': 'Geography'
            },
            'national_exams': ['GCSE', 'A-Levels'],
            'language': 'English',
            'grade_levels': ['KS1-2', 'KS3', 'KS4-5'],
            'currency': 'GBP',
            'timezone': 'GMT/BST'
        }
    }
    
    # Localized content prompts for each region
    LOCALIZED_PROMPTS = {
        'kenya': {
            'greeting': 'Jambo! Welcome to AI Shiksha Kenya 🇰🇪',
            'exam_style': 'KNEC-style examination questions with practical applications',
            'examples': 'Use examples relevant to East African context',
            'cultural_note': 'Integration of Kenyan cultural values and community-based learning'
        },
        'bangladesh': {
            'greeting': 'স্বাগতম! Welcome to AI Shiksha Bangladesh 🇧🇩',
            'exam_style': 'NCTB and board examination preparation style',
            'examples': 'Use examples relevant to Bangladeshi context',
            'cultural_note': 'Integration of Bangladeshi cultural heritage and language'
        },
        'usa': {
            'greeting': 'Welcome to AI Shiksha USA 🇺🇸',
            'exam_style': 'Common Core and standardized test preparation',
            'examples': 'Use examples relevant to American context',
            'cultural_note': 'Focus on college and career readiness'
        },
        'uk': {
            'greeting': 'Welcome to AI Shiksha UK 🇬🇧',
            'exam_style': 'GCSE and A-Level examination format',
            'examples': 'Use examples relevant to British context',
            'cultural_note': 'Focus on academic rigor and depth'
        }
    }
    
    # Country-specific local context for lesson generation
    LOCAL_CONTEXTS = {
        'kenya': {
            'culture': 'Kenyan community values, Harambee spirit, diverse ethnic groups',
            'environment': 'Savanna, wildlife, agriculture, coastal regions',
            'economy': 'Agriculture, tourism, technology (Silicon Savannah)'
        },
        'bangladesh': {
            'culture': 'Bengali heritage, language movement, diverse traditions',
            'environment': 'Delta region, rivers, monsoon climate, agriculture',
            'economy': 'Garment industry, agriculture, remittances, technology'
        },
        'usa': {
            'culture': 'Diverse immigrant nation, American Dream, individual liberty',
            'environment': 'Diverse climates, 50 states, national parks',
            'economy': "World's largest economy, innovation, technology"
        },
        'uk': {
            'culture': 'British heritage, royal tradition, multicultural society',
            'environment': 'Temperate climate, varied landscapes, historic cities',
            'economy': 'Service economy, financial hub, creative industries'
        }
    }
    
    @staticmethod
    def get_overlay(country_code):
        """Get curriculum overlay for specific country"""
        return LocalCurriculumOverlay.CURRICULUM_OVERLAYS.get(country_code, {})
    
    @staticmethod
    def get_local_context(country_code):
        """Get local context for specific country"""
        return LocalCurriculumOverlay.LOCAL_CONTEXTS.get(country_code, {})
    
    @staticmethod
    def get_localized_prompt(country_code, key):
        """Get localized prompt for specific country"""
        prompts = LocalCurriculumOverlay.LOCALIZED_PROMPTS.get(country_code, {})
        return prompts.get(key, '')
    
    @staticmethod
    def localize_question(question, country_code):
        """Localize a universal question with country-specific context"""
        localized = question.copy()
        overlay = LocalCurriculumOverlay.get_overlay(country_code)
        context = LocalCurriculumOverlay.get_local_context(country_code)
        
        if overlay and 'subjects' in overlay:
            # Map universal subject to local subject name
            for uni_sub, local_sub in overlay['subjects'].items():
                if uni_sub in question.get('subject', '').lower():
                    localized['local_subject'] = local_sub
                    break
        
        # Add local context to explanation
        if 'explanation' in localized:
            context_phrases = {
                'kenya': f" using Kenyan examples and context (agriculture, wildlife, community)",
                'bangladesh': f" using Bangladeshi examples (rivers, garment industry, Bengali culture)",
                'usa': f" using American examples (diversity, innovation, local communities)",
                'uk': f" using British examples (history, multicultural society, local context)"
            }
            localized['explanation'] += context_phrases.get(country_code, '')
        
        # Add local cultural note
        if 'socratic_hint' in localized:
            cultural_note = LocalCurriculumOverlay.get_localized_prompt(country_code, 'cultural_note')
            if cultural_note:
                localized['socratic_hint'] += f" (Cultural context: {cultural_note})"
        
        return localized
    
    @staticmethod
    def get_grade_levels(country_code):
        """Get grade levels for specific country"""
        overlay = LocalCurriculumOverlay.get_overlay(country_code)
        return overlay.get('grade_levels', ['Primary', 'Secondary'])

# ==================== CONTEXT COLLECTORS ====================

class ContextCollector:
    """Collects user context for generating personalized plans"""
    
    @staticmethod
    def collect_student_context():
        """Collect student-specific context"""
        with st.container():
            st.markdown("### 📝 Student Learning Context")
            st.markdown("Provide details to personalize your learning experience")
            
            col1, col2 = st.columns(2)
            
            with col1:
                learning_goal = st.text_area(
                    "🎯 What are your learning goals?",
                    placeholder="e.g., I want to improve my math skills, prepare for exams, or learn AI basics...",
                    height=80
                )
                
                current_level = st.select_slider(
                    "📊 Current proficiency level:",
                    options=["Beginner", "Intermediate", "Advanced", "Expert"],
                    value="Intermediate"
                )
                
                topics_interest = st.multiselect(
                    "📚 Topics you're interested in:",
                    ["Algebra", "Geometry", "Statistics", "Reading", "Writing", 
                     "Grammar", "Biology", "Chemistry", "Physics", "Geography"],
                    default=["Algebra", "Reading"]
                )
            
            with col2:
                learning_style = st.selectbox(
                    "🧠 Preferred learning style:",
                    ["Visual", "Auditory", "Reading/Writing", "Kinesthetic", "Mixed"]
                )
                
                time_available = st.slider(
                    "⏰ Time available for learning (hours/week):",
                    min_value=1,
                    max_value=20,
                    value=5
                )
                
                challenges = st.text_area(
                    "⚠️ Challenges you're facing:",
                    placeholder="e.g., Difficulty understanding concepts, lack of practice, exam anxiety...",
                    height=80
                )
            
            # Additional context
            st.markdown("#### 🎯 Specific Goals")
            short_term_goal = st.text_input(
                "Short-term goal (1 month):",
                placeholder="e.g., Pass math exam, improve writing skills..."
            )
            
            long_term_goal = st.text_input(
                "Long-term goal (6 months - 1 year):",
                placeholder="e.g., Graduate with honors, start a career in AI..."
            )
            
            # Store context
            context = {
                'learning_goal': learning_goal,
                'current_level': current_level,
                'topics_interest': topics_interest,
                'learning_style': learning_style,
                'time_available': time_available,
                'challenges': challenges,
                'short_term_goal': short_term_goal,
                'long_term_goal': long_term_goal,
                'collected_at': datetime.now().isoformat()
            }
            
            st.session_state.student_context = context
            
            if st.button("💾 Save Learning Context", key="save_student_context"):
                st.success("✅ Learning context saved successfully!")
                st.balloons()
            
            return context
    
    @staticmethod
    def collect_teacher_context():
        """Collect teacher-specific context"""
        with st.container():
            st.markdown("### 📋 Teacher Planning Context")
            st.markdown("Provide details to generate personalized lesson plans")
            
            col1, col2 = st.columns(2)
            
            with col1:
                subject_specialization = st.text_input(
                    "📚 Subject you teach:",
                    placeholder="e.g., Mathematics, Science, English..."
                )
                
                class_size = st.number_input(
                    "👥 Class size:",
                    min_value=1,
                    max_value=100,
                    value=30
                )
                
                grade_level = st.selectbox(
                    "📊 Grade level:",
                    ["PP1", "PP2", "Grade 1-3", "Grade 4-6", "Grade 7-9", 
                     "Form 1-2", "Form 3-4", "K-5", "6-8", "9-12", "KS1-2", "KS3", "KS4-5"]
                )
            
            with col2:
                curriculum_track = st.selectbox(
                    "📋 Curriculum track:",
                    ["General", "Science", "Arts", "Technology", "Business"]
                )
                
                student_needs = st.text_area(
                    "🎯 Specific student needs:",
                    placeholder="e.g., Diverse learning needs, special education, gifted students...",
                    height=80
                )
                
                resources_available = st.text_area(
                    "📚 Resources available:",
                    placeholder="e.g., Technology, textbooks, lab equipment...",
                    height=80
                )
            
            # Additional context
            st.markdown("#### 🔧 Teaching Preferences")
            teaching_style = st.selectbox(
                "👨‍🏫 Teaching style:",
                ["Traditional", "Interactive", "Project-based", "Flipped classroom", "Inquiry-based"]
            )
            
            assessment_preference = st.selectbox(
                "📝 Assessment preference:",
                ["Formative", "Summative", "Mixed", "Continuous evaluation"]
            )
            
            # Store context
            context = {
                'subject_specialization': subject_specialization,
                'class_size': class_size,
                'grade_level': grade_level,
                'curriculum_track': curriculum_track,
                'student_needs': student_needs,
                'resources_available': resources_available,
                'teaching_style': teaching_style,
                'assessment_preference': assessment_preference,
                'collected_at': datetime.now().isoformat()
            }
            
            st.session_state.teacher_context = context
            
            if st.button("💾 Save Teaching Context", key="save_teacher_context"):
                st.success("✅ Teaching context saved successfully!")
                st.balloons()
            
            return context
    
    @staticmethod
    def collect_professional_context():
        """Collect professional-specific context"""
        with st.container():
            st.markdown("### 💼 Professional Development Context")
            st.markdown("Provide details for career acceleration and workflow optimization")
            
            col1, col2 = st.columns(2)
            
            with col1:
                industry = st.selectbox(
                    "🏢 Industry:",
                    ["Technology", "Finance", "Healthcare", "Education", "Marketing", 
                     "Consulting", "Manufacturing", "Retail", "Non-profit"]
                )
                
                role = st.text_input(
                    "👔 Your role:",
                    placeholder="e.g., Data Analyst, Marketing Manager, Educator..."
                )
                
                experience_level = st.select_slider(
                    "📊 Experience level:",
                    options=["Entry", "Junior", "Mid-level", "Senior", "Executive"],
                    value="Mid-level"
                )
            
            with col2:
                skills_to_develop = st.multiselect(
                    "🔧 Skills you want to develop:",
                    ["Project Management", "Data Analysis", "Leadership", "Communication",
                     "AI/ML", "Digital Marketing", "Financial Analysis", "Strategic Planning"],
                    default=["Data Analysis", "AI/ML"]
                )
                
                career_goals = st.text_area(
                    "🎯 Career goals:",
                    placeholder="e.g., Get promoted to management, transition to new industry...",
                    height=80
                )
                
                current_challenges = st.text_area(
                    "⚠️ Current professional challenges:",
                    placeholder="e.g., Automating workflows, managing teams, upskilling...",
                    height=80
                )
            
            # Additional context
            st.markdown("#### 🚀 Professional Development Preferences")
            time_investment = st.slider(
                "⏰ Time available for professional development (hours/week):",
                min_value=1,
                max_value=20,
                value=5
            )
            
            learning_format = st.selectbox(
                "📚 Preferred learning format:",
                ["Self-paced online", "Live workshops", "Virtual conferences", "Mentorship", "Hybrid"]
            )
            
            # Store context
            context = {
                'industry': industry,
                'role': role,
                'experience_level': experience_level,
                'skills_to_develop': skills_to_develop,
                'career_goals': career_goals,
                'current_challenges': current_challenges,
                'time_investment': time_investment,
                'learning_format': learning_format,
                'collected_at': datetime.now().isoformat()
            }
            
            st.session_state.professional_context = context
            
            if st.button("💾 Save Professional Context", key="save_professional_context"):
                st.success("✅ Professional context saved successfully!")
                st.balloons()
            
            return context
    
    @staticmethod
    def collect_sme_context():
        """Collect SME-specific context"""
        with st.container():
            st.markdown("### 🏢 SME Business Growth Context")
            st.markdown("Provide details for business automation and growth strategies")
            
            col1, col2 = st.columns(2)
            
            with col1:
                business_type = st.selectbox(
                    "🏪 Business type:",
                    ["Retail", "Service", "Agriculture", "Manufacturing", "Tech", "Hospitality"]
                )
                
                business_size = st.select_slider(
                    "👥 Business size:",
                    options=["Solo", "2-5", "6-20", "21-50", "50+"],
                    value="2-5"
                )
                
                years_operating = st.number_input(
                    "📅 Years in business:",
                    min_value=1,
                    max_value=50,
                    value=3
                )
            
            with col2:
                primary_audience = st.text_input(
                    "🎯 Primary target audience:",
                    placeholder="e.g., Small businesses, students, parents..."
                )
                
                business_goals = st.text_area(
                    "🎯 Business goals:",
                    placeholder="e.g., Increase revenue, expand to new markets, improve efficiency...",
                    height=80
                )
                
                pain_points = st.text_area(
                    "⚠️ Current business pain points:",
                    placeholder="e.g., Manual processes, customer acquisition, inventory management...",
                    height=80
                )
            
            # Additional context
            st.markdown("#### 💰 Financial Context")
            annual_revenue_range = st.selectbox(
                "💰 Annual revenue range:",
                ["Under 10K", "10K-50K", "50K-200K", "200K-1M", "1M+"]
            )
            
            monthly_budget = st.number_input(
                "💳 Monthly budget for automation/tools ($):",
                min_value=0,
                max_value=10000,
                value=500
            )
            
            # Store context
            context = {
                'business_type': business_type,
                'business_size': business_size,
                'years_operating': years_operating,
                'primary_audience': primary_audience,
                'business_goals': business_goals,
                'pain_points': pain_points,
                'annual_revenue_range': annual_revenue_range,
                'monthly_budget': monthly_budget,
                'collected_at': datetime.now().isoformat()
            }
            
            st.session_state.sme_context = context
            
            if st.button("💾 Save Business Context", key="save_sme_context"):
                st.success("✅ Business context saved successfully!")
                st.balloons()
            
            return context

# ==================== ENHANCED SEGMENT ENGINES ====================

class EnhancedStudentOutcomeEngine(StudentOutcomeEngine):
    """Enhanced student engine with context-aware features"""
    
    def __init__(self, country_code='kenya'):
        super().__init__(country_code)
        self.context = st.session_state.get('student_context', {})
    
    def generate_personalized_plan(self):
        """Generate a personalized learning plan based on context"""
        context = self.context
        
        if not context:
            return None
        
        plan = {
            'title': f"Personalized Learning Plan for {context.get('current_level', 'Student')}",
            'goals': context.get('learning_goal', 'Improve academic performance'),
            'short_term_goal': context.get('short_term_goal', ''),
            'long_term_goal': context.get('long_term_goal', ''),
            'topics': context.get('topics_interest', ['General']),
            'learning_style': context.get('learning_style', 'Mixed'),
            'time_available': context.get('time_available', 5),
            'challenges': context.get('challenges', ''),
            'recommended_approach': self._generate_approach(),
            'weekly_schedule': self._generate_schedule(),
            'resources': self._generate_resources(),
            'milestones': self._generate_milestones()
        }
        
        return plan
    
    def _generate_approach(self):
        """Generate recommended learning approach"""
        learning_style = self.context.get('learning_style', 'Mixed')
        
        approaches = {
            'Visual': 'Use diagrams, charts, mind maps, and video content',
            'Auditory': 'Use podcasts, lectures, discussions, and audio materials',
            'Reading/Writing': 'Use textbooks, notes, articles, and written exercises',
            'Kinesthetic': 'Use hands-on activities, role-plays, and practical exercises',
            'Mixed': 'Combine visual, auditory, reading, and kinesthetic approaches'
        }
        
        return approaches.get(learning_style, 'Balanced approach with various methods')
    
    def _generate_schedule(self):
        """Generate weekly learning schedule"""
        hours = self.context.get('time_available', 5)
        
        schedule = {
            'weekly_hours': hours,
            'daily_hours': round(hours / 5, 1) if hours > 0 else 0,
            'recommended_session': '45 minutes per session',
            'breakdown': [
                f"{round(hours * 0.2, 1)} hours - Core concept learning",
                f"{round(hours * 0.3, 1)} hours - Practice and exercises",
                f"{round(hours * 0.2, 1)} hours - Review and revision",
                f"{round(hours * 0.3, 1)} hours - Application and projects"
            ]
        }
        
        return schedule
    
    def _generate_resources(self):
        """Generate recommended learning resources"""
        country = self.country
        topics = self.context.get('topics_interest', ['General'])
        
        resources = []
        for topic in topics:
            resources.append(f"{topic} - Localized materials for {country}")
        
        resources.extend([
            "Interactive learning modules",
            "Practice exercises with instant feedback",
            "Peer learning opportunities",
            "Progress tracking tools"
        ])
        
        return resources
    
    def _generate_milestones(self):
        """Generate learning milestones"""
        return [
            {"week": 1, "goal": "Complete diagnostic assessment", "progress": 0},
            {"week": 2, "goal": "Master core concepts", "progress": 25},
            {"week": 4, "goal": "Complete intermediate topics", "progress": 50},
            {"week": 8, "goal": "Achieve proficiency target", "progress": 75},
            {"week": 12, "goal": "Complete learning plan objectives", "progress": 100}
        ]

class EnhancedTeacherOutcomeEngine(TeacherOutcomeEngine):
    """Enhanced teacher engine with context-aware features"""
    
    def __init__(self, country_code='kenya'):
        super().__init__(country_code)
        self.context = st.session_state.get('teacher_context', {})
    
    def generate_contextual_lesson_plan(self):
        """Generate a lesson plan based on teacher context"""
        context = self.context
        
        if not context:
            return None
        
        subject = context.get('subject_specialization', 'General')
        grade = context.get('grade_level', 'Grade 7')
        
        # Generate base plan
        base_plan = self.generate_lesson_plan(subject, grade, 45)
        
        # Enhance with context
        enhanced_plan = {
            'title': f"{subject} Lesson Plan - {grade}",
            'curriculum': overlay.get('system', 'Universal'),
            'country': self.country,
            'grade_level': grade,
            'class_size': context.get('class_size', 30),
            'duration': 45,
            'teaching_style': context.get('teaching_style', 'Mixed'),
            'assessment_preference': context.get('assessment_preference', 'Mixed'),
            'objectives': self._generate_contextual_objectives(),
            'activities': self._generate_contextual_activities(),
            'assessment': self._generate_contextual_assessment(),
            'differentiation': self._generate_differentiation_strategies(),
            'resources_needed': self._generate_resource_list(),
            'time_allocation': self._generate_time_allocation()
        }
        
        return enhanced_plan
    
    def _generate_contextual_objectives(self):
        """Generate objectives based on context"""
        subject = self.context.get('subject_specialization', 'General')
        grade = self.context.get('grade_level', 'Grade 7')
        student_needs = self.context.get('student_needs', '')
        
        objectives = [
            f"Understand key concepts of {subject} for {grade} level",
            f"Apply {subject} knowledge to real-world problems",
            f"Develop critical thinking in {subject} context"
        ]
        
        if 'diverse' in student_needs.lower():
            objectives.append("Accommodate diverse learning needs with differentiated instruction")
        
        if 'gifted' in student_needs.lower():
            objectives.append("Provide extension activities for advanced learners")
        
        return objectives
    
    def _generate_contextual_activities(self):
        """Generate activities based on context"""
        teaching_style = self.context.get('teaching_style', 'Traditional')
        class_size = self.context.get('class_size', 30)
        
        activities = []
        
        if teaching_style in ['Interactive', 'Inquiry-based']:
            activities.extend([
                "Group discussion and collaborative problem-solving",
                "Hands-on activities and experiments",
                "Peer teaching and presentations"
            ])
        elif teaching_style in ['Project-based', 'Flipped classroom']:
            activities.extend([
                "Project work and independent research",
                "Student-led presentations",
                "Real-world application scenarios"
            ])
        else:
            activities.extend([
                "Direct instruction with clear explanations",
                "Guided practice with immediate feedback",
                "Independent practice and review"
            ])
        
        # Adjust for class size
        if class_size > 40:
            activities.append("Use technology for large group engagement")
        
        return activities
    
    def _generate_contextual_assessment(self):
        """Generate assessment based on context"""
        assessment_preference = self.context.get('assessment_preference', 'Mixed')
        
        assessments = {
            'Formative': ['Exit tickets', 'Quick quizzes', 'Think-pair-share', 'One-minute papers'],
            'Summative': ['Unit tests', 'Final projects', 'Oral presentations', 'Portfolios'],
            'Mixed': ['Formative checks', 'Summative assessments', 'Peer assessment'],
            'Continuous evaluation': ['Weekly quizzes', 'Observations', 'Work samples']
        }
        
        return assessments.get(assessment_preference, assessments['Mixed'])
    
    def _generate_differentiation_strategies(self):
        """Generate differentiation strategies"""
        return {
            'Visual Learners': 'Use diagrams, charts, and visual aids',
            'Auditory Learners': 'Include discussions and audio explanations',
            'Kinesthetic Learners': 'Add hands-on activities and movement',
            'Advanced Learners': 'Provide extension challenges and projects',
            'Struggling Learners': 'Offer additional support and scaffolding'
        }
    
    def _generate_resource_list(self):
        """Generate list of needed resources"""
        resources = self.context.get('resources_available', '')
        
        resource_list = [
            'Whiteboard/Projector',
            'Textbooks and reference materials',
            'Worksheets and handouts'
        ]
        
        if 'technology' in resources.lower():
            resource_list.extend(['Computers/Tablets', 'Educational software'])
        
        if 'lab' in resources.lower():
            resource_list.extend(['Lab equipment', 'Experiment materials'])
        
        return resource_list
    
    def _generate_time_allocation(self):
        """Generate time allocation for lesson"""
        return {
            'Introduction': '5-10 minutes',
            'Main Activity': '20-25 minutes',
            'Group Work': '10-15 minutes',
            'Assessment': '5-10 minutes',
            'Closure': '5 minutes'
        }

class EnhancedProfessionalOutcomeEngine(ProfessionalOutcomeEngine):
    """Enhanced professional engine with context-aware features"""
    
    def __init__(self, domain='business', country_code='kenya'):
        super().__init__(domain, country_code)
        self.context = st.session_state.get('professional_context', {})
    
    def generate_contextual_workflow(self, task_type):
        """Generate workflow based on professional context"""
