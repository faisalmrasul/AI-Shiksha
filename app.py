# app.py - AI Shiksha Global Platform with Universal Core + Local Overlay Architecture
# Built for global scalability with country-specific curriculum overlays

import streamlit as st
import json
import os
import random
import pandas as pd
from datetime import datetime
import hashlib

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
    
    # Country-specific curriculum mappings (USA, UK, Bangladesh, Kenya only)
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
            'economy': 'World\'s largest economy, innovation, technology'
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

# ==================== SEGMENT-SPECIFIC OUTCOME ENGINES ====================

class StudentOutcomeEngine:
    """Student - Grade & Exam Outcomes Engine"""
    
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.context = LocalCurriculumOverlay.get_local_context(country_code)
    
    def get_adaptive_questions(self, subject, difficulty='medium'):
        """Get adaptive questions based on student performance"""
        questions = {
            'easy': [
                {
                    'id': 1,
                    'subject': subject,
                    'question': 'What is 5 + 7?',
                    'options': ['10', '11', '12', '13'],
                    'correct': '12',
                    'explanation': '5 + 7 = 12',
                    'socratic_hint': 'Count from 5: 6,7,8,9,10,11,12'
                }
            ],
            'medium': [
                {
                    'id': 2,
                    'subject': subject,
                    'question': 'What is 15 × 8?',
                    'options': ['100', '120', '130', '150'],
                    'correct': '120',
                    'explanation': '15 × 8 = 120 (15 × 10 - 15 × 2 = 150 - 30 = 120)',
                    'socratic_hint': 'Break it down: 15 × 10 = 150, then subtract 15 × 2 = 30'
                }
            ],
            'hard': [
                {
                    'id': 3,
                    'subject': subject,
                    'question': 'If 3x + 7 = 22, what is x?',
                    'options': ['3', '5', '7', '9'],
                    'correct': '5',
                    'explanation': '3x = 22 - 7 = 15, x = 15/3 = 5',
                    'socratic_hint': 'First, isolate the term with x'
                }
            ]
        }
        
        # Localize the questions
        localized = []
        for q in questions.get(difficulty, []):
            q['country'] = self.country
            q['exam_style'] = self.overlay.get('national_exams', ['local'])[0]
            q['local_context'] = self.context
            localized.append(LocalCurriculumOverlay.localize_question(q, self.country))
        
        return localized
    
    def track_progress(self, user_data):
        """Track and visualize student progress"""
        progress_metrics = {
            'current_score': user_data.get('score', 0),
            'streak': user_data.get('streak', 0),
            'topics_mastered': user_data.get('mastered', []),
            'areas_to_improve': user_data.get('weak_areas', []),
            'projected_grade': self._calculate_projected_grade(user_data),
            'grade_level': self.overlay.get('grade_levels', ['Unknown'])[0]
        }
        return progress_metrics
    
    def _calculate_projected_grade(self, user_data):
        """Calculate projected grade based on performance"""
        score = user_data.get('score', 0)
        
        # Country-specific grading scales
        grading_scales = {
            'kenya': {90: 'A (Excellent)', 75: 'B (Good)', 60: 'C (Satisfactory)', 45: 'D (Needs Improvement)', 0: 'E (Remedial)'},
            'bangladesh': {80: 'A+ (Excellent)', 70: 'A (Good)', 60: 'A- (Satisfactory)', 50: 'B (Average)', 0: 'C (Needs Improvement)'},
            'usa': {90: 'A', 80: 'B', 70: 'C', 60: 'D', 0: 'F'},
            'uk': {70: 'A (First Class)', 60: 'B (Upper Second)', 50: 'C (Lower Second)', 40: 'D (Third)', 0: 'E (Fail)'}
        }
        
        scale = grading_scales.get(self.country, {90: 'A', 75: 'B', 60: 'C', 45: 'D', 0: 'E'})
        
        for threshold, grade in sorted(scale.items(), reverse=True):
            if score >= threshold:
                return grade
        return 'Needs Assessment'

