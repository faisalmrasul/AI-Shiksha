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

# ==================== SEGMENT-SPECIFIC OUTCOME ENGINES ====================

class StudentOutcomeEngine:
    """Student - Grade & Exam Outcomes Engine"""
    
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.context = LocalCurriculumOverlay.get_local_context(country_code)
        self.question_pool = self._initialize_question_pool()
    
    def _initialize_question_pool(self):
        """Initialize a larger question pool"""
        return {
            'easy': [
                {
                    'id': 1,
                    'subject': 'mathematics',
                    'question': 'What is 5 + 7?',
                    'options': ['10', '11', '12', '13'],
                    'correct': '12',
                    'explanation': '5 + 7 = 12',
                    'socratic_hint': 'Count from 5: 6,7,8,9,10,11,12'
                },
                {
                    'id': 2,
                    'subject': 'english_language',
                    'question': 'What is the plural of "child"?',
                    'options': ['Childs', 'Children', 'Childrens', 'Childes'],
                    'correct': 'Children',
                    'explanation': 'The plural of "child" is "children"',
                    'socratic_hint': 'Think about irregular plurals in English'
                },
                {
                    'id': 3,
                    'subject': 'basic_science',
                    'question': 'What is the process by which plants make their own food?',
                    'options': ['Respiration', 'Photosynthesis', 'Fermentation', 'Digestion'],
                    'correct': 'Photosynthesis',
                    'explanation': 'Plants use photosynthesis to convert sunlight into energy',
                    'socratic_hint': 'Think about how plants use sunlight'
                },
                {
                    'id': 4,
                    'subject': 'geography',
                    'question': 'Which is the largest continent by area?',
                    'options': ['Africa', 'Asia', 'North America', 'Europe'],
                    'correct': 'Asia',
                    'explanation': 'Asia is the largest continent covering about 30% of Earth\'s land',
                    'socratic_hint': 'Think about the size of different continents'
                },
                {
                    'id': 5,
                    'subject': 'general_knowledge',
                    'question': 'What is the capital of Kenya?',
                    'options': ['Nairobi', 'Mombasa', 'Kisumu', 'Eldoret'],
                    'correct': 'Nairobi',
                    'explanation': 'Nairobi is the capital city of Kenya',
                    'socratic_hint': 'Think about major cities in East Africa'
                }
            ],
            'medium': [
                {
                    'id': 6,
                    'subject': 'mathematics',
                    'question': 'What is 15 × 8?',
                    'options': ['100', '120', '130', '150'],
                    'correct': '120',
                    'explanation': '15 × 8 = 120 (15 × 10 - 15 × 2 = 150 - 30 = 120)',
                    'socratic_hint': 'Break it down: 15 × 10 = 150, then subtract 15 × 2 = 30'
                },
                {
                    'id': 7,
                    'subject': 'english_language',
                    'question': 'Which word is a synonym for "happy"?',
                    'options': ['Sad', 'Joyful', 'Angry', 'Tired'],
                    'correct': 'Joyful',
                    'explanation': '"Joyful" is a synonym for "happy"',
                    'socratic_hint': 'Think about words that mean the same as happy'
                },
                {
                    'id': 8,
                    'subject': 'basic_science',
                    'question': 'What is the chemical symbol for water?',
                    'options': ['H2O', 'CO2', 'NaCl', 'HCl'],
                    'correct': 'H2O',
                    'explanation': 'Water is H2O - two hydrogen atoms and one oxygen atom',
                    'socratic_hint': 'Think about what water is made of'
                },
                {
                    'id': 9,
                    'subject': 'geography',
                    'question': 'Which country is known as the "Land of the Rising Sun"?',
                    'options': ['China', 'Japan', 'South Korea', 'Thailand'],
                    'correct': 'Japan',
                    'explanation': 'Japan is known as the "Land of the Rising Sun"',
                    'socratic_hint': 'Think about the meaning of the Japanese flag'
                },
                {
                    'id': 10,
                    'subject': 'general_knowledge',
                    'question': 'What is the currency of Bangladesh?',
                    'options': ['Rupee', 'Taka', 'Rial', 'Ringgit'],
                    'correct': 'Taka',
                    'explanation': 'Bangladeshi Taka is the currency of Bangladesh',
                    'socratic_hint': 'Think about currencies in South Asia'
                }
            ],
            'hard': [
                {
                    'id': 11,
                    'subject': 'mathematics',
                    'question': 'If 3x + 7 = 22, what is x?',
                    'options': ['3', '5', '7', '9'],
                    'correct': '5',
                    'explanation': '3x = 22 - 7 = 15, x = 15/3 = 5',
                    'socratic_hint': 'First, isolate the term with x'
                },
                {
                    'id': 12,
                    'subject': 'basic_science',
                    'question': 'What is the process by which plants release water vapor?',
                    'options': ['Transpiration', 'Photosynthesis', 'Respiration', 'Condensation'],
                    'correct': 'Transpiration',
                    'explanation': 'Transpiration is the process of water movement through plants and evaporation from leaves',
                    'socratic_hint': 'Think about how plants lose water'
                },
                {
                    'id': 13,
                    'subject': 'mathematics',
                    'question': 'What is the square root of 144?',
                    'options': ['10', '11', '12', '13'],
                    'correct': '12',
                    'explanation': '12 × 12 = 144, so the square root of 144 is 12',
                    'socratic_hint': 'Think about what number multiplied by itself gives 144'
                },
                {
                    'id': 14,
                    'subject': 'general_knowledge',
                    'question': 'What is the largest desert in the world?',
                    'options': ['Sahara', 'Gobi', 'Kalahari', 'Antarctic'],
                    'correct': 'Antarctic',
                    'explanation': 'The Antarctic Desert is the largest desert covering about 14 million km²',
                    'socratic_hint': 'Think about the definition of a desert'
                },
                {
                    'id': 15,
                    'subject': 'geography',
                    'question': 'Which river is the longest in the world?',
                    'options': ['Amazon', 'Nile', 'Mississippi', 'Yangtze'],
                    'correct': 'Amazon',
                    'explanation': 'The Amazon River is approximately 6,400 km long, making it the longest in the world',
                    'socratic_hint': 'Think about South America\'s largest river'
                }
            ]
        }
    
    def get_adaptive_questions(self, subject, difficulty='medium'):
        """Get adaptive questions based on student performance"""
        # Filter questions by subject
        questions = []
        for q in self.question_pool.get(difficulty, []):
            if subject.lower() in q['subject']:
                q_copy = q.copy()
                q_copy['country'] = self.country
                q_copy['exam_style'] = self.overlay.get('national_exams', ['local'])[0]
                q_copy['local_context'] = self.context
                questions.append(LocalCurriculumOverlay.localize_question(q_copy, self.country))
        
        # If no questions found for subject, return generic ones
        if not questions:
            for q in self.question_pool.get(difficulty, []):
                if q['subject'] == 'general_knowledge':
                    q_copy = q.copy()
                    q_copy['country'] = self.country
                    q_copy['exam_style'] = self.overlay.get('national_exams', ['local'])[0]
                    q_copy['local_context'] = self.context
                    questions.append(LocalCurriculumOverlay.localize_question(q_copy, self.country))
        
        return questions[:3]  # Return up to 3 questions
    
    def track_progress(self, user_data):
        """Track and visualize student progress"""
        progress_metrics = {
            'current_score': user_data.get('score', 0),
            'streak': user_data.get('streak', 0),
            'topics_mastered': user_data.get('mastered', []),
            'areas_to_improve': user_data.get('weak_areas', []),
            'projected_grade': self._calculate_projected_grade(user_data),
            'grade_level': self.overlay.get('grade_levels', ['Unknown'])[0],
            'questions_answered': st.session_state.total_questions_answered,
            'accuracy': self._calculate_accuracy()
        }
        return progress_metrics
    
    def _calculate_accuracy(self):
        """Calculate accuracy based on correct/total answers"""
        if st.session_state.total_questions_answered == 0:
            return 0
        return (st.session_state.correct_answers / st.session_state.total_questions_answered) * 100
    
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
        self.lesson_templates = self._initialize_lesson_templates()
    
    def _initialize_lesson_templates(self):
        """Initialize lesson plan templates for different subjects"""
        return {
            'photosynthesis': {
                'title': 'Photosynthesis: How Plants Make Food',
                'grade': 'Grade 7',
                'duration': 45,
                'curriculum': 'Universal',
                'objectives': [
                    'Explain the process of photosynthesis',
                    'Identify the key components needed for photosynthesis',
                    'Describe the importance of photosynthesis for life on Earth'
                ],
                'activities': [
                    'Interactive video demonstration (10 min)',
                    'Group discussion and modeling (20 min)',
                    'Diagram labeling and assessment (15 min)'
                ]
            },
            'algebra': {
                'title': 'Introduction to Algebra',
                'grade': 'Grade 8',
                'duration': 45,
                'curriculum': 'Universal',
                'objectives': [
                    'Understand basic algebraic concepts',
                    'Solve simple linear equations',
                    'Apply algebra to real-world problems'
                ],
                'activities': [
                    'Warm-up: Pattern recognition (10 min)',
                    'Main: Hands-on equation solving (20 min)',
                    'Closure: Real-world applications (15 min)'
                ]
            },
            'grammar': {
                'title': 'Mastering Grammar: Parts of Speech',
                'grade': 'Grade 5',
                'duration': 45,
                'curriculum': 'Universal',
                'objectives': [
                    'Identify different parts of speech',
                    'Use correct grammar in sentences',
                    'Improve writing skills'
                ],
                'activities': [
                    'Interactive grammar game (10 min)',
                    'Worksheet practice (20 min)',
                    'Creative writing exercise (15 min)'
                ]
            }
        }
    
    def generate_lesson_plan(self, subject, grade, duration, curriculum='universal'):
        """Generate lesson plan with local curriculum overlay"""
        subject_lower = subject.lower()
        overlay = LocalCurriculumOverlay.get_overlay(self.country)
        
        # Check if we have a template for this subject
        template_key = None
        for key in self.lesson_templates:
            if key in subject_lower or subject_lower in key:
                template_key = key
                break
        
        if template_key:
            template = self.lesson_templates[template_key]
            plan = {
                'title': template['title'],
                'curriculum': overlay.get('system', 'Universal'),
                'country': self.country,
                'duration': duration,
                'objectives': template['objectives'],
                'activities': template['activities'],
                'assessment': self._generate_assessment(subject)
            }
        else:
            # Generate generic plan
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
            plan['cultural_context'] = self.context
        
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
                    'Interpret results and suggest actions