class TeacherOutcomeEngine:
    """Teacher - Hours-Saved Engine"""
    
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.context = LocalCurriculumOverlay.get_local_context(country_code)
    
    def generate_lesson_plan(self, subject, grade, duration, curriculum='universal'):
        """Generate lesson plan with local curriculum overlay"""
        overlay = self.overlay
        context = self.context
        
        plan = {
            'title': f"{subject} Lesson - {grade}",
            'curriculum': overlay.get('system', 'Universal'),
            'country': self.country,
            'duration': duration,
            'objectives': self._generate_objectives(subject, grade),
            'activities': self._generate_activities(subject, duration),
            'assessment': self._generate_assessment(subject)
        }
        
        # Add local context
        if overlay:
            plan['local_context'] = f"Aligned with {overlay.get('system')} ({overlay.get('code')})"
            plan['language_support'] = f"Available in {overlay.get('language', 'English')}"
            plan['cultural_context'] = context
        
        return plan
    
    def _generate_objectives(self, subject, grade):
        """Generate learning objectives with local context"""
        objectives = [
            f"Understand key concepts of {subject} at {grade} level",
            f"Apply {subject} knowledge to real-world problems",
            f"Develop critical thinking in {subject} context"
        ]
        
        # Add local objectives based on country
        if self.country == 'kenya':
            objectives.extend([
                "Demonstrate competency-based learning outcomes",
                "Integrate Kenyan community values in learning"
            ])
        elif self.country == 'bangladesh':
            objectives.extend([
                "Develop skills aligned with Bangladesh National Curriculum",
                "Apply learning to Bengali language and cultural context"
            ])
        elif self.country == 'usa':
            objectives.extend([
                "Meet Common Core State Standards",
                "Develop college and career readiness skills"
            ])
        elif self.country == 'uk':
            objectives.extend([
                "Achieve National Curriculum objectives",
                "Develop rigorous academic understanding"
            ])
        
        return objectives
    
    def _generate_activities(self, subject, duration):
        """Generate lesson activities with local context"""
        activities = []
        time_slots = []
        
        # Split duration into segments
        if duration <= 30:
            time_slots = [10, 10, 10]
        elif duration <= 45:
            time_slots = [15, 20, 10]
        else:
            time_slots = [15, 30, 15]
        
        # Add local context to activities
        local_examples = {
            'kenya': 'using local examples from Kenyan agriculture, wildlife, and community',
            'bangladesh': 'using local examples from Bangladeshi rivers, culture, and garment industry',
            'usa': 'using local examples from American communities and innovation',
            'uk': 'using local examples from British history and multicultural society'
        }
        
        example_note = local_examples.get(self.country, 'using local examples')
        
        activities = [
            f"Warm-up (0-{time_slots[0]} min): Introduction to {subject} {example_note}",
            f"Main Activity ({time_slots[0]}-{time_slots[0]+time_slots[1]} min): Interactive learning session with group work",
            f"Closure ({time_slots[0]+time_slots[1]}-{duration} min): Review and Q&A with local context application"
        ]
        
        return activities
    
    def _generate_assessment(self, subject):
        """Generate assessment rubric with country-specific standards"""
        return {
            'criteria': ['Understanding', 'Application', 'Analysis', 'Communication'],
            'weighting': [30, 25, 25, 20],
            'rubric': self._get_localized_rubric()
        }
    
    def _get_localized_rubric(self):
        """Get country-specific rubric descriptions"""
        rubrics = {
            'kenya': {
                'Excellent': 'Exceeds competency expectations with community application',
                'Good': 'Meets competency expectations with practical understanding',
                'Satisfactory': 'Basic competency achieved',
                'Needs Improvement': 'Requires additional support for competency'
            },
            'bangladesh': {
                'Excellent': 'Outstanding understanding with Bengali context mastery',
                'Good': 'Strong understanding with local application',
                'Satisfactory': 'Meets curriculum requirements',
                'Needs Improvement': 'Needs additional support for board standards'
            },
            'usa': {
                'Excellent': 'Exceeds standards with creativity and insight',
                'Good': 'Meets all standards with confidence',
                'Satisfactory': 'Meets basic standards',
                'Needs Improvement': 'Requires additional support for standards'
            },
            'uk': {
                'Excellent': 'Exceptional understanding with depth and rigor',
                'Good': 'Strong understanding with academic quality',
                'Satisfactory': 'Meets National Curriculum requirements',
                'Needs Improvement': 'Requires additional support for GCSE/A-Level preparation'
            }
        }
        
        return rubrics.get(self.country, {
            'Excellent': 'Demonstrates mastery with creativity',
            'Good': 'Shows strong understanding',
            'Satisfactory': 'Meets basic requirements',
            'Needs Improvement': 'Requires additional support'
        })

class ProfessionalOutcomeEngine:
    """Professional - Career Acceleration Lab"""
    
    def __init__(self, domain='business', country_code='kenya'):
        self.domain = domain
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
    
    def generate_workflow(self, task_type):
        """Generate AI-powered workflow for professional tasks"""
        workflows = {
            'research': {
                'steps': [
                    'Define research question',
                    'Gather and analyze data',
                    'Synthesize findings',
                    'Generate report',
                    'Add citations and references'
                ],
                'output': 'Research synthesis with actionable insights',
                'localization': f'Using {self.overlay.get("system", "global")} standards and {self.overlay.get("currency", "local")} context'
            },
            'marketing': {
                'steps': [
                    'Define target audience',
                    'Create content strategy',
                    'Generate marketing copy',
                    'Design visual elements',
                    'Track and optimize performance'
                ],
                'output': 'Multi-channel marketing campaign',
                'localization': f'Localized for {self.country.upper()} market with {self.overlay.get("language", "English")} support'
            },
            'analytics': {
                'steps': [
                    'Collect data from all sources',
                    'Clean and preprocess data',
                    'Perform statistical analysis',
                    'Create visualizations',
                    'Interpret results and suggest actions'
                ],
                'output': 'Comprehensive analytics dashboard',
                'localization': f'Adapted for {self.overlay.get("system", "local")} business environment'
            }
        }
        
        return workflows.get(task_type, workflows['research'])

class SMEOutcomeEngine:
    """SME - Growth Automation Engine"""
    
    def __init__(self, market='africa', country_code='kenya'):
        self.market = market
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
    
    def generate_automation(self, business_type):
        """Generate automation solutions for SMEs"""
        automations = {
            'retail': {
                'inventory': 'Auto-reorder when stock below threshold',
                'customer_support': 'AI chatbot for common queries',
                'payments': f'Integrated mobile money ({self._get_payment_rails()})',
                'marketing': f'Automated WhatsApp/SMS campaigns in {self.overlay.get("language", "English")}'
            },
            'service': {
                'booking': 'Self-service booking and scheduling',
                'followup': 'Automated client check-ins and feedback',
                'billing': 'Auto-generate invoices and receipts',
                'referrals': 'Digital referral tracking system'
            },
            'agriculture': {
                'weather_alerts': f'Real-time weather notifications for {self.country}',
                'market_prices': f'Daily price updates in {self.overlay.get("currency", "local")}',
                'supply_chain': 'Track and optimize distribution',
                'financial': f'Crop insurance and loan management in {self.country} context'
            }
        }
        
        return automations.get(business_type, automations['retail'])
    
    def _get_payment_rails(self):
        """Get country-specific payment rails"""
        rails = {
            'kenya': 'M-Pesa, Airtel Money, Equitel',
            'bangladesh': 'bKash, Nagad, Rocket',
            'usa': 'PayPal, Stripe, Venmo, Square',
            'uk': 'PayPal, Stripe, Barclays, Monzo'
        }
        return rails.get(self.country, 'M-Pesa, Airtel Money')

# ==================== MAIN APPLICATION ====================

# Initialize session state
def init_session_state():
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
        'preferred_language': 'English'
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# Page configuration
st.set_page_config(
    page_title="AI Shiksha - Universal Core + Local Overlay",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
def apply_custom_css():
    st.markdown("""
    <style>
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }
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
    }
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
    .flag-emoji {
        font-size: 1.2rem;
        margin-right: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

apply_custom_css()

# ==================== SIDEBAR ====================

st.sidebar.title("🌍 AI Shiksha")
st.sidebar.caption("Universal Core + Local Overlay")

# Country selection (USA, UK, Bangladesh, Kenya only)
country_flags = {
    'kenya': '🇰🇪',
    'bangladesh': '🇧🇩',
    'usa': '🇺🇸',
    'uk': '🇬🇧'
}

country_code = st.sidebar.selectbox(
    "🌐 Select Country/Region:",
    ['kenya', 'bangladesh', 'usa', 'uk'],
    format_func=lambda x: f"{country_flags.get(x, '🌍')} {x.title()}"
)
st.session_state.country_code = country_code

# Get overlay info
overlay = LocalCurriculumOverlay.get_overlay(country_code)
context = LocalCurriculumOverlay.get_local_context(country_code)

if overlay:
    st.sidebar.info(f"""
    **{country_flags.get(country_code, '🌍')} {country_code.title()}**
    **Curriculum:** {overlay.get('system', 'Universal')}
    **Exam Boards:** {', '.join(overlay.get('boards', ['Local']))}
    **Language:** {overlay.get('language', 'English')}
    **Currency:** {overlay.get('currency', 'Local')}
    """)

# Role selection
user_role = st.sidebar.selectbox(
    "👤 Select Your Role:",
    ['Student', 'Teacher', 'Professional', 'SME Business Owner']
)
st.session_state.user_role = user_role

# Navigation
menu_options = {
    'Student': ['🎓 Dashboard', '📝 Practice', '📊 Progress', '🏆 Achievements'],
    'Teacher': ['👨‍🏫 Dashboard', '📋 Lesson Builder', '📝 Assessment', '⏱️ Hours Saved'],
    'Professional': ['💼 Dashboard', '🔬 Research', '📈 Analytics', '📚 Portfolio'],
    'SME Business Owner': ['🏢 Dashboard', '📈 Growth', '🤖 Automation', '📊 Analytics']
}

st.sidebar.divider()
choice = st.sidebar.radio("Navigate:", menu_options.get(user_role, ['Dashboard']))

# Vibe Check
def show_vibe_check():
    with st.sidebar.expander("🎯 Daily Vibe Check", expanded=False):
        vibe = st.select_slider(
            "How's your learning energy today?",
            options=["😴 Low", "😐 Neutral", "⚡ Medium", "🔥 High", "🚀 Cosmic"],
            value="🔥 High"
        )
        
        if vibe in ["🔥 High", "🚀 Cosmic"]:
            st.success("Let's ride that energy wave! 🌊")
            st.balloons()
        elif vibe == "😴 Low":
            st.info("Start with a 5-min quick win!")
        
        if st.button("🎯 Get your vibe mission"):
            missions = {
                "😴 Low": "Complete 1 easy MCQ to get moving",
                "😐 Neutral": "Explore a new learning module",
                "⚡ Medium": "Generate a practice test",
                "🔥 High": "Tackle a complex problem set",
                "🚀 Cosmic": "Challenge: Build a mini-project"
            }
            st.info(f"🚀 **Vibe Mission:** {missions.get(vibe)}")

show_vibe_check()

# ==================== MAIN CONTENT ====================

def show_home():
    st.title("🌍 AI Shiksha Global Edition")
    st.subheader(f"{country_flags.get(country_code, '🌍')} {country_code.title()} - Universal Core + Local Curriculum Overlay")
    
    # Universal Core Overview
    with st.expander("🔷 Universal Core - Portable Across All Systems", expanded=True):
        st.markdown("""
        <div class="universal-core">
        <h4>📚 Core Subjects (Available Everywhere)</h4>
        """, unsafe_allow_html=True)
        
        cols = st.columns(3)
        subjects = ['Mathematics', 'English Language', 'Basic Science', 'Geography', 'General Knowledge', 'Applied AI']
        for i, subject in enumerate(subjects):
            cols[i % 3].markdown(f"✅ **{subject}**")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Local Overlay
    with st.expander("🔶 Local Curriculum Overlay - Country-Specific", expanded=True):
        st.markdown(f"""
        <div class="local-overlay">
        <h4>{country_flags.get(country_code, '🌍')} {country_code.title()} - Curriculum Details</h4>
        <p><strong>Curriculum System:</strong> {overlay.get('system', 'Universal')}</p>
        <p><strong>Exam Boards:</strong> {', '.join(overlay.get('boards', ['Local boards']))}</p>
        <p><strong>National Exams:</strong> {', '.join(overlay.get('national_exams', ['Local exams']))}</p>
        <p><strong>Language Support:</strong> {overlay.get('language', 'English')}</p>
        <p><strong>Grade Levels:</strong> {', '.join(overlay.get('grade_levels', ['All levels']))}</p>
        <p><strong>Currency:</strong> {overlay.get('currency', 'Local')}</p>
        <p><strong>Cultural Context:</strong> {context.get('culture', 'Global')}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Segment Engines
    st.divider()
    st.subheader("🎯 Segment-Specific Outcome Engines")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**🎓 Students**")
        st.caption("Grade & Exam Outcomes Engine")
        st.markdown("✅ Adaptive practice")
        st.markdown("✅ Score trends")
        st.markdown("✅ Competition prep")
        st.markdown("✅ Socratic loops")
    
    with col2:
        st.markdown("**👨‍🏫 Teachers**")
        st.caption("Hours-Saved Engine")
        st.markdown("✅ Lesson builder")
        st.markdown("✅ Rubric generator")
        st.markdown("✅ Feedback drafting")
        st.markdown("✅ Policy integrator")
    
    with col3:
        st.markdown("**💼 Professionals**")
        st.caption("Career Acceleration Lab")
        st.markdown("✅ AI workflows")
        st.markdown("✅ Portfolio artifacts")
        st.markdown("✅ Research synthesis")
        st.markdown("✅ Domain tracks")
    
    with col4:
        st.markdown("**🏢 SMEs**")
        st.caption("Growth Automation Engine")
        st.markdown("✅ Marketing automation")
        st.markdown("✅ Support chatbots")
        st.markdown("✅ Sales analytics")
        st.markdown("✅ Payment integration")

# ==================== STUDENT DASHBOARD ====================

def show_student_dashboard():
    st.header(f"🎓 Student Dashboard - {country_code.title()}")
    
    # Initialize engines
    student_engine = StudentOutcomeEngine(country_code)
    
    # Show current stats
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Score", f"{st.session_state.student_score}%")
    col2.metric("Day Streak", f"{st.session_state.streak} days")
    col3.metric("Completed Lessons", len(st.session_state.completed_lessons))
    col4.metric("Achievements", len(st.session_state.achievements))
    
    # Adaptive practice
    st.subheader("📝 Adaptive Practice")
    st.caption(f"Aligned with {overlay.get('system', 'Universal')} curriculum")
    
    subject = st.selectbox("Select Subject:", ['Mathematics', 'English Language', 'Basic Science', 'Geography', 'General Knowledge'])
    difficulty = st.select_slider("Difficulty Level:", ['easy', 'medium', 'hard'], value='medium')
    
    if st.button("🎯 Generate Practice Questions"):
        questions = student_engine.get_adaptive_questions(subject.lower(), difficulty)
        
        if questions:
            for q in questions[:2]:  # Show 2 questions
                st.markdown(f"### Question: {q['question']}")
                st.caption(f"📚 {q.get('exam_style', 'Local exam')} style")
                
                with st.expander("💡 Socratic Hint"):
                    st.info(q.get('socratic_hint', 'Think step by step'))
                
                selected = st.radio(f"Select your answer:", q['options'], key=f"q_{q['id']}")
                
                if st.button(f"Submit Answer {q['id']}", key=f"submit_{q['id']}"):
                    if selected == q['correct']:
                        st.balloons()
                        st.success(f"✅ Correct! {q.get('explanation', '')}")
                        st.session_state.student_score = min(100, st.session_state.student_score + 5)
                        st.session_state.streak += 1
                    else:
                        st.error(f"❌ Incorrect. The correct answer is {q['correct']}")
                        st.session_state.streak = 0
    
    # Progress tracking
    st.subheader("📊 Progress Tracking")
    
    # Create progress data
    weeks = ['Week 1', 'Week 2', 'Week 3', 'Week 4', 'Current']
    scores = [45, 52, 58, 63, st.session_state.student_score]
    
    df = pd.DataFrame({'Week': weeks, 'Score': scores})
    st.line_chart(df.set_index('Week'))
    
    # Performance analysis
    col1, col2 = st.columns(2)
    with col1:
        grade = student_engine._calculate_projected_grade({'score': st.session_state.student_score})
        st.metric("Projected Grade", grade)
    
    with col2:
        if st.session_state.student_score >= 60:
            st.success("✅ On track for success!")
        else:
            st.warning("📚 Keep practicing to improve")
    
    # Achievements
    if st.session_state.achievements:
        st.subheader("🏆 Achievements")
        for achievement in st.session_state.achievements:
            st.markdown(f'<span class="achievement-badge">🏆 {achievement}</span>', unsafe_allow_html=True)

# ==================== TEACHER DASHBOARD ====================

def show_teacher_dashboard():
    st.header(f"👨‍🏫 Teacher Dashboard - {country_code.title()}")
    
    teacher_engine = TeacherOutcomeEngine(country_code)
    
    # Hours saved counter
    col1, col2, col3 = st.columns(3)
    col1.metric("Hours Saved This Week", "4.5 hrs", "↑ 2.3 hrs")
    col2.metric("Time Saved vs Traditional", "62%", "↑ 12%")
    col3.metric("Lessons Generated", "23", "↑ 5")
    
    # Lesson Builder
    st.subheader("📋 Universal Lesson + Rubric Builder")
    st.caption(f"Aligned with {overlay.get('system', 'Universal')} curriculum")
    
    col1, col2 = st.columns(2)
    with col1:
        subject = st.text_input("Lesson Subject:", "Photosynthesis")
        grade = st.selectbox("Grade Level:", overlay.get('grade_levels', ['Primary', 'Secondary']))
        duration = st.slider("Lesson Duration (minutes):", 30, 90, 45)
    
    with col2:
        curriculum = st.selectbox("Curriculum Overlay:", ['Universal', overlay.get('system', 'Local')])
        include_ethics = st.checkbox("Include Ethics/Policy Module", value=True)
        language = st.selectbox("Language:", ['English', 'Kiswahili', 'Bengali', 'Spanish'])
    
    if st.button("✨ Generate Lesson Plan", type="primary"):
        with st.spinner("Generating lesson plan with local overlay..."):
            lesson = teacher_engine.generate_lesson_plan(subject, grade, duration)
            
            st.success(f"✅ Lesson Plan Generated in 2.3 seconds!")
            
            tab1, tab2, tab3 = st.tabs(["📋 Lesson Plan", "📊 Rubric", "⏱️ Time Savings"])
            
            with tab1:
                st.markdown(f"### {lesson['title']}")
                st.markdown(f"**Curriculum:** {lesson['curriculum']}")
                st.markdown(f"**Duration:** {duration} minutes")
                st.markdown(f"**Country Context:** {lesson.get('local_context', 'Universal')}")
                st.markdown(f"**Cultural Context:** {context.get('culture', 'Global')}")
                
                st.markdown("#### Learning Objectives:")
                for obj in lesson['objectives']:
                    st.markdown(f"- {obj}")
                
                st.markdown("#### Lesson Activities:")
                for activity in lesson['activities']:
                    st.markdown(f"- {activity}")
            
            with tab2:
                st.markdown("#### Assessment Rubric")
                rubric_data = []
                rubric = lesson['assessment']['rubric']
                for criterion, weight in zip(lesson['assessment']['criteria'], lesson['assessment']['weighting']):
                    rubric_data.append({
                        'Criterion': criterion,
                        'Weighting': f"{weight}%",
                        'Excellent': rubric.get('Excellent', 'Mastery'),
                        'Good': rubric.get('Good', 'Strong understanding'),
                        'Satisfactory': rubric.get('Satisfactory', 'Meets requirements'),
                        'Needs Improvement': rubric.get('Needs Improvement', 'Additional support needed')
                    })
                st.dataframe(pd.DataFrame(rubric_data))
            
            with tab3:
                st.markdown("#### ⏱️ Time Savings Analysis")
                st.metric("Traditional Grading Time", "100%", delta="-40-60%")
                st.success("""
                **Estimated Weekly Savings:**
                - Grading: 4.5 hours saved
                - Lesson Planning: 2.5 hours saved
                - Feedback Drafting: 2.0 hours saved
                **Total: 9.0 hours/week saved!** 🎉
                """)

# ==================== PROFESSIONAL DASHBOARD ====================

def show_professional_dashboard():
    st.header(f"💼 Professional Dashboard - {country_code.title()}")
    
    professional_engine = ProfessionalOutcomeEngine(st.session_state.domain, country_code)
    
    # Quick stats
    col1, col2, col3 = st.columns(3)
    col1.metric("Workflows Automated", "12", "↑ 3")
    col2.metric("Artifacts Generated", "24", "↑ 5")
    col3.metric("Time Saved", "18 hrs", "↑ 4 hrs")
    
    # Domain selection
    domain = st.selectbox("Select Domain:", ['Business', 'Finance', 'Marketing', 'Research', 'Education Technology'])
    st.session_state.domain = domain.lower()
    
    # Workflow generator
    st.subheader("🔬 Applied AI Workflow Generator")
    st.caption(f"Adapted for {country_code.upper()} business environment")
    
    task_type = st.selectbox("Task Type:", ['research', 'marketing', 'analytics', 'reporting'])
    
    if st.button("⚡ Generate AI Workflow", type="primary"):
        workflow = professional_engine.generate_workflow(task_type)
        
        st.markdown("### 🤖 AI-Powered Workflow")
        st.markdown(f"**Localization:** {workflow.get('localization', 'Global standard')}")
        
        st.markdown("#### Steps:")
        for i, step in enumerate(workflow['steps'], 1):
            st.markdown(f"{i}. {step}")
        
        st.info(f"**Output:** {workflow['output']}")
        
        # Generate sample artifact
        with st.expander("📄 View Sample Artifact"):
            st.markdown(f"""
            ### Executive Summary - {country_code.upper()} Market
            
            **Generated:** {datetime.now().strftime('%Y-%m-%d')}
            **Country Context:** {country_code.upper()}
            **Currency:** {overlay.get('currency', 'Local')}
            
            **Key Findings:**
            - 42% increase in efficiency with AI workflows
            - 37% reduction in manual processing time
            - ${int(overlay.get('currency_discount', 1)) * 15000:,} annual cost savings projected
            
            **Recommendations:**
            1. Implement automated reporting
            2. Deploy AI-powered analytics
            3. Establish continuous improvement loop
            """)

# ==================== SME DASHBOARD ====================

def show_sme_dashboard():
    st.header(f"🏢 SME Growth Automation Engine - {country_code.title()}")
    
    sme_engine = SMEOutcomeEngine('africa' if country_code in ['kenya', 'bangladesh'] else 'global', country_code)
    
    # Business metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Revenue Growth", "17%", "↑ 5%")
    col2.metric("Customer Satisfaction", "92%", "↑ 3%")
    col3.metric("Automation Rate", "68%", "↑ 12%")
    col4.metric("Cost Reduction", f"{overlay.get('currency', '$')}4,200", "↑ $1,200")
    
    # Business type
    business_type = st.selectbox(
        "Business Type:", 
        ['retail', 'service', 'agriculture', 'manufacturing', 'tech']
    )
    st.session_state.business_type = business_type
    
    # Automation solutions
    st.subheader("🤖 Automation Solutions")
    st.caption(f"Localized for {country_code.upper()} market with {overlay.get('language', 'English')} support")
    
    if st.button("🚀 Generate Automation Plan", type="primary"):
        automations = sme_engine.generate_automation(business_type)
        
        st.success(f"✅ Automation Plan Generated for {business_type.title()} Business")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 🔄 Automated Systems")
            for key, value in automations.items():
                st.markdown(f"- **{key.title()}:** {value}")
        
        with col2:
            st.markdown("#### 📊 Expected Impact")
            st.metric("Time Savings", "15-25 hours/week")
            st.metric("Revenue Increase", "20-30%", "Projected")
            st.metric("Customer Retention", "85%", "↑ 10%")
        
        # Payment integration
        st.subheader("💰 Multi-Rail Payment Integration")
        st.markdown(f"**Region:** {country_code.upper()}")
        st.markdown(f"**Currency:** {overlay.get('currency', 'Local')}")
        st.markdown("**Supported Payment Rails:**")
        
        rails = sme_engine._get_payment_rails()
        for rail in rails.split(', '):
            st.markdown(f"✅ {rail}")

# ==================== MAIN NAVIGATION ====================

def main():
    if choice == '🎓 Dashboard':
        show_student_dashboard()
    elif choice == '📝 Practice':
        show_student_dashboard()  # Same functionality for now
    elif choice == '📊 Progress':
        show_student_dashboard()  # Same functionality for now
    elif choice == '🏆 Achievements':
        show_student_dashboard()  # Same functionality for now
    elif choice == '👨‍🏫 Dashboard':
        show_teacher_dashboard()
    elif choice == '📋 Lesson Builder':
        show_teacher_dashboard()  # Same functionality for now
    elif choice == '📝 Assessment':
        show_teacher_dashboard()  # Same functionality for now
    elif choice == '⏱️ Hours Saved':
        show_teacher_dashboard()  # Same functionality for now
    elif choice == '💼 Dashboard':
        show_professional_dashboard()
    elif choice == '🔬 Research':
        show_professional_dashboard()  # Same functionality for now
    elif choice == '📈 Analytics':
        show_professional_dashboard()  # Same functionality for now
    elif choice == '📚 Portfolio':
        show_professional_dashboard()  # Same functionality for now
    elif choice == '🏢 Dashboard':
        show_sme_dashboard()
    elif choice == '📈 Growth':
        show_sme_dashboard()  # Same functionality for now
    elif choice == '🤖 Automation':
        show_sme_dashboard()  # Same functionality for now
    elif choice == '📊 Analytics':
        show_sme_dashboard()  # Same functionality for now
    else:
        show_home()

if __name__ == "__main__":
    main()
