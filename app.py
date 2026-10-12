# app.py - AI Shiksha Global Platform
# Universal Core + Local Overlay Architecture
# Prototype — Aligned with EU AI Act (Regulation 2024/1689) Principles
#
# NOTE: This is a PROTOTYPE. It is not placed on the EU market.
# Its governance architecture is ALIGNED WITH EU AI Act principles
# as a design standard. No legal compliance claim is made.

import streamlit as st
import json
import os
import random
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import io
import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
import numpy as np

# ==================== OPTIONAL IMPORTS WITH FALLBACK ====================
try:
    import networkx as nx
    HAS_NETWORKX = True
except ImportError:
    nx = None
    HAS_NETWORKX = False

try:
    import matplotlib.pyplot as plt
    HAS_MATPLOTLIB = True
except ImportError:
    plt = None
    HAS_MATPLOTLIB = False

# ==================== PAGE CONFIGURATION - MUST BE FIRST ====================
st.set_page_config(
    page_title="AI Shiksha - Universal Core + Local Overlay",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None


# ==================== AI GOVERNANCE LAYER ====================
# Aligned with EU AI Act (Regulation 2024/1689) design principles.
# This module is a DESIGN STANDARD, not a legal compliance claim.
# AI Shiksha is a prototype; it is not placed on the EU market.

class AIRiskTier(Enum):
    PROHIBITED = "prohibited"
    HIGH = "high"
    LIMITED = "limited"
    MINIMAL = "minimal"


@dataclass
class AISystemRegistration:
    system_id: str
    name: str
    intended_purpose: str
    risk_tier: AIRiskTier
    affected_segments: List[str]
    human_oversight_required: bool
    transparency_required: bool
    annex_iii_category: Optional[str] = None


AI_SYSTEM_REGISTRY: Dict[str, AISystemRegistration] = {
    "student.mastery_engine": AISystemRegistration(
        system_id="student.mastery_engine",
        name="Student Mastery & Gap Analysis",
        intended_purpose="Adaptive practice, mastery determination, gap detection",
        risk_tier=AIRiskTier.HIGH,
        annex_iii_category="Annex III 3(b) — evaluating learning outcomes",
        affected_segments=["Student"],
        human_oversight_required=True,
        transparency_required=True,
    ),
    "teacher.feedback_generator": AISystemRegistration(
        system_id="teacher.feedback_generator",
        name="Batch Feedback Assistant",
        intended_purpose="Draft feedback for teacher review",
        risk_tier=AIRiskTier.HIGH,
        annex_iii_category="Annex III 3(b) — evaluating learning outcomes",
        affected_segments=["Teacher", "Student"],
        human_oversight_required=True,
        transparency_required=True,
    ),
    "teacher.lesson_builder": AISystemRegistration(
        system_id="teacher.lesson_builder",
        name="Lesson Bundle Generator",
        intended_purpose="Generate lesson assets for teacher use",
        risk_tier=AIRiskTier.LIMITED,
        affected_segments=["Teacher"],
        human_oversight_required=True,
        transparency_required=True,
    ),
    "student.socratic_tutor": AISystemRegistration(
        system_id="student.socratic_tutor",
        name="Socratic Guidance",
        intended_purpose="Content-only hints and analogies",
        risk_tier=AIRiskTier.LIMITED,
        affected_segments=["Student"],
        human_oversight_required=False,
        transparency_required=True,
    ),
    "sme.predictive_engine": AISystemRegistration(
        system_id="sme.predictive_engine",
        name="SME Predictive Analytics",
        intended_purpose="Forecasting and task prioritisation",
        risk_tier=AIRiskTier.LIMITED,
        affected_segments=["SME Business Owner"],
        human_oversight_required=True,
        transparency_required=True,
    ),
    "professional.research_engine": AISystemRegistration(
        system_id="professional.research_engine",
        name="Professional Research & Portfolio",
        intended_purpose="Search, citation, analysis for professionals",
        risk_tier=AIRiskTier.LIMITED,
        affected_segments=["Professional"],
        human_oversight_required=True,
        transparency_required=True,
    ),
}


class TransparencyLayer:
    """Attaches AI disclosure to every AI-generated output."""

    DISCLOSURES = {
        AIRiskTier.HIGH: (
            "⚠️ AI-assisted. Output must be reviewed by a qualified human "
            "before being relied upon. You may contest this output."
        ),
        AIRiskTier.LIMITED: "ℹ️ AI-generated content. Verify important information.",
        AIRiskTier.MINIMAL: "ℹ️ AI-powered suggestion.",
    }

    @staticmethod
    def attach(output: Dict[str, Any], system_id: str) -> Dict[str, Any]:
        reg = AI_SYSTEM_REGISTRY.get(system_id)
        if not reg or not isinstance(output, dict):
            return output

        return {
            **output,
            "_ai_disclosure": {
                "system_id": system_id,
                "system_name": reg.name,
                "risk_tier": reg.risk_tier.value,
                "disclosure_text": TransparencyLayer.DISCLOSURES[reg.risk_tier],
                "human_oversight": reg.human_oversight_required,
                "generated_at": datetime.now().isoformat(),
                "note": "AI Shiksha is a prototype. Design aligns with EU AI Act "
                        "principles but makes no legal compliance claim.",
            },
        }


class HumanOversightGate:
    """Requires named human approval for high-risk outputs (Art. 14 aligned)."""

    @staticmethod
    def check(system_id: str, approved_by: Optional[str]) -> Dict[str, Any]:
        reg = AI_SYSTEM_REGISTRY.get(system_id)
        if not reg or reg.risk_tier != AIRiskTier.HIGH:
            return {"allowed": True, "reason": "Not high-risk"}

        if not approved_by:
            return {
                "allowed": False,
                "reason": f"'{reg.name}' is high-risk. A named human approver "
                          f"is required before output reaches end users.",
                "system_id": system_id,
            }

        return {"allowed": True, "approved_by": approved_by}


class AIEventLogger:
    """Lightweight event logging for a prototype. Writes JSONL to disk."""

    def __init__(self, path: str = "compliance/events.jsonl"):
        self.path = path

    def log(
        self,
        system_id: str,
        segment: str,
        input_text: str,
        output_summary: str,
        approved_by: Optional[str] = None,
    ) -> str:
        event_id = hashlib.sha256(
            f"{system_id}{datetime.now().timestamp()}".encode()
        ).hexdigest()[:12]

        event = {
            "event_id": event_id,
            "system_id": system_id,
            "timestamp": datetime.now().isoformat(),
            "segment": segment,
            "input_hash": hashlib.sha256(input_text.encode()).hexdigest()[:16],
            "output_summary": str(output_summary)[:300],
            "human_approved_by": approved_by,
        }

        try:
            os.makedirs(os.path.dirname(self.path), exist_ok=True)
            with open(self.path, "a") as f:
                f.write(json.dumps(event) + "\n")
        except Exception:
            pass  # prototype: never block the user for logging failure

        return event_id


# Singleton helpers
def _transparency():
    return TransparencyLayer()

def _oversight():
    return HumanOversightGate()

def _logger():
    return AIEventLogger()


# ==================== TEACHER DATA MODELS ====================

@dataclass
class LessonPlan:
    id: str
    title: str
    subject: str
    grade_level: str
    duration: int
    objectives: List[str]
    standards: List[str]
    materials: List[str]
    warm_up: str
    direct_instruction: str
    guided_practice: str
    independent_practice: str
    assessment: str
    differentiation: Dict[str, str]
    exit_ticket: str
    created_at: datetime
    modified_at: datetime


@dataclass
class Rubric:
    id: str
    title: str
    criteria: List[str]
    levels: List[str]
    descriptions: Dict[str, Dict[str, str]]
    weightings: Dict[str, float]


@dataclass
class Quiz:
    id: str
    title: str
    subject: str
    grade_level: str
    questions: List[Dict[str, Any]]
    total_points: int
    time_limit: Optional[int]
    created_at: datetime


@dataclass
class StudentFeedback:
    id: str
    student_name: str
    assignment: str
    strengths: List[str]
    areas_for_growth: List[str]
    suggestions: str
    score: Optional[float]
    generated_at: datetime
    approved: bool = False
    approved_by: Optional[str] = None


@dataclass
class TimeSavedMetric:
    week_start: datetime
    lesson_planning_hours: float
    grading_hours: float
    admin_hours: float
    total_hours: float
    week_over_week_change: float


class CurriculumStandard(Enum):
    COMMON_CORE = "common_core"
    NGSS = "ngss"
    TEKS = "teks"
    CBC = "cbc"
    NCTB = "nctb"
    NATIONAL = "national"


# ==================== TEACHER INTELLIGENCE ENGINE ====================

class TeacherIntelligenceEngine:
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.lesson_plans = []
        self.rubrics = []
        self.quizzes = []
        self.feedback_batches = []
        self.time_saved_history = []
        self.standard_databases = {}

        self._initialize_sample_data()
        self._initialize_standard_databases()

    def _initialize_sample_data(self):
        sample_lesson = LessonPlan(
            id='lp_001',
            title='Introduction to Photosynthesis',
            subject='Science',
            grade_level='Grade 7',
            duration=45,
            objectives=[
                'Explain the process of photosynthesis',
                'Identify the reactants and products of photosynthesis',
                'Describe the role of chlorophyll in photosynthesis'
            ],
            standards=['NGSS-LS1-6: Photosynthesis and energy flow'],
            materials=['Whiteboard', 'Markers', 'Plant diagrams', 'Worksheet'],
            warm_up='What do plants need to grow? Discuss with partner (5 min)',
            direct_instruction='Explain photosynthesis using diagrams and key vocabulary (15 min)',
            guided_practice='Label photosynthesis diagram with teacher support (10 min)',
            independent_practice='Complete worksheet independently (10 min)',
            assessment='Exit ticket: List 3 things plants need for photosynthesis',
            differentiation={
                'ELL': 'Key vocabulary list with images',
                'Gifted': 'Research extension: How does photosynthesis vary in different plants?',
                'Struggling': 'Fill-in-the-blank guided notes'
            },
            exit_ticket='Write 3 facts about photosynthesis',
            created_at=datetime.now() - timedelta(days=7),
            modified_at=datetime.now() - timedelta(days=3)
        )
        self.lesson_plans.append(sample_lesson)

        sample_rubric = Rubric(
            id='rb_001',
            title='Science Lab Report Rubric',
            criteria=['Hypothesis', 'Procedure', 'Data Collection', 'Analysis', 'Conclusion'],
            levels=['Excellent', 'Proficient', 'Developing', 'Beginning'],
            descriptions={
                'Hypothesis': {
                    'Excellent': 'Clear, testable hypothesis with scientific reasoning',
                    'Proficient': 'Clear, testable hypothesis',
                    'Developing': 'Vague hypothesis, lacks clarity',
                    'Beginning': 'No hypothesis or completely unclear'
                },
                'Procedure': {
                    'Excellent': 'Detailed, replicable procedure with safety considerations',
                    'Proficient': 'Clear procedure, replicable',
                    'Developing': 'Missing steps, hard to follow',
                    'Beginning': 'No procedure or completely unclear'
                },
                'Data Collection': {
                    'Excellent': 'Comprehensive data with visual representations',
                    'Proficient': 'Complete data collection',
                    'Developing': 'Incomplete data, missing observations',
                    'Beginning': 'No data collected'
                },
                'Analysis': {
                    'Excellent': 'Deep analysis with connections to concepts',
                    'Proficient': 'Correct analysis of data',
                    'Developing': 'Superficial analysis, missing connections',
                    'Beginning': 'No analysis or completely incorrect'
                },
                'Conclusion': {
                    'Excellent': 'Well-supported conclusion with broader implications',
                    'Proficient': 'Supported conclusion',
                    'Developing': 'Weak conclusion, not supported by data',
                    'Beginning': 'No conclusion or completely unsupported'
                }
            },
            weightings={
                'Hypothesis': 0.15,
                'Procedure': 0.15,
                'Data Collection': 0.20,
                'Analysis': 0.25,
                'Conclusion': 0.25
            }
        )
        self.rubrics.append(sample_rubric)

        sample_quiz = Quiz(
            id='qz_001',
            title='Photosynthesis Quiz',
            subject='Science',
            grade_level='Grade 7',
            questions=[
                {
                    'id': 'q1',
                    'type': 'multiple_choice',
                    'question': 'What is the primary energy source for photosynthesis?',
                    'options': ['Glucose', 'Sunlight', 'Water', 'Carbon Dioxide'],
                    'correct_answer': 'Sunlight',
                    'points': 2
                },
                {
                    'id': 'q2',
                    'type': 'multiple_choice',
                    'question': 'What are the products of photosynthesis?',
                    'options': ['Carbon Dioxide and Water', 'Glucose and Oxygen', 'Water and Oxygen', 'Glucose and Carbon Dioxide'],
                    'correct_answer': 'Glucose and Oxygen',
                    'points': 2
                },
            ],
            total_points=4,
            time_limit=15,
            created_at=datetime.now() - timedelta(days=2)
        )
        self.quizzes.append(sample_quiz)

        sample_time_saved = TimeSavedMetric(
            week_start=datetime.now() - timedelta(days=7),
            lesson_planning_hours=2.5,
            grading_hours=3.0,
            admin_hours=1.5,
            total_hours=7.0,
            week_over_week_change=0.15
        )
        self.time_saved_history.append(sample_time_saved)

    def _initialize_standard_databases(self):
        self.standard_databases = {
            'common_core': {
                'ELA': ['CCRA.R.1', 'CCRA.R.2', 'CCRA.W.1', 'CCRA.W.2', 'CCRA.SL.1'],
                'Math': ['CCRA.M.1', 'CCRA.M.2', 'CCRA.M.3', 'CCRA.M.4', 'CCRA.M.5']
            },
            'ngss': {
                'Physical': ['PS1-1', 'PS1-2', 'PS2-1', 'PS2-2', 'PS3-1'],
                'Life': ['LS1-1', 'LS1-2', 'LS2-1', 'LS2-2', 'LS3-1'],
                'Earth': ['ESS1-1', 'ESS1-2', 'ESS2-1', 'ESS2-2', 'ESS3-1']
            },
            'teks': {
                'Science': ['TEKS.7.5A', 'TEKS.7.6A', 'TEKS.7.7A', 'TEKS.7.8A'],
                'Math': ['TEKS.7.1A', 'TEKS.7.2A', 'TEKS.7.3A', 'TEKS.7.4A']
            },
            'cbc': {
                'Science': ['CBC.SCI.7.1', 'CBC.SCI.7.2', 'CBC.SCI.7.3'],
                'Math': ['CBC.MATH.7.1', 'CBC.MATH.7.2', 'CBC.MATH.7.3']
            }
        }

    def connect_lms(self, lms_type: str, credentials: Dict[str, str]) -> Dict[str, Any]:
        lms_configs = {
            'google_classroom': {'name': 'Google Classroom', 'icon': '📚',
                                 'features': ['sync_assignments', 'sync_grades', 'roster_management'],
                                 'requires_oauth': True},
            'canvas': {'name': 'Canvas', 'icon': '🎨',
                       'features': ['sync_assignments', 'sync_grades', 'course_materials', 'discussions'],
                       'requires_oauth': True},
            'schoology': {'name': 'Schoology', 'icon': '📖',
                          'features': ['sync_assignments', 'sync_grades', 'courses'],
                          'requires_oauth': True},
            'microsoft_teams': {'name': 'Microsoft Teams', 'icon': '💬',
                                'features': ['sync_assignments', 'sync_grades', 'teams_integration'],
                                'requires_oauth': True}
        }
        if lms_type in lms_configs:
            return {'status': 'connected', 'lms_type': lms_type,
                    'config': lms_configs[lms_type],
                    'message': f"Successfully connected to {lms_configs[lms_type]['name']}"}
        return {'status': 'error', 'message': f"Unsupported LMS: {lms_type}"}

    def sync_lms_data(self, lms_type: str, sync_type: str = 'all') -> Dict[str, Any]:
        return {'status': 'success', 'lms_type': lms_type, 'sync_type': sync_type,
                'data': {'students': 25, 'assignments': 8, 'grades_synced': 72,
                         'last_sync': datetime.now().isoformat()},
                'message': f"Successfully synced {sync_type} data from {lms_type}"}

    def map_standards(self, content: str, standard_type: str = 'common_core') -> List[str]:
        matched = []
        content_lower = content.lower()
        standards_db = self.standard_databases.get(standard_type, {})
        for category, standards in standards_db.items():
            for standard in standards:
                standard_keywords = standard.lower().split('.')
                if any(keyword in content_lower for keyword in standard_keywords):
                    matched.append(standard)
        return matched[:5]

    def convert_document(self, uploaded_file, output_format: str) -> Dict[str, Any]:
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            doc_engine = DocumentIntelligenceEngine(self.country)
            text = doc_engine.extract_text_from_file(uploaded_file)
            if text.startswith("Error"):
                return {'status': 'error', 'message': text}
            converted = {
                'original_format': file_extension,
                'output_format': output_format,
                'content': text,
                'title': uploaded_file.name.replace(f'.{file_extension}', ''),
                'downloadable': True
            }
            converted['message'] = f'Converted to {output_format} format'
            return converted
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def generate_lesson_bundle(self, subject: str, grade: str, topic: str, duration: int) -> Dict[str, Any]:
        lesson_plan = self._generate_lesson_plan(subject, grade, topic, duration)
        slide_outline = self._generate_slide_outline(lesson_plan)
        worksheet = self._generate_worksheet(lesson_plan)
        answer_key = self._generate_answer_key(worksheet)

        bundle = {
            'lesson_plan': lesson_plan,
            'slide_outline': slide_outline,
            'worksheet': worksheet,
            'answer_key': answer_key,
            'bundle_id': f"bundle_{hashlib.md5(f'{subject}{grade}{topic}'.encode()).hexdigest()[:8]}",
            'created_at': datetime.now().isoformat()
        }

        # Log event
        _logger().log(
            system_id="teacher.lesson_builder",
            segment="Teacher",
            input_text=f"{subject}|{grade}|{topic}",
            output_summary=f"Generated bundle {bundle['bundle_id']}"
        )

        return _transparency().attach(bundle, "teacher.lesson_builder")

    def _generate_lesson_plan(self, subject: str, grade: str, topic: str, duration: int) -> Dict[str, Any]:
        return {
            'title': f"{topic} - {subject} ({grade})",
            'subject': subject,
            'grade': grade,
            'duration': duration,
            'objectives': [
                f'Understand key concepts of {topic}',
                f'Apply {topic} knowledge to real-world scenarios',
                f'Develop critical thinking skills related to {topic}'
            ],
            'standards': self.map_standards(topic),
            'materials': ['Textbook', 'Worksheets', 'Multimedia resources'],
            'procedure': {
                'warm_up': f'Engage students with a question about {topic} (5-10 min)',
                'direct_instruction': f'Present key concepts of {topic} (15-20 min)',
                'guided_practice': f'Work through examples together (10-15 min)',
                'independent_practice': f'Students work independently on {topic} (15-20 min)',
                'closure': f'Review and assess understanding with exit ticket (5 min)'
            },
            'differentiation': {
                'struggling': 'Provide additional support and scaffolding',
                'gifted': 'Offer extension activities and deeper exploration',
                'ell': 'Include visuals and simplified language'
            },
            'assessment': f'Formative assessment throughout, summative quiz at end'
        }

    def _generate_slide_outline(self, lesson_plan: Dict[str, Any]) -> List[Dict[str, Any]]:
        return [
            {'slide': 1, 'title': f"Welcome to {lesson_plan['title']}", 'type': 'title'},
            {'slide': 2, 'title': 'Learning Objectives', 'type': 'objectives'},
            {'slide': 3, 'title': 'Key Vocabulary', 'type': 'vocabulary'},
            {'slide': 4, 'title': 'Introduction', 'type': 'intro'},
            {'slide': 5, 'title': 'Main Concepts', 'type': 'content'},
            {'slide': 6, 'title': 'Examples', 'type': 'examples'},
            {'slide': 7, 'title': 'Practice Problems', 'type': 'practice'},
            {'slide': 8, 'title': 'Summary', 'type': 'summary'},
            {'slide': 9, 'title': 'Questions', 'type': 'questions'},
            {'slide': 10, 'title': 'Next Steps', 'type': 'next_steps'}
        ]

    def _generate_worksheet(self, lesson_plan: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'title': f"{lesson_plan['title']} - Worksheet",
            'sections': [
                {'section': 'Part 1: Vocabulary',
                 'instructions': 'Match the vocabulary terms to their definitions',
                 'questions': ['Term 1', 'Term 2', 'Term 3']},
                {'section': 'Part 2: Concept Check',
                 'instructions': 'Answer the following questions based on the lesson',
                 'questions': ['Question 1', 'Question 2', 'Question 3']},
                {'section': 'Part 3: Application',
                 'instructions': 'Apply your knowledge to these scenarios',
                 'questions': ['Scenario 1', 'Scenario 2']}
            ],
            'total_points': 20
        }

    def _generate_answer_key(self, worksheet: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'title': f"Answer Key - {worksheet['title']}",
            'answers': {
                'Part 1': ['Term 1 Definition', 'Term 2 Definition', 'Term 3 Definition'],
                'Part 2': ['Question 1 Answer', 'Question 2 Answer', 'Question 3 Answer'],
                'Part 3': ['Scenario 1 Solution', 'Scenario 2 Solution']
            },
            'total_points': worksheet['total_points']
        }

    def adjust_reading_level(self, text: str, target_level: str) -> Dict[str, Any]:
        words = text.split()
        word_count = len(words)
        reading_levels = {
            'beginner': {'vocab_complexity': 0.3, 'sentence_complexity': 0.4, 'description': 'Grades 2-3'},
            'intermediate': {'vocab_complexity': 0.5, 'sentence_complexity': 0.6, 'description': 'Grades 4-6'},
            'advanced': {'vocab_complexity': 0.7, 'sentence_complexity': 0.8, 'description': 'Grades 7-9'},
            'expert': {'vocab_complexity': 0.9, 'sentence_complexity': 0.9, 'description': 'Grades 10-12'}
        }
        level_config = reading_levels.get(target_level, reading_levels['intermediate'])
        adjusted_text = text
        if target_level == 'beginner':
            adjusted_text = text.replace('complex', 'hard').replace('analyze', 'study')
            adjusted_text = ' '.join(adjusted_text.split()[:word_count // 2])
        elif target_level == 'expert':
            adjusted_text = text + ' This content has been enhanced for advanced readers with additional context and depth.'

        result = {
            'original_text': text,
            'adjusted_text': adjusted_text,
            'target_level': target_level,
            'level_description': level_config['description'],
            'word_count_original': word_count,
            'word_count_adjusted': len(adjusted_text.split()),
            'changes': {
                'vocabulary': f"Adjusted to {level_config['vocab_complexity']*100:.0f}% complexity",
                'sentences': f"Adjusted to {level_config['sentence_complexity']*100:.0f}% complexity"
            }
        }
        return _transparency().attach(result, "teacher.lesson_builder")

    def generate_rubric(self, title: str, criteria: List[str], levels: List[str]) -> Rubric:
        rubric_id = f"rb_{hashlib.md5(f'{title}{datetime.now().timestamp()}'.encode()).hexdigest()[:8]}"
        descriptions = {}
        for criterion in criteria:
            descriptions[criterion] = {
                levels[0]: f"Excellent: {criterion} - demonstrates mastery",
                levels[1]: f"Proficient: {criterion} - shows understanding",
                levels[2]: f"Developing: {criterion} - needs more support",
                levels[3]: f"Beginning: {criterion} - requires intervention"
            }
        weightings = {criterion: 1.0 / len(criteria) for criterion in criteria}
        return Rubric(id=rubric_id, title=title, criteria=criteria, levels=levels,
                      descriptions=descriptions, weightings=weightings)

    def generate_quiz(self, subject: str, grade: str, topic: str, num_questions: int = 5) -> Quiz:
        quiz_id = f"qz_{hashlib.md5(f'{subject}{grade}{topic}{datetime.now().timestamp()}'.encode()).hexdigest()[:8]}"
        questions = []
        question_types = ['multiple_choice', 'short_answer', 'open_ended']
        for i in range(num_questions):
            q_type = question_types[i % len(question_types)]
            question = {
                'id': f'q{i+1}',
                'type': q_type,
                'question': f'Question {i+1} about {topic}',
                'points': 2 if q_type == 'multiple_choice' else 3 if q_type == 'short_answer' else 5
            }
            if q_type == 'multiple_choice':
                question['options'] = ['Option A', 'Option B', 'Option C', 'Option D']
                question['correct_answer'] = 'Option A'
            if q_type == 'short_answer':
                question['correct_answer'] = f'Correct answer for question {i+1}'
            questions.append(question)

        total_points = sum(q.get('points', 0) for q in questions)
        return Quiz(
            id=quiz_id,
            title=f"{topic} Quiz - {subject} ({grade})",
            subject=subject,
            grade_level=grade,
            questions=questions,
            total_points=total_points,
            time_limit=total_points * 2,
            created_at=datetime.now()
        )

    def get_lesson_blocks(self, lesson_plan: LessonPlan) -> Dict[str, Any]:
        return {
            'blocks': {
                'warm_up': {'content': lesson_plan.warm_up, 'editable': True, 'regenerable': True},
                'direct_instruction': {'content': lesson_plan.direct_instruction, 'editable': True, 'regenerable': True},
                'guided_practice': {'content': lesson_plan.guided_practice, 'editable': True, 'regenerable': True},
                'independent_practice': {'content': lesson_plan.independent_practice, 'editable': True, 'regenerable': True},
                'assessment': {'content': lesson_plan.assessment, 'editable': True, 'regenerable': True},
                'exit_ticket': {'content': lesson_plan.exit_ticket, 'editable': True, 'regenerable': True}
            },
            'lesson_id': lesson_plan.id,
            'title': lesson_plan.title
        }

    def regenerate_block(self, block_type: str, context: str) -> str:
        templates = {
            'warm_up': f"New warm-up activity for: {context}",
            'direct_instruction': f"Updated direct instruction for: {context}",
            'guided_practice': f"New guided practice for: {context}",
            'independent_practice': f"Updated independent practice for: {context}",
            'assessment': f"New assessment for: {context}",
            'exit_ticket': f"New exit ticket for: {context}"
        }
        return templates.get(block_type, f"Regenerated {block_type} for: {context}")

    def apply_accommodation(self, content: str, accommodation_type: str) -> Dict[str, Any]:
        accommodations = {
            'iep_504': {'name': 'IEP/504 Modification',
                        'changes': 'Extended time, modified assignments, preferential seating',
                        'applied': True},
            'sentence_starters': {'name': 'Sentence Starters',
                                  'changes': 'Added sentence frames for writing tasks',
                                  'applied': True},
            'ell_translation': {'name': 'ELL Translation',
                                'changes': 'Added bilingual support and visual aids',
                                'applied': True},
            'simplified_text': {'name': 'Simplified Text',
                                'changes': 'Reduced complexity, added definitions',
                                'applied': True}
        }
        result = accommodations.get(accommodation_type, {})
        if result.get('applied', False):
            modified_content = content
            if accommodation_type == 'sentence_starters':
                modified_content = f"Start with: I think that...\n\nOriginal: {content}"
            elif accommodation_type == 'ell_translation':
                modified_content = f"[Translation]\n{content}\n\n[Original]\n{content}"
            elif accommodation_type == 'simplified_text':
                modified_content = f"Simple: {content[:100]}...\n\nOriginal: {content}"
            return {
                'status': 'applied',
                'accommodation_type': accommodation_type,
                'name': result['name'],
                'changes': result['changes'],
                'modified_content': modified_content
            }
        return {'status': 'unknown', 'message': f'Unknown accommodation: {accommodation_type}'}

    def generate_batch_feedback(self, assignments: List[Dict[str, Any]]) -> List[StudentFeedback]:
        # FIXED: f-string nested quote bug for Python 3.10/3.11 compatibility
        feedback_batch = []
        logger = _logger()

        for assignment in assignments:
            strengths = [
                random.choice(['Strong understanding of concepts', 'Good analysis', 'Clear writing']),
                random.choice(['Effective use of evidence', 'Engaging writing style', 'Critical thinking'])
            ]
            areas_for_growth = [
                random.choice(['Add more detail', 'Check grammar and spelling', 'Provide more examples']),
                random.choice(['Expand on ideas', 'Clarify arguments', 'Use stronger evidence'])
            ]

            name = assignment.get('student_name', 'Student')
            ts = datetime.now().timestamp()
            feedback_id = f"fb_{hashlib.md5(f'{name}{ts}'.encode()).hexdigest()[:8]}"

            feedback = StudentFeedback(
                id=feedback_id,
                student_name=name,
                assignment=assignment.get('assignment_title', 'Assignment'),
                strengths=strengths,
                areas_for_growth=areas_for_growth,
                suggestions=f"Based on your work, I recommend focusing on "
                            f"{areas_for_growth[0].lower()} and {areas_for_growth[1].lower()}.",
                score=random.randint(70, 95),
                generated_at=datetime.now(),
                approved=False,
                approved_by=None  # High-risk: requires named approver
            )

            # Log event
            logger.log(
                system_id="teacher.feedback_generator",
                segment="Teacher",
                input_text=str(assignment),
                output_summary=feedback.suggestions,
            )

            feedback_batch.append(feedback)

        self.feedback_batches.extend(feedback_batch)
        return feedback_batch

    def approve_feedback(self, feedback_id: str, approved_by: str = None) -> Dict[str, Any]:
        # Enforce human oversight gate
        gate = _oversight().check("teacher.feedback_generator", approved_by)
        if not gate["allowed"]:
            return {"status": "blocked", "reason": gate["reason"]}

        for feedback in self.feedback_batches:
            if feedback.id == feedback_id:
                feedback.approved = True
                feedback.approved_by = approved_by
                _logger().log(
                    system_id="teacher.feedback_generator",
                    segment="Teacher",
                    input_text=feedback_id,
                    output_summary=f"Approved by {approved_by}",
                    approved_by=approved_by
                )
                return {
                    'status': 'approved',
                    'feedback_id': feedback_id,
                    'message': f"Feedback for {feedback.student_name} approved"
                }

        return {'status': 'error', 'message': 'Feedback not found'}

    def calculate_time_saved(self) -> Dict[str, Any]:
        breakdown = {
            'lesson_planning': {'hours': 2.5, 'saved': 'vs 4.5 hours traditional'},
            'grading': {'hours': 3.0, 'saved': 'vs 6 hours traditional'},
            'admin_work': {'hours': 1.5, 'saved': 'vs 3 hours traditional'},
            'feedback_drafting': {'hours': 1.0, 'saved': 'vs 2 hours traditional'}
        }
        total_hours = sum(item['hours'] for item in breakdown.values())
        traditional_hours = 15.5
        return {
            'total_hours_saved': round(total_hours, 1),
            'total_percent_saved': round((total_hours / traditional_hours) * 100, 1),
            'breakdown': breakdown,
            'weekly_average': round(total_hours, 1),
            'monthly_projection': round(total_hours * 4, 1),
            'yearly_projection': round(total_hours * 48, 1)
        }

    def generate_parent_update(self, student_name: str, subject: str, progress: str) -> str:
        templates = [
            f"Dear Parent/Guardian of {student_name},\n\n"
            f"I am pleased to share an update on {student_name}'s progress in {subject}. "
            f"{student_name} has been {progress}. "
            f"I look forward to continuing to support {student_name}'s growth. "
            f"Please reach out if you have any questions.\n\n"
            f"Best regards,\nTeacher",
        ]
        return random.choice(templates)

    def generate_sub_plan(self, subject: str, grade: str, lesson_topic: str) -> Dict[str, Any]:
        return {
            'title': f"Sub Plan: {lesson_topic} - {subject} ({grade})",
            'overview': f"This plan covers {lesson_topic} for {grade} students in {subject}.",
            'schedule': {
                'period_1': {'time': '8:00-8:45', 'activity': f'Intro to {lesson_topic}', 'materials': 'Textbook pages 1-5'},
                'period_2': {'time': '8:50-9:35', 'activity': f'Guided practice on {lesson_topic}', 'materials': 'Worksheet'},
                'period_3': {'time': '9:40-10:25', 'activity': 'Independent work', 'materials': 'Assignment'},
                'period_4': {'time': '10:30-11:15', 'activity': 'Review and wrap-up', 'materials': 'Answer key'}
            },
            'emergency_procedures': 'In case of emergency, follow school protocol in the handbook.',
            'notes': 'Please leave notes on student progress for the regular teacher.'
        }

    def redact_pii(self, text: str) -> Dict[str, Any]:
        redacted_text = text
        name_pattern = r'\b[A-Z][a-z]+\s[A-Z][a-z]+\b'
        redacted_text = re.sub(name_pattern, '[STUDENT]', redacted_text)
        email_pattern = r'\b[\w\.-]+@[\w\.-]+\.\w+\b'
        redacted_text = re.sub(email_pattern, '[EMAIL]', redacted_text)
        return {
            'original': text,
            'redacted': redacted_text,
            'pii_removed': len(re.findall(name_pattern, text)) + len(re.findall(email_pattern, text)),
            'compliance_note': 'Designed with FERPA/COPPA data-minimisation principles. '
                              'AI Shiksha is a prototype; no compliance claim is made.'
        }


# ==================== PROFESSIONAL DATA MODELS ====================

@dataclass
class SourceDocument:
    id: str
    title: str
    source_type: str
    file_path: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    citations: List[Dict[str, Any]] = field(default_factory=list)
    parsed_tables: List[Dict[str, Any]] = field(default_factory=list)
    uploaded_at: datetime = field(default_factory=datetime.now)


@dataclass
class Citation:
    id: str
    document_id: str
    page_number: int
    paragraph: str
    claim: str
    confidence: float
    source_text: str


@dataclass
class PortfolioAsset:
    ticker: str
    name: str
    sector: str
    shares: int
    purchase_price: float
    current_price: float
    market_value: float
    weight: float
    daily_change: float
    weekly_change: float
    monthly_change: float


@dataclass
class WatchdogAlert:
    id: str
    asset_ticker: str
    alert_type: str
    severity: str
    message: str
    source: str
    timestamp: datetime
    read: bool = False


@dataclass
class MacroScenario:
    name: str
    description: str
    rate_change: float
    inflation_change: float
    growth_change: float
    market_shock: float
    portfolio_impact: float


class SearchType(Enum):
    HYBRID = "hybrid"
    VECTOR = "vector"
    KEYWORD = "keyword"
    SEMANTIC = "semantic"


# ==================== PROFESSIONAL INTELLIGENCE ENGINE ====================

class ProfessionalIntelligenceEngine:
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.documents = []
        self.citations = []
        self.portfolio_assets = []
        self.watchdog_alerts = []
        self.analysis_history = []
        self.search_index = {}
        self.vector_embeddings = {}
        self._initialize_sample_data()

    def _initialize_sample_data(self):
        sample_docs = [
            {
                'id': 'doc_001',
                'title': 'Q4 2024 Earnings Report - TechCorp',
                'source_type': 'sec_filing',
                'content': """TechCorp Q4 2024 earnings exceeded analyst expectations. 
                Revenue reached $12.4 billion, up 18% year-over-year. 
                EPS of $2.15 beat estimates of $1.95. 
                Cloud revenue grew 32% to $4.2 billion. 
                Operating margin expanded to 28.5% from 26.1%.""",
                'metadata': {'filing_date': '2025-01-15', 'quarter': 'Q4 2024', 'company': 'TechCorp'},
                'citations': [
                    {'page': 2, 'paragraph': 3, 'claim': 'Revenue reached $12.4 billion', 'confidence': 0.95},
                ]
            },
        ]
        for doc_data in sample_docs:
            doc = SourceDocument(
                id=doc_data['id'], title=doc_data['title'], source_type=doc_data['source_type'],
                file_path=f"{doc_data['id']}.pdf", content=doc_data['content'],
                metadata=doc_data['metadata'], citations=doc_data['citations']
            )
            self.documents.append(doc)

        sample_assets = [
            PortfolioAsset('AAPL', 'Apple Inc.', 'Technology', 100, 150.00, 175.50, 17550.00, 0.25, 0.02, 0.05, 0.12),
            PortfolioAsset('MSFT', 'Microsoft Corp.', 'Technology', 50, 330.00, 380.00, 19000.00, 0.27, 0.015, 0.04, 0.10),
            PortfolioAsset('GOOGL', 'Alphabet Inc.', 'Technology', 75, 140.00, 155.00, 11625.00, 0.17, 0.01, 0.03, 0.08),
            PortfolioAsset('AMZN', 'Amazon.com Inc.', 'Consumer', 30, 185.00, 195.00, 5850.00, 0.08, -0.005, 0.02, 0.05),
            PortfolioAsset('NVDA', 'NVIDIA Corp.', 'Technology', 40, 450.00, 520.00, 20800.00, 0.30, 0.03, 0.08, 0.25),
        ]
        self.portfolio_assets = sample_assets

        sample_alerts = [
            WatchdogAlert('alert_001', 'AAPL', 'news', 'medium',
                          'Apple announces new AI product line - potential growth catalyst',
                          'Reuters', datetime.now() - timedelta(hours=2)),
            WatchdogAlert('alert_002', 'NVDA', 'earnings', 'high',
                          'NVIDIA earnings due next week - expected to beat estimates',
                          'Bloomberg', datetime.now() - timedelta(hours=5)),
        ]
        self.watchdog_alerts = sample_alerts

    def ingest_document(self, file_content: str, file_name: str, source_type: str,
                        metadata: Dict = None) -> SourceDocument:
        doc_id = f"doc_{hashlib.md5(file_name.encode()).hexdigest()[:8]}"
        doc = SourceDocument(
            id=doc_id, title=file_name, source_type=source_type,
            file_path=file_name, content=file_content,
            metadata=metadata or {}, uploaded_at=datetime.now()
        )
        doc.citations = self._extract_citations(file_content)
        doc.parsed_tables = self._extract_tables(file_content)
        self.documents.append(doc)
        self._index_document(doc)
        return doc

    def _extract_citations(self, content: str) -> List[Dict[str, Any]]:
        citations = []
        lines = content.split('\n')
        for i, line in enumerate(lines):
            claims = re.findall(
                r'([A-Z][^.!?]*\s+(?:was|is|reached|grew|increased|decreased|fell|rose|were)\s+[^.!?]*\d+[^.!?]*)',
                line
            )
            for claim in claims:
                if len(claim) > 20:
                    citations.append({
                        'page': i // 40 + 1,
                        'paragraph': i + 1,
                        'claim': claim.strip(),
                        'confidence': 0.85
                    })
        return citations[:10]

    def _extract_tables(self, content: str) -> List[Dict[str, Any]]:
        tables = []
        lines = content.split('\n')
        table_data = []
        for line in lines:
            if '|' in line or '\t' in line:
                parts = re.split(r'[|\t]+', line)
                if len(parts) > 2:
                    table_data.append([p.strip() for p in parts if p.strip()])
        if table_data:
            tables.append({
                'rows': len(table_data),
                'columns': len(table_data[0]) if table_data else 0,
                'data': table_data
            })
        return tables

    def _index_document(self, doc: SourceDocument):
        words = re.findall(r'\b[a-zA-Z]{3,}\b', doc.content.lower())
        for word in words:
            if word not in self.search_index:
                self.search_index[word] = []
            self.search_index[word].append(doc.id)

    def hybrid_search(self, query: str, search_type: SearchType = SearchType.HYBRID) -> List[Dict[str, Any]]:
        results = []
        query_words = re.findall(r'\b[a-zA-Z]{3,}\b', query.lower())

        keyword_results = {}
        for word in query_words:
            if word in self.search_index:
                for doc_id in self.search_index[word]:
                    keyword_results[doc_id] = keyword_results.get(doc_id, 0) + 1

        vector_results = {}
        for doc in self.documents:
            doc_words = re.findall(r'\b[a-zA-Z]{3,}\b', doc.content.lower())
            overlap = len(set(query_words) & set(doc_words))
            if overlap > 0:
                vector_results[doc.id] = overlap / len(set(query_words) | set(doc_words))

        all_doc_ids = set(keyword_results.keys()) | set(vector_results.keys())
        for doc_id in all_doc_ids:
            doc = next((d for d in self.documents if d.id == doc_id), None)
            if doc:
                keyword_score = keyword_results.get(doc_id, 0) / max(1, len(query_words))
                vector_score = vector_results.get(doc_id, 0)
                if search_type == SearchType.KEYWORD:
                    final_score = keyword_score
                elif search_type == SearchType.VECTOR:
                    final_score = vector_score
                elif search_type == SearchType.SEMANTIC:
                    final_score = vector_score * 0.7 + keyword_score * 0.3
                else:
                    final_score = keyword_score * 0.4 + vector_score * 0.6
                if final_score > 0.1:
                    results.append({
                        'document': doc,
                        'score': round(final_score, 3),
                        'matches': list(set(query_words) & set(re.findall(r'\b[a-zA-Z]{3,}\b', doc.content.lower())))
                    })

        sorted_results = sorted(results, key=lambda x: x['score'], reverse=True)
        return _transparency().attach({'results': sorted_results}, "professional.research_engine").get('results', sorted_results)

    def generate_citation_chain(self, claim: str, document_id: str) -> List[Dict[str, Any]]:
        doc = next((d for d in self.documents if d.id == document_id), None)
        if not doc:
            return []
        citations = []
        for citation in doc.citations:
            if claim.lower() in citation['claim'].lower() or any(
                word in citation['claim'].lower() for word in claim.lower().split()[:5]
            ):
                citations.append({
                    'claim': citation['claim'],
                    'page': citation.get('page', 1),
                    'paragraph': citation.get('paragraph', 1),
                    'confidence': citation.get('confidence', 0.85),
                    'source_text': doc.content.split('\n')[citation.get('paragraph', 1) - 1]
                                    if citation.get('paragraph') else ''
                })
        return citations

    def audit_analysis(self, analysis_text: str, source_documents: List[SourceDocument]) -> Dict[str, Any]:
        audit_results = {
            'verified_claims': [],
            'unverified_claims': [],
            'citations_generated': [],
            'confidence_score': 0.0
        }
        claims = re.findall(
            r'([A-Z][^.!?]*\s+(?:was|is|reached|grew|increased|decreased|fell|rose|were|will|would|could|should)\s+[^.!?]*\d+[^.!?]*)',
            analysis_text
        )
        for claim in claims:
            verified = False
            for doc in source_documents:
                if claim.lower() in doc.content.lower():
                    citations = self.generate_citation_chain(claim, doc.id)
                    if citations:
                        audit_results['verified_claims'].append({
                            'claim': claim, 'source': doc.title, 'citations': citations
                        })
                        audit_results['citations_generated'].extend(citations)
                        verified = True
                        break
            if not verified:
                audit_results['unverified_claims'].append(claim)
        audit_results['confidence_score'] = len(audit_results['verified_claims']) / max(1, len(claims))
        return audit_results

    def execute_quant_analysis(self, code: str, data: pd.DataFrame) -> Dict[str, Any]:
        # SECURITY: exec() disabled in prototype. Production will use subprocess sandbox.
        return {
            'status': 'not_available',
            'message': 'Code execution is disabled in the prototype for security reasons.',
            'note': 'A production version would use an isolated subprocess sandbox.',
            'execution_time': 0.0
        }

    def fetch_market_data(self, ticker: str) -> Dict[str, Any]:
        # Deterministic seed for reproducibility within a session day
        seed = int(datetime.now().strftime("%Y%m%d")) + hash(ticker) % 10000
        rng = random.Random(seed)
        base_price = rng.uniform(100, 500)
        result = {
            'ticker': ticker,
            'price': round(base_price, 2),
            'change': round(rng.uniform(-5, 5), 2),
            'change_percent': round(rng.uniform(-3, 3), 2),
            'volume': rng.randint(1000000, 10000000),
            'high': round(base_price * rng.uniform(1.01, 1.05), 2),
            'low': round(base_price * rng.uniform(0.95, 0.99), 2),
            'timestamp': datetime.now().isoformat(),
            'note': 'Simulated data for prototype demonstration.'
        }
        return result

    def fetch_sec_filing(self, ticker: str) -> Dict[str, Any]:
        filings = [
            {'type': '10-K', 'date': '2025-01-15', 'title': 'Annual Report'},
            {'type': '10-Q', 'date': '2025-01-10', 'title': 'Quarterly Report'},
            {'type': '8-K', 'date': '2025-01-05', 'title': 'Current Report'},
            {'type': 'DEF 14A', 'date': '2025-01-02', 'title': 'Proxy Statement'}
        ]
        seed = int(datetime.now().strftime("%Y%m%d")) + hash(ticker) % 100
        rng = random.Random(seed)
        return {
            'ticker': ticker,
            'filings': [f for f in filings if rng.random() > 0.5],
            'timestamp': datetime.now().isoformat(),
            'note': 'Simulated data for prototype demonstration.'
        }

    def fetch_earnings_call(self, ticker: str) -> Dict[str, Any]:
        return {
            'ticker': ticker,
            'quarter': 'Q4 2024',
            'date': '2025-01-20',
            'transcript': f"Earnings call transcript for {ticker}. Revenue exceeded expectations...",
            'highlights': ['Revenue beat by 5%', 'EPS exceeded guidance', 'Forward guidance raised'],
            'timestamp': datetime.now().isoformat(),
            'note': 'Simulated data for prototype demonstration.'
        }

    def calculate_portfolio_metrics(self) -> Dict[str, Any]:
        total_value = sum(asset.market_value for asset in self.portfolio_assets)
        sector_exposure = {}
        for asset in self.portfolio_assets:
            sector_exposure[asset.sector] = sector_exposure.get(asset.sector, 0) + asset.weight
        returns = [asset.daily_change for asset in self.portfolio_assets]
        volatility = float(np.std(returns)) if returns else 0
        tracking_error = round(volatility * 0.5, 4)
        return {
            'total_value': round(total_value, 2),
            'sector_exposure': sector_exposure,
            'volatility': round(volatility, 4),
            'tracking_error': tracking_error,
            'sharpe_ratio': round((0.1 - 0.03) / max(0.01, volatility), 2),
            'concentration_risk': round(max(sector_exposure.values()) if sector_exposure else 0, 2)
        }

    def run_watchdog_alerts(self) -> List[WatchdogAlert]:
        # Deterministic seed for reproducibility
        seed = int(datetime.now().strftime("%Y%m%d"))
        rng = random.Random(seed)
        new_alerts = []
        for asset in self.portfolio_assets:
            if rng.random() > 0.85:
                alert = WatchdogAlert(
                    id=f"alert_{seed}_{asset.ticker}_earnings",
                    asset_ticker=asset.ticker, alert_type='earnings', severity='high',
                    message=f'Earnings announcement for {asset.ticker} expected tomorrow',
                    source='SEC EDGAR', timestamp=datetime.now()
                )
                new_alerts.append(alert)
            if rng.random() > 0.9:
                alert = WatchdogAlert(
                    id=f"alert_{seed}_{asset.ticker}_price",
                    asset_ticker=asset.ticker, alert_type='price', severity='medium',
                    message=f'{asset.ticker} price {"up" if rng.random() > 0.5 else "down"} significantly',
                    source='Market Feed', timestamp=datetime.now()
                )
                new_alerts.append(alert)
        self.watchdog_alerts.extend(new_alerts)
        return new_alerts

    def run_macro_stress_test(self, scenario: MacroScenario) -> Dict[str, Any]:
        portfolio_value = sum(asset.market_value for asset in self.portfolio_assets)
        rate_impact = scenario.rate_change * 0.5
        inflation_impact = scenario.inflation_change * 0.3
        growth_impact = scenario.growth_change * 0.4
        market_impact = scenario.market_shock * 0.7
        total_impact = rate_impact + inflation_impact + growth_impact + market_impact
        impacted_value = portfolio_value * (1 + total_impact)
        asset_impacts = []
        for asset in self.portfolio_assets:
            sector_multiplier = {
                'Technology': 0.2, 'Consumer': 0.15, 'Financial': 0.25,
                'Healthcare': 0.1, 'Energy': 0.3
            }.get(asset.sector, 0.15)
            asset_impact = total_impact * sector_multiplier
            impacted_asset_value = asset.market_value * (1 + asset_impact)
            asset_impacts.append({
                'ticker': asset.ticker,
                'current_value': asset.market_value,
                'impacted_value': impacted_asset_value,
                'impact_percent': asset_impact * 100
            })
        return {
            'portfolio_name': 'Professional Portfolio',
            'scenario_name': scenario.name,
            'current_value': portfolio_value,
            'impacted_value': impacted_value,
            'total_return': total_impact * 100,
            'asset_impacts': asset_impacts,
            'risk_assessment': 'High' if abs(total_impact) > 0.2 else 'Medium' if abs(total_impact) > 0.1 else 'Low'
        }

    def generate_deliverable(self, template_type: str, data: Dict[str, Any]) -> str:
        templates = {
            'investment_memo': """
            # Investment Committee Memo
            **Date:** {date}
            **Analyst:** {analyst}
            ## Executive Summary
            {summary}
            ## Investment Thesis
            {thesis}
            ## Risk Analysis
            {risks}
            ## Recommendation
            **Action:** {action}
            **Target Price:** {target_price}
            """,
            'research_note': """
            # Research Note: {title}
            **Date:** {date}
            **Analyst:** {analyst}
            ## Key Findings
            {findings}
            ## Conclusion
            {conclusion}
            """
        }
        template = templates.get(template_type, templates['investment_memo'])
        try:
            return template.format(**data)
        except Exception:
            return template

    def extract_table_from_pdf(self, pdf_content: str) -> pd.DataFrame:
        lines = pdf_content.split('\n')
        table_data = []
        headers = None
        for line in lines:
            if '|' in line or '\t' in line:
                parts = [p.strip() for p in re.split(r'[|\t]+', line) if p.strip()]
                if parts:
                    if not headers:
                        headers = parts[:len(parts)]
                    else:
                        table_data.append(parts[:len(headers)])
        if table_data and headers:
            return pd.DataFrame(table_data, columns=headers)
        return pd.DataFrame({
            'Metric': ['Revenue', 'EBITDA', 'Net Income', 'EPS'],
            'Q4 2024': ['$12.4B', '$3.5B', '$2.1B', '$2.15'],
            'Q4 2023': ['$10.5B', '$2.8B', '$1.7B', '$1.75'],
            'Change': ['+18%', '+25%', '+24%', '+23%']
        })

    def get_workspace_data(self) -> Dict[str, Any]:
        return {
            'documents': [
                {'id': doc.id, 'title': doc.title, 'type': doc.source_type,
                 'content': doc.content[:500] + ('...' if len(doc.content) > 500 else '')}
                for doc in self.documents
            ],
            'citations': self.citations,
            'analysis_history': self.analysis_history,
            'portfolio_data': self.calculate_portfolio_metrics()
        }


# ==================== SME DATA MODELS ====================

@dataclass
class BusinessMetric:
    name: str
    value: float
    change: float
    trend: str
    category: str
    timestamp: datetime


@dataclass
class ActionTask:
    id: str
    title: str
    description: str
    priority: str
    category: str
    impact: str
    action_type: str
    status: str
    created_at: datetime
    due_date: Optional[datetime] = None


@dataclass
class WebhookEvent:
    event_type: str
    payload: Dict[str, Any]
    timestamp: datetime
    processed: bool = False


class PriorityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


# ==================== SME INFRASTRUCTURE ENGINE ====================

class SMEInfrastructureEngine:
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.webhook_events = []
        self.api_connections = {}
        self.etl_pipeline_data = {}

    def etl_process(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            extracted = self._extract_data(raw_data)
            transformed = self._transform_data(extracted)
            loaded = self._load_data(transformed)
            return {'status': 'success', 'extracted': extracted,
                    'transformed': transformed, 'loaded': loaded,
                    'timestamp': datetime.now().isoformat()}
        except Exception as e:
            return {'status': 'error', 'error': str(e), 'timestamp': datetime.now().isoformat()}

    def _extract_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        extracted = {}
        for key in ['transactions', 'invoices', 'inventory', 'customers']:
            if key in raw_data:
                extracted[key] = raw_data[key]
        for key in extracted:
            if isinstance(extracted[key], list):
                extracted[key] = self._normalize_list(extracted[key])
        return extracted

    def _normalize_list(self, data_list: List[Dict]) -> List[Dict]:
        normalized = []
        for item in data_list:
            if 'amount' in item and 'total' not in item:
                item['total'] = item['amount']
            if 'qty' in item and 'quantity' not in item:
                item['quantity'] = item['qty']
            normalized.append(item)
        return normalized

    def _transform_data(self, extracted: Dict[str, Any]) -> Dict[str, Any]:
        transformed = {}
        if 'transactions' in extracted:
            t = extracted['transactions']
            transformed['total_revenue'] = sum(x.get('total', 0) for x in t)
            transformed['transaction_count'] = len(t)
            transformed['average_transaction'] = transformed['total_revenue'] / max(1, len(t))
        if 'inventory' in extracted:
            inv = extracted['inventory']
            transformed['total_inventory_items'] = len(inv)
            transformed['low_stock_items'] = [i for i in inv if i.get('quantity', 0) < i.get('threshold', 10)]
            transformed['out_of_stock_items'] = [i for i in inv if i.get('quantity', 0) <= 0]
        if 'customers' in extracted:
            c = extracted['customers']
            transformed['total_customers'] = len(c)
            transformed['repeat_customers'] = [x for x in c if x.get('orders', 0) > 1]
        return transformed

    def _load_data(self, transformed: Dict[str, Any]) -> Dict[str, Any]:
        self.etl_pipeline_data.update(transformed)
        return transformed

    def connect_api(self, service: str, credentials: Dict[str, str]) -> Dict[str, Any]:
        api_configs = {
            'stripe': {'name': 'Stripe', 'icon': '💳', 'endpoints': ['payments', 'invoices', 'customers', 'subscriptions'], 'auth_type': 'api_key'},
            'quickbooks': {'name': 'QuickBooks', 'icon': '📊', 'endpoints': ['invoices', 'expenses', 'customers', 'reports'], 'auth_type': 'oauth2'},
            'shopify': {'name': 'Shopify', 'icon': '🛍️', 'endpoints': ['orders', 'products', 'customers', 'inventory'], 'auth_type': 'api_key'},
            'toast': {'name': 'Toast POS', 'icon': '🍽️', 'endpoints': ['orders', 'menu', 'inventory', 'reports'], 'auth_type': 'api_key'},
            'jobber': {'name': 'Jobber', 'icon': '🔧', 'endpoints': ['clients', 'invoices', 'visits', 'schedule'], 'auth_type': 'oauth2'}
        }
        if service in api_configs:
            self.api_connections[service] = {
                'config': api_configs[service], 'credentials': credentials,
                'connected': True, 'last_sync': datetime.now().isoformat()
            }
            return {'status': 'connected', 'service': service,
                    'message': f"Successfully connected to {api_configs[service]['name']}"}
        return {'status': 'error', 'service': service, 'message': f"Unsupported API service: {service}"}

    def fetch_api_data(self, service: str, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        if service not in self.api_connections:
            return {'status': 'error', 'message': f"Service {service} not connected"}
        mock_data = {
            'payments': [
                {'id': 1, 'amount': 150.00, 'status': 'paid', 'date': '2024-01-15'},
                {'id': 2, 'amount': 75.50, 'status': 'paid', 'date': '2024-01-14'},
            ],
            'invoices': [
                {'id': 'INV-001', 'amount': 150.00, 'status': 'paid', 'due_date': '2024-01-20'},
                {'id': 'INV-002', 'amount': 75.50, 'status': 'overdue', 'due_date': '2024-01-10'},
            ],
            'orders': [
                {'id': 'ORD-001', 'total': 150.00, 'status': 'fulfilled', 'items': 3},
            ],
            'inventory': [
                {'id': 'SKU-001', 'name': 'Product A', 'quantity': 45, 'threshold': 50},
                {'id': 'SKU-002', 'name': 'Product B', 'quantity': 12, 'threshold': 20},
            ]
        }
        return {'status': 'success', 'service': service, 'endpoint': endpoint,
                'data': mock_data.get(endpoint, []), 'timestamp': datetime.now().isoformat()}

    def process_webhook(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        event = WebhookEvent(event_type=event_type, payload=payload, timestamp=datetime.now())
        self.webhook_events.append(event)
        handlers = {
            'checkout.paid': self._handle_checkout_paid,
            'invoice.overdue': self._handle_invoice_overdue,
            'inventory.low': self._handle_inventory_low,
            'customer.churn_risk': self._handle_customer_churn_risk
        }
        handler = handlers.get(event_type)
        if handler:
            return handler(event)
        return {'status': 'unhandled', 'event_type': event_type}

    def _handle_checkout_paid(self, event: WebhookEvent) -> Dict[str, Any]:
        amount = event.payload.get('amount', 0)
        customer = event.payload.get('customer', {})
        task = ActionTask(
            id=f"task_{datetime.now().timestamp()}",
            title="New Payment Received",
            description=f"Payment of ${amount:.2f} received from {customer.get('name', 'Customer')}",
            priority='low', category='finance', impact=f"+${amount:.2f} revenue",
            action_type='auto', status='approved', created_at=datetime.now()
        )
        return {'status': 'processed', 'event_type': 'checkout.paid',
                'action_task': task, 'message': 'Payment processed successfully'}

    def _handle_invoice_overdue(self, event: WebhookEvent) -> Dict[str, Any]:
        invoice_id = event.payload.get('invoice_id', 'unknown')
        amount = event.payload.get('amount', 0)
        days_overdue = event.payload.get('days_overdue', 0)
        task = ActionTask(
            id=f"task_{datetime.now().timestamp()}",
            title=f"Invoice {invoice_id} is {days_overdue} days overdue",
            description=f"Client payment of ${amount:.2f} is overdue. Send payment reminder.",
            priority='high', category='finance', impact=f"Potential loss of ${amount:.2f}",
            action_type='approval', status='pending', created_at=datetime.now(),
            due_date=datetime.now() + timedelta(days=1)
        )
        return {'status': 'processed', 'event_type': 'invoice.overdue',
                'action_task': task, 'message': 'Overdue invoice alert created'}

    def _handle_inventory_low(self, event: WebhookEvent) -> Dict[str, Any]:
        product = event.payload.get('product', {})
        current_qty = event.payload.get('current_qty', 0)
        threshold = event.payload.get('threshold', 0)
        price = product.get('price', 0)
        potential_loss = (threshold - current_qty) * price
        task = ActionTask(
            id=f"task_{datetime.now().timestamp()}",
            title=f"Low Stock Alert: {product.get('name', 'Product')}",
            description=f"Current stock: {current_qty} units. Threshold: {threshold}. Restock now.",
            priority='critical', category='inventory',
            impact=f"Prevent ${potential_loss:.2f} lost revenue",
            action_type='approval', status='pending', created_at=datetime.now(),
            due_date=datetime.now() + timedelta(hours=12)
        )
        return {'status': 'processed', 'event_type': 'inventory.low',
                'action_task': task, 'message': 'Inventory alert created'}

    def _handle_customer_churn_risk(self, event: WebhookEvent) -> Dict[str, Any]:
        customer = event.payload.get('customer', {})
        churn_score = event.payload.get('churn_score', 0)
        days_inactive = event.payload.get('days_inactive', 0)
        task = ActionTask(
            id=f"task_{datetime.now().timestamp()}",
            title=f"Churn Risk: {customer.get('name', 'Customer')}",
            description=f"Customer inactive for {days_inactive} days. Churn score: {churn_score:.1%}",
            priority='high', category='customers',
            impact=f"Potential loss of ${customer.get('ltv', 0):.2f} LTV",
            action_type='draft', status='pending', created_at=datetime.now()
        )
        return {'status': 'processed', 'event_type': 'customer.churn_risk',
                'action_task': task, 'message': 'Churn risk alert created'}


# ==================== SME AI ENGINE ====================

class SMEAIEngine:
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.infrastructure = SMEInfrastructureEngine(country_code)

    def predict_cash_flow(self, historical_data: List[Dict]) -> Dict[str, Any]:
        # Deterministic seed within a day
        seed = int(datetime.now().strftime("%Y%m%d"))
        rng = random.Random(seed)
        days = 30
        current_balance = 5000
        predictions = []
        for i in range(days):
            daily_inflow = rng.uniform(100, 500)
            daily_outflow = rng.uniform(50, 300)
            current_balance += daily_inflow - daily_outflow
            predictions.append({
                'day': i + 1,
                'date': (datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d'),
                'balance': round(current_balance, 2),
                'inflow': round(daily_inflow, 2),
                'outflow': round(daily_outflow, 2)
            })
        min_balance = min(p['balance'] for p in predictions)
        min_balance_day = next(p['day'] for p in predictions if p['balance'] == min_balance)
        result = {
            'predictions': predictions,
            'min_balance': round(min_balance, 2),
            'min_balance_day': min_balance_day,
            'avg_daily_balance': round(sum(p['balance'] for p in predictions) / days, 2),
            'risk_level': 'high' if min_balance < 1000 else 'medium' if min_balance < 3000 else 'low',
            'note': 'Simulated forecast for prototype. Deterministic within a single day.'
        }
        return result

    def predict_churn(self, customer_data: List[Dict]) -> List[Dict]:
        predictions = []
        for customer in customer_data[:10]:
            days_since_last_order = customer.get('days_since_last_order', 0)
            order_count = customer.get('order_count', 0)
            churn_score = min(1.0, (days_since_last_order / 90) * 0.7 + (1 - min(1, order_count / 5)) * 0.3)
            predictions.append({
                'customer_id': customer.get('id', 'unknown'),
                'name': customer.get('name', 'Unknown'),
                'churn_score': round(churn_score, 3),
                'risk_level': 'high' if churn_score > 0.6 else 'medium' if churn_score > 0.3 else 'low',
                'recommendation': self._get_churn_recommendation(churn_score)
            })
        return sorted(predictions, key=lambda x: x['churn_score'], reverse=True)

    def _get_churn_recommendation(self, churn_score: float) -> str:
        if churn_score > 0.7:
            return "🚨 Immediate intervention: Personalized offer needed"
        elif churn_score > 0.5:
            return "⚠️ Send re-engagement email with special discount"
        elif churn_score > 0.3:
            return "📧 Send regular engagement content"
        return "✅ Keep doing what you're doing"

    def predict_inventory_depletion(self, inventory_data: List[Dict]) -> List[Dict]:
        predictions = []
        for item in inventory_data:
            current_qty = item.get('quantity', 0)
            daily_sales_avg = item.get('daily_sales_avg', 1)
            threshold = item.get('threshold', 10)
            if daily_sales_avg > 0:
                days_until_depletion = current_qty / daily_sales_avg
                days_until_threshold = max(0, (current_qty - threshold) / daily_sales_avg)
            else:
                days_until_depletion = 999
                days_until_threshold = 999
            predictions.append({
                'product_id': item.get('id', 'unknown'),
                'name': item.get('name', 'Unknown'),
                'current_qty': current_qty,
                'days_until_depletion': round(days_until_depletion, 1),
                'days_until_threshold': round(days_until_threshold, 1),
                'status': 'critical' if days_until_threshold < 3 else 'warning' if days_until_threshold < 7 else 'ok',
                'restock_quantity': max(threshold * 2 - current_qty, 0)
            })
        return sorted(predictions, key=lambda x: x['days_until_threshold'])

    def predict_customer_ltv(self, customer_data: List[Dict]) -> List[Dict]:
        predictions = []
        for customer in customer_data[:10]:
            avg_order = customer.get('avg_order_value', 50)
            frequency = customer.get('frequency', 1)
            months = customer.get('months_active', 6)
            current_ltv = avg_order * frequency * months
            projected_ltv = avg_order * frequency * 24
            predictions.append({
                'customer_id': customer.get('id', 'unknown'),
                'name': customer.get('name', 'Unknown'),
                'current_ltv': round(current_ltv, 2),
                'projected_ltv': round(projected_ltv, 2),
                'potential_increase': round(projected_ltv - current_ltv, 2),
                'segment': 'high' if projected_ltv > 1000 else 'medium' if projected_ltv > 500 else 'low'
            })
        return sorted(predictions, key=lambda x: x['projected_ltv'], reverse=True)

    def natural_language_query(self, query: str, data_context: Dict[str, Any]) -> Dict[str, Any]:
        query_lower = query.lower()
        response = {
            'query': query,
            'timestamp': datetime.now().isoformat(),
            'results': []
        }
        if 'cash' in query_lower or 'balance' in query_lower:
            cash_flow = self.predict_cash_flow([])
            response['results'].append({
                'type': 'cash_flow', 'data': cash_flow,
                'summary': f"Your current cash flow projection shows a minimum balance of "
                           f"${cash_flow['min_balance']:.2f} on day {cash_flow['min_balance_day']}. "
                           f"Risk level: {cash_flow['risk_level']}."
            })
        if 'inventory' in query_lower or 'stock' in query_lower:
            inventory_data = [
                {'id': 'SKU-001', 'name': 'Product A', 'quantity': 45, 'threshold': 50, 'daily_sales_avg': 2},
                {'id': 'SKU-002', 'name': 'Product B', 'quantity': 12, 'threshold': 20, 'daily_sales_avg': 1.5},
                {'id': 'SKU-003', 'name': 'Product C', 'quantity': 3, 'threshold': 10, 'daily_sales_avg': 1}
            ]
            predictions = self.predict_inventory_depletion(inventory_data)
            critical_items = [p for p in predictions if p['status'] == 'critical']
            response['results'].append({
                'type': 'inventory', 'data': predictions,
                'summary': f"Found {len(critical_items)} items at critical stock levels."
            })
        if 'customer' in query_lower or 'churn' in query_lower:
            customer_data = [
                {'id': 1, 'name': 'John Doe', 'days_since_last_order': 45, 'avg_order_value': 75, 'order_count': 3},
                {'id': 2, 'name': 'Jane Smith', 'days_since_last_order': 12, 'avg_order_value': 120, 'order_count': 8},
            ]
            churn_predictions = self.predict_churn(customer_data)
            high_risk = [c for c in churn_predictions if c['risk_level'] == 'high']
            response['results'].append({
                'type': 'churn', 'data': churn_predictions,
                'summary': f"{len(high_risk)} customers at high churn risk."
            })
        if not response['results']:
            response['results'].append({
                'type': 'general', 'data': {},
                'summary': "I couldn't find specific data for your query. "
                           "Try asking about cash flow, revenue, inventory, or customers."
            })
        # Log the query
        _logger().log(
            system_id="sme.predictive_engine",
            segment="SME Business Owner",
            input_text=query,
            output_summary=response['results'][0].get('summary', '')[:200]
        )
        return _transparency().attach(response, "sme.predictive_engine")

    def validate_llm_output(self, output: Dict[str, Any], action_type: str) -> Dict[str, Any]:
        validation = {'valid': True, 'errors': [], 'warnings': [], 'corrected': {}}
        if action_type in ['invoice', 'payment', 'financial']:
            amount = output.get('amount', 0)
            if amount < 0:
                validation['valid'] = False
                validation['errors'].append("Amount cannot be negative")
            if amount > 100000:
                validation['warnings'].append("Large transaction amount - please verify")
        return validation


# ==================== SME PRODUCT UX ENGINE ====================

class SMEProductUXEngine:
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.infrastructure = SMEInfrastructureEngine(country_code)
        self.ai_engine = SMEAIEngine(country_code)
        self.tasks = []
        self.alert_history = []

    def generate_tasks(self, business_data: Dict[str, Any]) -> List[ActionTask]:
        tasks = []
        tasks.extend(self._generate_inventory_tasks(business_data))
        tasks.extend(self._generate_financial_tasks(business_data))
        tasks.extend(self._generate_customer_tasks(business_data))
        tasks.extend(self._generate_marketing_tasks(business_data))
        tasks.extend(self._generate_operations_tasks(business_data))
        priority_order = {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}
        tasks.sort(key=lambda t: priority_order.get(t.priority, 4))
        self.tasks = tasks
        return tasks

    def _generate_inventory_tasks(self, data: Dict) -> List[ActionTask]:
        tasks = []
        for item in data.get('inventory', []):
            qty = item.get('quantity', 0)
            threshold = item.get('threshold', 10)
            price = item.get('price', 0)
            if qty <= 0:
                potential_loss = threshold * price
                tasks.append(ActionTask(
                    id=f"inv_{item.get('id', 'unknown')}_{datetime.now().timestamp()}",
                    title=f"🚨 OUT OF STOCK: {item.get('name', 'Product')}",
                    description=f"Critical! No stock remaining. Order now to prevent ${potential_loss:.2f} lost revenue.",
                    priority='critical', category='inventory',
                    impact=f"Prevent ${potential_loss:.2f} lost sales",
                    action_type='approval', status='pending', created_at=datetime.now(),
                    due_date=datetime.now() + timedelta(hours=6)
                ))
            elif qty < threshold:
                potential_loss = (threshold - qty) * price
                tasks.append(ActionTask(
                    id=f"inv_{item.get('id', 'unknown')}_{datetime.now().timestamp()}",
                    title=f"⚠️ Low Stock: {item.get('name', 'Product')}",
                    description=f"Only {qty} units remaining (Threshold: {threshold}). Restock to maintain availability.",
                    priority='high', category='inventory',
                    impact=f"Prevent ${potential_loss:.2f} lost revenue",
                    action_type='draft', status='pending', created_at=datetime.now(),
                    due_date=datetime.now() + timedelta(days=1)
                ))
        return tasks

    def _generate_financial_tasks(self, data: Dict) -> List[ActionTask]:
        tasks = []
        for inv in data.get('invoices', []):
            if inv.get('status') == 'overdue':
                tasks.append(ActionTask(
                    id=f"fin_{inv.get('id', 'unknown')}_{datetime.now().timestamp()}",
                    title=f"💳 Overdue Payment: {inv.get('id', 'Invoice')}",
                    description=f"Payment of ${inv.get('amount', 0):.2f} is overdue. Send reminder to customer.",
                    priority='high', category='finance',
                    impact=f"Recover ${inv.get('amount', 0):.2f}",
                    action_type='approval', status='pending', created_at=datetime.now(),
                    due_date=datetime.now() + timedelta(days=2)
                ))
        cash_flow = self.ai_engine.predict_cash_flow([])
        if cash_flow['risk_level'] == 'high':
            tasks.append(ActionTask(
                id=f"fin_cash_{datetime.now().timestamp()}",
                title=f"💰 Cash Flow Alert: ${cash_flow['min_balance']:.2f} minimum projected",
                description=f"Cash flow projected to drop to ${cash_flow['min_balance']:.2f} in {cash_flow['min_balance_day']} days.",
                priority='critical', category='finance', impact="Avoid cash shortage",
                action_type='alert', status='pending', created_at=datetime.now(),
                due_date=datetime.now() + timedelta(days=1)
            ))
        return tasks

    def _generate_customer_tasks(self, data: Dict) -> List[ActionTask]:
        tasks = []
        customers = data.get('customers', [])
        churn_predictions = self.ai_engine.predict_churn(customers[:10])
        for prediction in churn_predictions[:3]:
            if prediction['risk_level'] == 'high':
                tasks.append(ActionTask(
                    id=f"cust_{prediction.get('customer_id', 'unknown')}_{datetime.now().timestamp()}",
                    title=f"👤 Churn Risk: {prediction.get('name', 'Customer')}",
                    description=f"{prediction.get('name', 'Customer')} at {prediction['churn_score']*100:.0f}% churn risk.",
                    priority='high', category='customers', impact="Retain LTV",
                    action_type='draft', status='pending', created_at=datetime.now()
                ))
        return tasks

    def _generate_marketing_tasks(self, data: Dict) -> List[ActionTask]:
        # FIXED: f-string bug
        tasks = []
        opportunities = [
            {'title': "🎯 Email Campaign for Inactive Customers",
             'desc': "Send re-engagement email to customers inactive for 30+ days",
             'impact': "+15% customer retention"},
            {'title': "📱 Social Media Ad Boost",
             'desc': "Boost top-performing post to reach new audience",
             'impact': "+20% reach"},
        ]
        for opp in opportunities[:2]:
            key = hashlib.md5(opp['title'].encode()).hexdigest()[:8]
            ts = datetime.now().timestamp()
            tasks.append(ActionTask(
                id=f"mkt_{key}_{ts}",
                title=opp['title'], description=opp['desc'],
                priority='medium', category='marketing', impact=opp['impact'],
                action_type='draft', status='pending', created_at=datetime.now()
            ))
        return tasks

    def _generate_operations_tasks(self, data: Dict) -> List[ActionTask]:
        # FIXED: f-string bug
        tasks = []
        ops_tasks = [
            {'title': "📊 Monthly Financial Review",
             'desc': "Review and reconcile all accounts for month-end", 'priority': 'high'},
            {'title': "📋 Supplier Contract Renewal",
             'desc': "Review supplier contracts up for renewal next month", 'priority': 'medium'},
        ]
        for task in ops_tasks:
            key = hashlib.md5(task['title'].encode()).hexdigest()[:8]
            ts = datetime.now().timestamp()
            tasks.append(ActionTask(
                id=f"ops_{key}_{ts}",
                title=task['title'], description=task['desc'],
                priority=task['priority'], category='operations',
                impact="Improved operational efficiency",
                action_type='auto', status='pending', created_at=datetime.now(),
                due_date=datetime.now() + timedelta(days=7)
            ))
        return tasks

    def approve_task(self, task_id: str) -> Dict[str, Any]:
        for task in self.tasks:
            if task.id == task_id and task.status == 'pending':
                task.status = 'approved'
                return {'status': 'approved', 'task': task,
                        'message': f"Task '{task.title}' has been approved."}
        return {'status': 'error', 'message': 'Task not found or already processed'}

    def dismiss_task(self, task_id: str) -> Dict[str, Any]:
        for task in self.tasks:
            if task.id == task_id:
                task.status = 'dismissed'
                return {'status': 'dismissed', 'task': task,
                        'message': f"Task '{task.title}' dismissed"}
        return {'status': 'error', 'message': 'Task not found'}

    def generate_digest(self, channel: str = 'whatsapp') -> Dict[str, Any]:
        pending = [t for t in self.tasks if t.status == 'pending']
        priority_tasks = [t for t in pending if t.priority in ['critical', 'high']]
        digest = {
            'channel': channel,
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_tasks': len(pending),
                'critical_tasks': len([t for t in pending if t.priority == 'critical']),
                'high_tasks': len([t for t in pending if t.priority == 'high'])
            },
            'top_priorities': [
                {'title': t.title, 'description': t.description, 'impact': t.impact,
                 'due': t.due_date.strftime('%Y-%m-%d') if t.due_date else 'No deadline'}
                for t in priority_tasks[:5]
            ],
            'action_required': len(priority_tasks) > 0,
            'message': self._format_digest_message(channel, priority_tasks[:3])
        }
        self.alert_history.append(digest)
        return digest

    def _format_digest_message(self, channel: str, top_tasks: List[ActionTask]) -> str:
        if channel == 'whatsapp':
            pending = [t for t in self.tasks if t.status == 'pending']
            message = "📊 *AI Shiksha Daily Business Digest* 📊\n\n"
            message += f"📌 {len(pending)} pending tasks\n"
            message += f"🚨 {len([t for t in pending if t.priority == 'critical'])} critical tasks\n\n"
            if top_tasks:
                message += "*Top Priorities:*\n"
                for i, task in enumerate(top_tasks, 1):
                    message += f"{i}. {task.title}\n"
            else:
                message += "✅ No urgent tasks. You're on track! 🎉"
            return message
        return "Digest generated successfully"


# ==================== DOCUMENT INTELLIGENCE ENGINE ====================

class DocumentIntelligenceEngine:
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.context = LocalCurriculumOverlay.get_local_context(country_code)

    def extract_text_from_file(self, uploaded_file) -> str:
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            text = ""
            if file_extension == 'pdf':
                if PyPDF2 is None:
                    return "PDF support requires PyPDF2. Please install: pip install PyPDF2"
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            elif file_extension == 'docx':
                if docx is None:
                    return "DOCX support requires python-docx. Please install: pip install python-docx"
                doc = docx.Document(io.BytesIO(uploaded_file.read()))
                for para in doc.paragraphs:
                    text += para.text + "\n"
            elif file_extension in ['txt', 'csv', 'json']:
                text = uploaded_file.read().decode('utf-8')
            else:
                return f"Unsupported file format: {file_extension}. Please upload PDF, DOCX, TXT, CSV, or JSON."
            return text.strip() if text else "No text could be extracted from the document."
        except Exception as e:
            return f"Error extracting text: {str(e)}"

    def analyze_document(self, text: str, segment: str) -> Dict[str, Any]:
        analysis = {
            'word_count': len(text.split()),
            'char_count': len(text),
            'sentence_count': len(re.split(r'[.!?]+', text)),
            'key_phrases': self._extract_key_phrases(text),
            'sentiment': self._analyze_sentiment(text),
            'readability': self._calculate_readability(text),
            'country_context': self.country,
            'curriculum': self.overlay.get('system', 'Universal')
        }
        if segment == 'Student':
            analysis.update(self._analyze_student_document(text))
        elif segment == 'Teacher':
            analysis.update(self._analyze_teacher_document(text))
        elif segment == 'Professional':
            analysis.update(self._analyze_professional_document(text))
        elif segment == 'SME Business Owner':
            analysis.update(self._analyze_sme_document(text))
        return analysis

    def _extract_key_phrases(self, text: str) -> List[str]:
        stopwords = {'the', 'a', 'an', 'of', 'to', 'for', 'with', 'on', 'at', 'from', 'by', 'in', 'and', 'or', 'but'}
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        freq = {}
        for word in words:
            if word not in stopwords:
                freq[word] = freq.get(word, 0) + 1
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
        return [w[0] for w in sorted_words if len(w[0]) > 3][:7]

    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        positive_words = {'good', 'great', 'excellent', 'positive', 'achievement', 'success',
                          'improve', 'growth', 'happy', 'satisfied', 'excited', 'motivated'}
        negative_words = {'bad', 'poor', 'difficult', 'challenge', 'struggle', 'fail',
                          'failure', 'frustrating', 'disappointed', 'unhappy', 'stress'}
        words = text.lower().split()
        pos = sum(1 for w in words if w in positive_words)
        neg = sum(1 for w in words if w in negative_words)
        total = pos + neg
        if total == 0:
            return {'sentiment_score': 0, 'sentiment': 'Neutral'}
        score = (pos - neg) / total
        return {'sentiment_score': round(score, 2),
                'sentiment': 'Positive' if score > 0.1 else 'Negative' if score < -0.1 else 'Neutral'}

    def _calculate_readability(self, text: str) -> Dict[str, Any]:
        sentences = [s for s in re.split(r'[.!?]+', text) if len(s.strip()) > 0]
        words = text.split()
        if len(sentences) == 0 or len(words) == 0:
            return {'flesch_score': 0, 'grade_level': 'Unknown'}
        avg_wps = len(words) / len(sentences)
        avg_spw = self._count_syllables(text) / len(words)
        flesch_score = 206.835 - (1.015 * avg_wps) - (84.6 * avg_spw)
        if flesch_score >= 90:
            grade = '5th Grade (Very Easy)'
        elif flesch_score >= 80:
            grade = '6th Grade (Easy)'
        elif flesch_score >= 70:
            grade = '7th Grade (Fairly Easy)'
        elif flesch_score >= 60:
            grade = '8th-9th Grade (Plain English)'
        elif flesch_score >= 50:
            grade = '10th-12th Grade (Fairly Difficult)'
        elif flesch_score >= 30:
            grade = 'College (Difficult)'
        else:
            grade = 'College Graduate (Very Difficult)'
        return {'flesch_score': round(flesch_score, 2), 'grade_level': grade,
                'avg_words_per_sentence': round(avg_wps, 2)}

    def _count_syllables(self, text: str) -> int:
        vowels = 'aeiouy'
        count = 0
        for word in text.lower().split():
            wv = sum(1 for c in word if c in vowels)
            if word.endswith('e'):
                wv = max(1, wv - 1)
            count += max(1, wv)
        return count

    def _analyze_student_document(self, text: str) -> Dict[str, Any]:
        academic_keywords = {'analyze', 'evaluate', 'synthesize', 'discuss', 'compare',
                             'contrast', 'research', 'study', 'experiment', 'hypothesis'}
        words = text.lower().split()
        academic_count = sum(1 for w in words if w in academic_keywords)
        topics = self._extract_topics(text)
        return {
            'academic_language_score': round(min(100, (academic_count / len(words) * 1000)) if words else 0, 2),
            'topics_mentioned': topics[:5],
            'suggested_improvements': self._suggest_student_improvements(text, topics)
        }

    def _analyze_teacher_document(self, text: str) -> Dict[str, Any]:
        ped_keywords = {'objective', 'learning', 'outcome', 'assessment', 'rubric',
                        'activity', 'discussion', 'project', 'group', 'differentiation'}
        words = text.lower().split()
        ped_count = sum(1 for w in words if w in ped_keywords)
        has_objective = 'objective' in text.lower()
        has_assessment = 'assessment' in text.lower()
        has_activity = 'activity' in text.lower()
        has_standards = 'standard' in text.lower()
        completeness_score = sum([has_objective, has_assessment, has_activity, has_standards]) / 4 * 100
        return {
            'pedagogical_score': round(min(100, (ped_count / len(words) * 1000)) if words else 0, 2),
            'curriculum_alignment': self._check_curriculum_alignment(text),
            'suggested_enhancements': self._suggest_teacher_enhancements(text),
            'completeness_score': round(completeness_score, 2),
            'has_objective': has_objective,
            'has_assessment': has_assessment,
            'has_activity': has_activity,
            'has_standards': has_standards
        }

    def _analyze_professional_document(self, text: str) -> Dict[str, Any]:
        prof_keywords = {'strategy', 'analysis', 'implementation', 'results', 'findings',
                         'recommendation', 'efficiency', 'performance', 'portfolio', 'market'}
        words = text.lower().split()
        prof_count = sum(1 for w in words if w in prof_keywords)
        return {
            'professional_score': round(min(100, (prof_count / len(words) * 1000)) if words else 0, 2),
            'business_context': self._extract_business_context(text),
            'actionable_insights': self._extract_actionable_insights(text),
            'financial_metrics': self._extract_financial_metrics(text)
        }

    def _analyze_sme_document(self, text: str) -> Dict[str, Any]:
        sme_keywords = {'revenue', 'cost', 'profit', 'customer', 'market', 'growth',
                        'operations', 'supply', 'logistics', 'sales'}
        words = text.lower().split()
        sme_count = sum(1 for w in words if w in sme_keywords)
        return {
            'business_score': round(min(100, (sme_count / len(words) * 1000)) if words else 0, 2),
            'growth_opportunities': self._identify_growth_opportunities(text),
            'automation_candidates': self._identify_automation_candidates(text),
            'financial_metrics': self._extract_financial_metrics(text)
        }

    def _extract_topics(self, text: str) -> List[str]:
        common_topics = {
            'mathematics': ['algebra', 'geometry', 'calculus', 'statistics'],
            'science': ['biology', 'chemistry', 'physics', 'environment'],
            'literature': ['novel', 'poetry', 'drama', 'prose'],
            'history': ['historical', 'civilization', 'ancient', 'modern'],
            'geography': ['map', 'climate', 'population', 'region'],
            'economics': ['market', 'trade', 'investment', 'currency'],
            'technology': ['computer', 'software', 'digital', 'programming'],
            'language': ['vocabulary', 'grammar', 'writing', 'reading']
        }
        found = []
        text_lower = text.lower()
        for category, keywords in common_topics.items():
            if any(kw in text_lower for kw in keywords):
                found.append(category.title())
        return found

    def _suggest_student_improvements(self, text: str, topics: List[str]) -> List[str]:
        suggestions = []
        words = text.split()
        if len(words) < 100:
            suggestions.append("Consider expanding your analysis with more depth and examples.")
        elif len(words) > 1000:
            suggestions.append("Consider condensing your work for clarity and focus.")
        academic_words = {'analyze', 'evaluate', 'synthesize', 'compare', 'contrast'}
        if not any(w in text.lower() for w in academic_words):
            suggestions.append("Incorporate more academic language (analyze, evaluate, synthesize).")
        return suggestions[:5]

    def _check_curriculum_alignment(self, text: str) -> Dict[str, Any]:
        curriculum_keywords = {
            'kenya': ['competency', 'cbc', 'knec', 'community'],
            'bangladesh': ['nctb', 'board', 'exam', 'national'],
            'usa': ['common core', 'ngss', 'standards'],
            'uk': ['national curriculum', 'gcse', 'a-level']
        }
        keywords = curriculum_keywords.get(self.country, [])
        text_lower = text.lower()
        matched = [kw for kw in keywords if kw in text_lower]
        score = len(matched) / len(keywords) if keywords else 0
        return {'score': round(score * 100, 2), 'matched_indicators': matched,
                'status': 'Aligned' if score > 0.5 else 'Partial' if score > 0.2 else 'Not Aligned'}

    def _suggest_teacher_enhancements(self, text: str) -> List[str]:
        suggestions = []
        text_lower = text.lower()
        if 'objective' not in text_lower:
            suggestions.append("Add clear learning objectives for each lesson.")
        if 'assessment' not in text_lower:
            suggestions.append("Include assessment criteria and methods.")
        if 'activity' not in text_lower:
            suggestions.append("Add interactive activities to engage students.")
        if 'differentiation' not in text_lower:
            suggestions.append("Include differentiation strategies for diverse learners.")
        return suggestions[:5]

    def _extract_business_context(self, text: str) -> Dict[str, Any]:
        context = {'industry': 'Not specified', 'market': 'Not specified',
                   'key_metrics': [], 'timeline': 'Not specified'}
        text_lower = text.lower()
        industries = {
            'tech': ['software', 'technology', 'digital'],
            'finance': ['finance', 'banking', 'investment'],
            'health': ['health', 'medical', 'wellness'],
            'retail': ['retail', 'store', 'customer'],
            'manufacturing': ['manufacture', 'production', 'factory']
        }
        for industry, keywords in industries.items():
            if any(kw in text_lower for kw in keywords):
                context['industry'] = industry.title()
                break
        return context

    def _extract_actionable_insights(self, text: str) -> List[str]:
        insights = []
        action_patterns = [
            r'(recommend|suggest|should|must)\s+([^.!?]+)',
            r'(implement|adopt|use)\s+([^.!?]+)',
        ]
        for pattern in action_patterns:
            for match in re.findall(pattern, text, re.IGNORECASE):
                if len(match) >= 2:
                    insight = f"{match[0]} {match[1]}"
                    if 10 < len(insight) < 100:
                        insights.append(insight.strip())
        return list(dict.fromkeys(insights))[:5]

    def _identify_growth_opportunities(self, text: str) -> List[str]:
        opportunities = []
        text_lower = text.lower()
        if any(kw in text_lower for kw in ['new market', 'expansion', 'enter']):
            opportunities.append("Market expansion opportunities")
        if any(kw in text_lower for kw in ['digital', 'online', 'e-commerce']):
            opportunities.append("Digital transformation opportunity")
        if any(kw in text_lower for kw in ['efficiency', 'cost', 'reduce']):
            opportunities.append("Cost optimization and efficiency improvement")
        return list(dict.fromkeys(opportunities))[:5]

    def _identify_automation_candidates(self, text: str) -> List[str]:
        candidates = []
        text_lower = text.lower()
        if any(kw in text_lower for kw in ['customer', 'support', 'enquiry']):
            candidates.append("Customer support chatbot")
        if any(kw in text_lower for kw in ['order', 'receipt', 'invoice']):
            candidates.append("Automated billing and invoicing")
        if any(kw in text_lower for kw in ['inventory', 'stock', 'supply']):
            candidates.append("Inventory management automation")
        return list(dict.fromkeys(candidates))[:5]

    def _extract_financial_metrics(self, text: str) -> Dict[str, Any]:
        metrics = {'revenue': None, 'profit': None, 'expenses': None,
                   'growth_rate': None, 'margin': None, 'roi': None}
        patterns = {
            'revenue': r'revenue\s*[:$]?\s*\$?(\d+[\.,]?\d*)',
            'profit': r'profit\s*[:$]?\s*\$?(\d+[\.,]?\d*)',
            'expenses': r'expenses?\s*[:$]?\s*\$?(\d+[\.,]?\d*)',
            'growth_rate': r'growth\s*[:]?\s*(\d+[\.,]?\d*)\s*%',
            'margin': r'margin\s*[:]?\s*(\d+[\.,]?\d*)\s*%',
            'roi': r'ROI\s*[:]?\s*(\d+[\.,]?\d*)\s*%'
        }
        for key, pattern in patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    metrics[key] = float(match.group(1).replace(',', ''))
                except ValueError:
                    pass
        return metrics


# ==================== STUDENT OUTCOME ENGINE (EU AI Act Aligned) ====================

class StudentOutcomeEngine:
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.context = LocalCurriculumOverlay.get_local_context(country_code)
        self.doc_engine = DocumentIntelligenceEngine(country_code)

        self.review_data = {}
        self.knowledge_graph = self._build_knowledge_graph()
        self.profile = {
            'concept_mastery': {},
            'attempts': {},
            'consecutive_wrong': {},
            'win_streak': 0,
            'total_attempts': 0,
            'total_correct': 0,
        }
        self.content_filter = self._build_content_filter()

        # Streak is now OPT-IN and informational only
        self.streak = 0
        self.streak_opt_in = False
        self.last_activity_date = datetime.now().date()

        self.solution_times = {}
        self.confidence_ratings = {}

    def _build_knowledge_graph(self):
        return {
            "addition": [],
            "subtraction": ["addition"],
            "multiplication": ["addition", "subtraction"],
            "division": ["multiplication", "subtraction"],
            "fractions": ["division", "multiplication"],
            "algebra_basics": ["fractions", "division"],
            "linear_equations": ["algebra_basics"],
            "quadratic_equations": ["factoring", "linear_equations"],
            "factoring": ["multiplication", "division", "algebra_basics"],
            "cell_structure": [],
            "photosynthesis": ["cell_structure"],
            "cellular_respiration": ["cell_structure"],
            "genetics": ["cell_structure"],
            "newtons_laws": [],
            "energy": ["newtons_laws"],
            "momentum": ["newtons_laws"],
            "thermodynamics": ["energy", "momentum"],
        }

    def _build_content_filter(self):
        return [
            "cheat", "hack", "exploit", "bypass", "illegal", "drugs",
            "porn", "violence", "terror", "abuse", "harass", "discriminate",
            "racist", "sexist", "hate", "kill", "murder", "weapon",
            "gambling", "lottery", "casino", "bet", "fraud", "scam"
        ]

    # ===== SPACED REPETITION (unchanged core logic) =====

    def get_review_prompt(self, concept_id: str) -> Optional[Dict[str, Any]]:
        if concept_id not in self.review_data:
            self.review_data[concept_id] = {
                'last_reviewed': datetime.now(),
                'interval': 1,
                'ease_factor': 2.5,
                'next_review': datetime.now() + timedelta(days=1)
            }
            return None
        data = self.review_data[concept_id]
        if datetime.now() >= data['next_review']:
            return {
                'concept_id': concept_id,
                'prompt': f"Review time for '{concept_id}'. Can you recall the key points?",
                'interval': data['interval'],
                'ease_factor': data['ease_factor']
            }
        return None

    def update_review(self, concept_id: str, quality: int):
        if concept_id not in self.review_data:
            return
        data = self.review_data[concept_id]
        if quality >= 3:
            data['interval'] = int(data['interval'] * data['ease_factor'])
            data['ease_factor'] += (0.1 - (5 - quality) * 0.08)
        else:
            data['interval'] = 1
            data['ease_factor'] = max(1.3, data['ease_factor'] - 0.2)
        data['last_reviewed'] = datetime.now()
        data['next_review'] = datetime.now() + timedelta(days=data['interval'])
        if quality >= 4 and data['interval'] > 7:
            self.profile['concept_mastery'][concept_id] = 'mastered'
        elif quality >= 3:
            self.profile['concept_mastery'][concept_id] = 'in_progress'
        else:
            self.profile['concept_mastery'][concept_id] = 'locked'

    # ===== PREREQUISITE KNOWLEDGE GRAPH =====

    def is_prereq_met(self, concept_id: str) -> bool:
        prereqs = self.knowledge_graph.get(concept_id, [])
        if not prereqs:
            return True
        for prereq in prereqs:
            if self.profile['concept_mastery'].get(prereq) != 'mastered':
                return False
        return True

    def get_available_topics(self) -> List[str]:
        return [c for c in self.knowledge_graph.keys() if self.is_prereq_met(c)]

    def get_mastery_tree(self) -> Dict[str, Dict[str, Any]]:
        tree = {}
        for concept, prereqs in self.knowledge_graph.items():
            status = self.profile['concept_mastery'].get(concept, 'locked')
            if status == 'locked' and self.is_prereq_met(concept):
                status = 'in_progress'
            tree[concept] = {
                'prerequisites': prereqs,
                'status': status,
                'mastery_level': self.profile.get('concept_mastery', {}).get(concept, 0)
            }
        return tree

    # ===== OCR (unchanged) =====

    def process_ocr_image(self, image_bytes: bytes) -> Dict[str, Any]:
        sample_text = "This is simulated OCR text extracted from the uploaded image."
        return {
            'status': 'success',
            'extracted_text': sample_text,
            'detected_language': 'en',
            'ai_task': "Solve the following equation: 3x + 5 = 17",
            'confidence': 0.89
        }

    # ===== SOCRATIC GUIDANCE =====

    def get_socratic_guidance(self, question: str, student_answer: str) -> Dict[str, Any]:
        guidance = {
            'hints': [
                "Think about what operation you need to perform first.",
                "Can you identify the unknown variable in the problem?",
                "Try breaking the problem into smaller parts."
            ],
            'analogies': [
                "This is like following a recipe - you need to complete each step in order.",
                "Think of it as a puzzle where each piece fits together."
            ],
            'step_by_step': [
                "Step 1: Identify what you know.",
                "Step 2: Determine what you need to find.",
                "Step 3: Apply the appropriate formula or operation.",
                "Step 4: Check your answer."
            ],
            'direct_answer_given': False
        }
        return _transparency().attach(guidance, "student.socratic_tutor")

    # ===== DYNAMIC DIFFICULTY =====

    def adjust_difficulty(self, concept_id: str, correct: bool) -> Dict[str, Any]:
        if concept_id not in self.profile['consecutive_wrong']:
            self.profile['consecutive_wrong'][concept_id] = 0
        if correct:
            self.profile['consecutive_wrong'][concept_id] = 0
            self.profile['win_streak'] += 1
            self.profile['total_correct'] += 1
            escalation = "escalated" if self.profile['win_streak'] >= 3 else "normal"
        else:
            self.profile['consecutive_wrong'][concept_id] += 1
            self.profile['win_streak'] = 0
            escalation = "sub_steps" if self.profile['consecutive_wrong'][concept_id] >= 2 else "normal"
        self.profile['total_attempts'] += 1

        result = {
            'concept_id': concept_id,
            'consecutive_wrong': self.profile['consecutive_wrong'][concept_id],
            'win_streak': self.profile['win_streak'],
            'action': escalation,
            'message': "Let's break this down into smaller steps." if escalation == "sub_steps"
                       else "Great job! Let's try a harder question." if escalation == "escalated"
                       else "Keep going!"
        }

        # Log for high-risk system
        _logger().log(
            system_id="student.mastery_engine",
            segment="Student",
            input_text=f"{concept_id}|correct={correct}",
            output_summary=f"action={escalation}"
        )

        return result

    # ===== VOICE INPUT (EU AI ACT ALIGNED — CONTENT ONLY) =====

    def process_voice_input(self, audio_bytes: bytes) -> Dict[str, Any]:
        """
        Content-only comprehension assessment.

        EU AI Act Art. 5(1)(f) prohibits emotion recognition in education.
        This function evaluates the CONTENT of spoken answers only.
        It does NOT infer emotional state, attention, stress, or affect.
        """
        simulated_transcript = (
            "I think photosynthesis is the process where plants use sunlight "
            "to make food from water and carbon dioxide."
        )
        content_score = 0.85

        result = {
            'status': 'success',
            'transcript': simulated_transcript,
            'content_comprehension_score': content_score,
            'explicitly_not_used_for': [
                'emotion recognition',
                'attention tracking',
                'stress or affect inference',
                'behavioral profiling'
            ],
            'disclosure': 'This assessment evaluates answer content only. '
                          'It does not infer emotional state.',
            'ai_act_reference': 'Designed to avoid Art. 5(1)(f) prohibited practice'
        }
        return result

    # ===== STREAK (EU AI ACT ALIGNED — NON-MANIPULATIVE) =====

    def set_streak_opt_in(self, opt_in: bool):
        """Streak tracking is opt-in only."""
        self.streak_opt_in = opt_in
        if not opt_in:
            self.streak = 0

    def update_streak(self) -> Dict[str, Any]:
        """
        Opt-in, non-manipulative habit tracking.

        Aligned with EU AI Act principles:
          - Never shames the user for missing a day
          - Never uses loss-aversion framing ("don't break it!")
          - Never ties streak to rewards the user can lose
          - Is purely informational
        """
        if not self.streak_opt_in:
            return {
                'streak': 0,
                'message': "Streak tracking is currently disabled. Enable it in settings if you'd like to track practice days.",
                'opt_in': False
            }

        today = datetime.now().date()
        if self.last_activity_date == today:
            return {'streak': self.streak, 'message': "Welcome back.", 'opt_in': True}

        days_diff = (today - self.last_activity_date).days
        self.last_activity_date = today

        if days_diff == 1:
            self.streak += 1

        return {
            'streak': self.streak,
            'message': f"Nice to see you. You've practiced {self.streak} day(s) recently.",
            'note': 'Streak tracking is informational only and never tied to rewards.',
            'opt_in': True
        }

    def get_push_notification(self) -> Optional[str]:
        """
        Non-manipulative notification. Opt-in only, no loss framing.
        """
        if not self.streak_opt_in:
            return None
        if self.streak == 0:
            return "📚 Ready to explore something new today?"
        return f"📚 You've practiced {self.streak} day(s) recently. No pressure — come back when you're ready."

    # ===== LATENT GAP TRACKING =====

    def track_gap(self, concept_id: str, solution_time_sec: float, confidence: int):
        if concept_id not in self.solution_times:
            self.solution_times[concept_id] = []
        if concept_id not in self.confidence_ratings:
            self.confidence_ratings[concept_id] = []
        self.solution_times[concept_id].append(solution_time_sec)
        self.confidence_ratings[concept_id].append(confidence)

    def get_gap_analysis(self) -> Dict[str, Any]:
        gaps = {}
        for concept, times in self.solution_times.items():
            avg_time = float(np.mean(times)) if times else 0
            avg_confidence = float(np.mean(self.confidence_ratings.get(concept, [5]))) if self.confidence_ratings.get(concept) else 5
            attempts = len(times)
            gap_score = (avg_time / 60) * 0.3 + (5 - avg_confidence) * 0.4 + (attempts / 10) * 0.3
            if gap_score > 0.5:
                gaps[concept] = {
                    'avg_time': avg_time,
                    'avg_confidence': avg_confidence,
                    'attempts': attempts,
                    'gap_score': gap_score,
                    'recommendation': "Revisit foundational concepts." if gap_score > 0.7
                                      else "Practice more with varied problems."
                }
        return gaps

    # ===== DATA ISOLATION (unchanged) =====

    def isolate_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'session_id': hashlib.md5(str(datetime.now().timestamp()).encode()).hexdigest()[:8],
            'data': data,
            'note': "This data is not saved or used for training. It exists only for the current session."
        }

    # ===== CONTENT SHIELD (unchanged) =====

    def filter_content(self, prompt: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        blocked = [term for term in self.content_filter if term in prompt_lower]
        if blocked:
            return {
                'allowed': False,
                'blocked_terms': blocked,
                'message': "This prompt contains inappropriate content and has been blocked."
            }
        return {'allowed': True, 'message': "Content is appropriate for academic use."}

    # ===== INSTANT STEP EVALUATION (unchanged) =====

    def evaluate_work(self, student_work: str) -> Dict[str, Any]:
        lines = student_work.split('\n')
        feedback = []
        for i, line in enumerate(lines):
            if len(line.strip()) == 0:
                continue
            if "=" in line or "solve" in line.lower():
                feedback.append({'line': i+1, 'text': line,
                                 'feedback': "Good! You're showing your work.", 'status': 'positive'})
            elif len(line.split()) < 3:
                feedback.append({'line': i+1, 'text': line,
                                 'feedback': "Can you expand on this point?", 'status': 'needs_improvement'})
            else:
                feedback.append({'line': i+1, 'text': line,
                                 'feedback': "Clear and well-written.", 'status': 'positive'})
        return {
            'total_lines': len(lines),
            'feedback': feedback,
            'suggested_improvements': "Try to include more explanations and show each step clearly."
        }


# ==================== UNIVERSAL CORE ====================

class UniversalCore:
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
        },
        'ai_ethics': {
            'topics': [
                'Bias & Fairness in AI',
                'Privacy & Data Ownership',
                'AI Hallucinations & Verification',
                'Academic Integrity with AI',
                'Algorithmic Accountability',
                'Responsible Prompting'
            ],
            'skills': [
                'Critical AI Literacy',
                'Ethical Reasoning',
                'Source Verification',
                'Digital Citizenship'
            ]
        }
    }

    UNIVERSAL_COMPETENCIES = {
        'critical_thinking': 'Analyze, evaluate, and synthesize information',
        'communication': 'Express ideas clearly in multiple formats',
        'collaboration': 'Work effectively with others',
        'creativity': 'Generate innovative solutions',
        'digital_literacy': 'Use technology effectively and responsibly'
    }


# ==================== LOCAL OVERLAY ====================

class LocalCurriculumOverlay:
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
            'boards': ['Dhaka Board', 'Rajshahi Board', 'Chittagong Board'],
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

    LOCAL_CONTEXTS = {
        'kenya': {'culture': 'Kenyan community values, Harambee spirit, diverse ethnic groups',
                  'environment': 'Savanna, wildlife, agriculture, coastal regions',
                  'economy': 'Agriculture, tourism, technology (Silicon Savannah)'},
        'bangladesh': {'culture': 'Bengali heritage, language movement, diverse traditions',
                       'environment': 'Delta region, rivers, monsoon climate, agriculture',
                       'economy': 'Garment industry, agriculture, remittances, technology'},
        'usa': {'culture': 'Diverse immigrant nation, American Dream, individual liberty',
                'environment': 'Diverse climates, 50 states, national parks',
                'economy': "World's largest economy, innovation, technology"},
        'uk': {'culture': 'British heritage, royal tradition, multicultural society',
               'environment': 'Temperate climate, varied landscapes, historic cities',
               'economy': 'Service economy, financial hub, creative industries'}
    }

    AI_ETHICS_FRAMING = {
        'kenya': 'Ubuntu ethics, community consent, Harambee data-sharing norms',
        'bangladesh': 'Digital Bangladesh 2041 goals, language equity in AI, worker data rights',
        'usa': 'NIST AI RMF, civil rights frameworks, FERPA student privacy',
        'uk': 'ICO AI guidance, Online Safety Act, Ofcom duties'
    }

    @staticmethod
    def get_overlay(country_code):
        return LocalCurriculumOverlay.CURRICULUM_OVERLAYS.get(country_code, {})

    @staticmethod
    def get_local_context(country_code):
        return LocalCurriculumOverlay.LOCAL_CONTEXTS.get(country_code, {})

    @staticmethod
    def get_grade_levels(country_code):
        overlay = LocalCurriculumOverlay.get_overlay(country_code)
        return overlay.get('grade_levels', ['Primary', 'Secondary'])

    @staticmethod
    def get_ai_ethics_framing(country_code):
        return LocalCurriculumOverlay.AI_ETHICS_FRAMING.get(country_code, 'Universal AI ethics principles')


# ==================== TEACHER OUTCOME ENGINE ====================

class TeacherOutcomeEngine:
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.context = LocalCurriculumOverlay.get_local_context(country_code)
        self.doc_engine = DocumentIntelligenceEngine(country_code)
        self.intelligence = TeacherIntelligenceEngine(country_code)

    def generate_lesson_plan(self, subject, grade, duration, curriculum='universal'):
        overlay = self.overlay
        plan = {
            'title': f"{subject} Lesson - {grade}",
            'curriculum': overlay.get('system', 'Universal'),
            'country': self.country,
            'duration': duration,
            'objectives': self._generate_objectives(subject, grade),
            'activities': self._generate_activities(subject, duration),
            'assessment': self._generate_assessment(subject)
        }
        if overlay:
            plan['local_context'] = f"Aligned with {overlay.get('system')} ({overlay.get('code')})"
            plan['language_support'] = f"Available in {overlay.get('language', 'English')}"
            plan['cultural_context'] = self.context
        return _transparency().attach(plan, "teacher.lesson_builder")

    def _generate_objectives(self, subject, grade):
        objectives = [
            f"Understand key concepts of {subject} at {grade} level",
            f"Apply {subject} knowledge to real-world problems",
            f"Develop critical thinking in {subject} context"
        ]
        return objectives

    def _generate_activities(self, subject, duration):
        if duration <= 30:
            slots = [10, 10, 10]
        elif duration <= 45:
            slots = [15, 20, 10]
        else:
            slots = [15, 30, 15]
        return [
            f"Warm-up (0-{slots[0]} min): Introduction to {subject}",
            f"Main Activity ({slots[0]}-{slots[0]+slots[1]} min): Interactive learning session",
            f"Closure ({slots[0]+slots[1]}-{duration} min): Review and Q&A"
        ]

    def _generate_assessment(self, subject):
        return {'criteria': ['Understanding', 'Application', 'Analysis', 'Communication'],
                'weighting': [30, 25, 25, 20]}

    # Delegation to intelligence
    def generate_lesson_bundle(self, subject, grade, topic, duration):
        return self.intelligence.generate_lesson_bundle(subject, grade, topic, duration)

    def generate_quiz(self, subject, grade, topic, num_questions=5):
        quiz = self.intelligence.generate_quiz(subject, grade, topic, num_questions)
        return quiz

    def generate_rubric(self, title, criteria, levels):
        return self.intelligence.generate_rubric(title, criteria, levels)

    def adjust_reading_level(self, text, target_level):
        return self.intelligence.adjust_reading_level(text, target_level)

    def convert_document(self, uploaded_file, output_format):
        return self.intelligence.convert_document(uploaded_file, output_format)

    def get_lesson_blocks(self, lesson_plan):
        return self.intelligence.get_lesson_blocks(lesson_plan)

    def regenerate_block(self, block_type, context):
        return self.intelligence.regenerate_block(block_type, context)

    def apply_accommodation(self, content, accommodation_type):
        return self.intelligence.apply_accommodation(content, accommodation_type)

    def generate_batch_feedback(self, assignments):
        return self.intelligence.generate_batch_feedback(assignments)

    def approve_feedback(self, feedback_id, approved_by=None):
        return self.intelligence.approve_feedback(feedback_id, approved_by)

    def calculate_time_saved(self):
        return self.intelligence.calculate_time_saved()

    def generate_parent_update(self, student_name, subject, progress):
        return self.intelligence.generate_parent_update(student_name, subject, progress)

    def generate_sub_plan(self, subject, grade, lesson_topic):
        return self.intelligence.generate_sub_plan(subject, grade, lesson_topic)

    def redact_pii(self, text):
        return self.intelligence.redact_pii(text)

    def connect_lms(self, lms_type, credentials):
        return self.intelligence.connect_lms(lms_type, credentials)

    def sync_lms_data(self, lms_type, sync_type='all'):
        return self.intelligence.sync_lms_data(lms_type, sync_type)

    def map_standards(self, content, standard_type='common_core'):
        return self.intelligence.map_standards(content, standard_type)


# ==================== PROFESSIONAL OUTCOME ENGINE ====================

class ProfessionalOutcomeEngine:
    def __init__(self, domain='business', country_code='kenya'):
        self.domain = domain
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.doc_engine = DocumentIntelligenceEngine(country_code)
        self.intelligence = ProfessionalIntelligenceEngine(country_code)

    def generate_workflow(self, task_type):
        workflows = {
            'research': {
                'steps': ['Define research question', 'Gather and analyze data',
                          'Synthesize findings', 'Generate report'],
                'output': 'Research synthesis with actionable insights'
            },
            'investment_research': {
                'steps': ['Identify investment thesis', 'Analyze market fundamentals',
                          'Evaluate competitive landscape', 'Build financial model',
                          'Generate investment recommendation'],
                'output': 'Investment research report with actionable insights'
            }
        }
        return workflows.get(task_type, workflows['research'])

    def hybrid_search(self, query, search_type='hybrid'):
        type_enum = SearchType.HYBRID
        if search_type == 'keyword':
            type_enum = SearchType.KEYWORD
        elif search_type == 'vector':
            type_enum = SearchType.VECTOR
        elif search_type == 'semantic':
            type_enum = SearchType.SEMANTIC
        return self.intelligence.hybrid_search(query, type_enum)

    def audit_analysis(self, analysis_text):
        return self.intelligence.audit_analysis(analysis_text, self.intelligence.documents)

    def execute_quant_analysis(self, code, data):
        return self.intelligence.execute_quant_analysis(code, data)

    def get_portfolio_metrics(self):
        return self.intelligence.calculate_portfolio_metrics()

    def run_stress_test(self, scenario):
        return self.intelligence.run_macro_stress_test(scenario)

    def generate_deliverable(self, template_type, data):
        return self.intelligence.generate_deliverable(template_type, data)

    def extract_table(self, pdf_content):
        return self.intelligence.extract_table_from_pdf(pdf_content)

    def get_watchdog_alerts(self):
        return self.intelligence.watchdog_alerts

    def refresh_watchdogs(self):
        return self.intelligence.run_watchdog_alerts()

    def get_market_data(self, ticker):
        return self.intelligence.fetch_market_data(ticker)

    def get_sec_filing(self, ticker):
        return self.intelligence.fetch_sec_filing(ticker)

    def get_earnings_call(self, ticker):
        return self.intelligence.fetch_earnings_call(ticker)

    def get_workspace_data(self):
        return self.intelligence.get_workspace_data()


# ==================== SME OUTCOME ENGINE ====================

class SMEOutcomeEngine:
    def __init__(self, market='africa', country_code='kenya'):
        self.market = market
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.doc_engine = DocumentIntelligenceEngine(country_code)
        self.infrastructure = SMEInfrastructureEngine(country_code)
        self.ai_engine = SMEAIEngine(country_code)
        self.ux_engine = SMEProductUXEngine(country_code)

    def generate_automation(self, business_type):
        automations = {
            'retail': {
                'inventory': 'Auto-reorder when stock below threshold',
                'customer_support': 'AI chatbot for common queries',
                'payments': f'Integrated mobile money ({self._get_payment_rails()})',
                'marketing': 'Automated WhatsApp/SMS campaigns'
            },
            'service': {
                'booking': 'Self-service booking and scheduling',
                'followup': 'Automated client check-ins',
                'billing': 'Auto-generate invoices and receipts',
                'referrals': 'Digital referral tracking system'
            },
            'agriculture': {
                'weather_alerts': 'Real-time weather notifications',
                'market_prices': 'Daily price updates',
                'supply_chain': 'Track and optimize distribution',
                'financial': 'Crop insurance and loan management'
            }
        }
        return automations.get(business_type, automations['retail'])

    def _get_payment_rails(self):
        rails = {
            'kenya': 'M-Pesa, Airtel Money, Equitel',
            'bangladesh': 'bKash, Nagad, Rocket',
            'usa': 'PayPal, Stripe, Venmo, Square',
            'uk': 'PayPal, Stripe, Barclays, Monzo'
        }
        return rails.get(self.country, 'M-Pesa, Airtel Money')

    def get_action_tasks(self, business_data):
        return self.ux_engine.generate_tasks(business_data)

    def process_webhook(self, event_type, payload):
        return self.infrastructure.process_webhook(event_type, payload)

    def connect_api(self, service, credentials):
        return self.infrastructure.connect_api(service, credentials)

    def natural_language_query(self, query, data_context):
        return self.ai_engine.natural_language_query(query, data_context)

    def generate_digest(self, channel='whatsapp'):
        return self.ux_engine.generate_digest(channel)


# ==================== MAIN APP ====================

def init_session_state():
    defaults = {
        'user_role': None,
        'country_code': 'kenya',
        'student_score': 54,
        'completed_lessons': [],
        'achievements': [],
        'streak': 0,
        'streak_opt_in': False,
        'weak_areas': [],
        'domain': 'business',
        'business_type': 'retail',
        'preferred_language': 'English',
        'doc_analysis_history': [],
        'sme_tasks': [],
        'sme_alerts': [],
        'webhook_events': [],
        'professional_workspace': {},
        'teacher_lesson_plans': [],
        'teacher_rubrics': [],
        'teacher_quizzes': [],
        'teacher_feedback': [],
        'student_engine': None,
        'spaced_repetition_data': {},
        'knowledge_graph_data': {},
        'streak_data': {}
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


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
    .stButton > button:hover { transform: scale(1.05); box-shadow: 0 10px 20px rgba(0,0,0,0.2); }
    .country-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white; padding: 4px 12px; border-radius: 20px;
        display: inline-block; margin: 4px; font-size: 0.8rem;
    }
    .universal-core { background: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #667eea; }
    .local-overlay { background: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #f5576c; }
    .document-analysis { background: #e8f5e9; padding: 20px; border-radius: 10px; border-left: 5px solid #4caf50; margin: 10px 0; }
    .task-critical { background: #ffebee; border-left: 5px solid #f44336; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .task-high { background: #fff3e0; border-left: 5px solid #ff9800; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .task-medium { background: #e3f2fd; border-left: 5px solid #2196f3; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .task-low { background: #f5f5f5; border-left: 5px solid #9e9e9e; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .professional-card { background: #f3e5f5; border-left: 5px solid #9c27b0; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .watchdog-alert { background: #fff3e0; border-left: 5px solid #ff6f00; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .citation-box { background: #e3f2fd; border-left: 5px solid #1565c0; padding: 15px; border-radius: 5px; margin: 10px 0; font-family: monospace; font-size: 0.9em; }
    .teacher-card { background: #e8f5e9; border-left: 5px solid #2e7d32; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .time-saved-metric { background: #fff8e1; border-left: 5px solid #f57f17; padding: 15px; border-radius: 5px; margin: 10px 0; }
    .student-progress-card { background: #f3e5f5; border-radius: 10px; padding: 15px; margin: 5px 0; border-left: 4px solid #7b1fa2; }
    .socratic-hint { background: #e8eaf6; border-radius: 8px; padding: 12px; margin: 8px 0; border-left: 4px solid #3949ab; font-style: italic; }
    .mastery-node { display: inline-block; padding: 6px 14px; border-radius: 20px; margin: 4px; font-weight: 600; font-size: 0.85rem; }
    .mastery-locked { background: #eeeeee; color: #9e9e9e; }
    .mastery-in-progress { background: #fff3e0; color: #e65100; }
    .mastery-mastered { background: #e8f5e9; color: #2e7d32; }
    .ai-disclosure { background: #fffde7; border-left: 4px solid #fbc02d; padding: 10px; border-radius: 5px; margin: 10px 0; font-size: 0.85rem; color: #5d4037; }
    .prototype-banner { background: #e3f2fd; border-left: 4px solid #1565c0; padding: 10px 15px; border-radius: 5px; margin: 10px 0; font-size: 0.85rem; color: #0d47a1; }
    </style>
    """, unsafe_allow_html=True)


apply_custom_css()


# ==================== SIDEBAR ====================

st.sidebar.title("🌍 AI Shiksha")
st.sidebar.caption("Universal Core + Local Overlay")

st.sidebar.markdown("""
<div class="prototype-banner">
<strong>🧪 Prototype</strong><br>
Governance architecture aligned with <strong>EU AI Act principles</strong> as a design standard.
No legal compliance claim is made.
</div>
""", unsafe_allow_html=True)

country_flags = {'kenya': '🇰🇪', 'bangladesh': '🇧🇩', 'usa': '🇺🇸', 'uk': '🇬🇧'}

country_code = st.sidebar.selectbox(
    "🌐 Select Country/Region:",
    ['kenya', 'bangladesh', 'usa', 'uk'],
    format_func=lambda x: f"{country_flags.get(x, '🌍')} {x.title()}"
)
st.session_state.country_code = country_code

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

user_role = st.sidebar.selectbox(
    "👤 Select Your Role:",
    ['Student', 'Teacher', 'Professional', 'SME Business Owner']
)
st.session_state.user_role = user_role

menu_options = {
    'Student': ['🎓 Dashboard', '📝 Practice', '📊 Progress', '🏆 Achievements',
                '🧠 Spaced Repetition', '🗺️ Knowledge Graph', '🎙️ Voice Recall',
                '📄 Document Analysis', '🛡️ AI Ethics'],
    'Teacher': ['👨‍🏫 Dashboard', '📋 Lesson Builder', '📝 Assessment', '⏱️ Hours Saved',
                '📄 Document Analysis', '📑 LMS Integration', '🎯 Standards Mapping',
                '🛡️ AI Ethics'],
    'Professional': ['💼 Dashboard', '🔬 Research', '📊 Portfolio', '📄 Document Analysis',
                     '📑 Workspace', '⚡ Watchdogs', '🛡️ AI Ethics'],
    'SME Business Owner': ['🏢 Dashboard', '📈 Growth', '🤖 Automation', '📄 Document Analysis',
                            '🔌 API Connectors', '⚡ Webhooks', '🛡️ AI Ethics']
}

st.sidebar.divider()
choice = st.sidebar.radio("Navigate:", menu_options.get(user_role, ['Dashboard']))


def show_vibe_check():
    with st.sidebar.expander("🎯 Daily Vibe Check", expanded=False):
        vibe = st.select_slider(
            "How's your learning energy today?",
            options=["😴 Low", "😐 Neutral", "⚡ Medium", "🔥 High", "🚀 Cosmic"],
            value="🔥 High"
        )
        if vibe in ["🔥 High", "🚀 Cosmic"]:
            st.success("Let's ride that energy wave! 🌊")
        elif vibe == "😴 Low":
            st.info("Start with a 5-min quick win!")


show_vibe_check()


# ==================== AI ETHICS PAGE ====================

def show_ai_ethics():
    st.header(f"🛡️ AI Ethics & Governance - {country_code.title()}")

    st.markdown("""
    <div class="prototype-banner">
    <strong>🧪 Prototype Notice</strong><br>
    AI Shiksha is a <strong>prototype</strong>. Its governance architecture is
    <strong>aligned with EU AI Act (Regulation 2024/1689) principles</strong> as a design standard.
    No legal compliance claim is made. AI Shiksha is not currently placed on the EU market.
    </div>
    """, unsafe_allow_html=True)

    # Registered systems
    st.subheader("🧭 Registered AI Systems")
    st.caption("Every AI system in AI Shiksha is declared with a risk tier and purpose.")

    rows = []
    for sid, reg in AI_SYSTEM_REGISTRY.items():
        rows.append({
            'System': reg.name,
            'Risk Tier': reg.risk_tier.value.title(),
            'Purpose': reg.intended_purpose,
            'Human Oversight': '✅' if reg.human_oversight_required else '—',
            'Transparency': '✅' if reg.transparency_required else '—',
            'Annex III': reg.annex_iii_category or '—'
        })
    st.dataframe(pd.DataFrame(rows), use_container_width=True)

    # What AI does NOT do
    st.subheader("🚫 What AI Shiksha Does Not Do")
    st.markdown("""
    - ❌ Infer emotional state from voice, text, or behaviour
    - ❌ Track attention or engagement via biometrics
    - ❌ Make final grading decisions without a human approver
    - ❌ Manipulate users via streaks, notifications, or loss aversion
    - ❌ Share student data with model training pipelines
    - ❌ Infer emotional state from voice input in education settings
    """)

    # What AI DOES do
    st.subheader("✅ What AI Shiksha Does")
    st.markdown("""
    - ✅ Discloses AI involvement on every AI-generated output
    - ✅ Requires human review on high-risk outputs (e.g., student feedback)
    - ✅ Logs AI decisions for auditability
    - ✅ Declares each AI system's risk tier and purpose
    - ✅ Separates student data from any training pipeline
    - ✅ Uses deterministic seeds for reproducible forecasts
    - ✅ Provides opt-in, non-manipulative habit tracking
    """)

    # Country framing
    st.subheader(f"🌍 {country_code.title()} — AI Ethics Framing")
    framing = LocalCurriculumOverlay.get_ai_ethics_framing(country_code)
    st.info(f"**Local context:** {framing}")

    # EU AI Act reference
    st.subheader("📖 About the EU AI Act")
    st.markdown("""
    The **EU AI Act (Regulation 2024/1689)** is the world's first comprehensive AI law.
    It classifies AI systems by risk tier:
    - **Prohibited** — banned outright (e.g., emotion recognition in education)
    - **High-risk** — heavy compliance (e.g., evaluating learning outcomes)
    - **Limited-risk** — transparency duties (e.g., chatbots, generated content)
    - **Minimal-risk** — no specific obligations

    AI Shiksha uses this framework as a **design standard** for a worldwide platform.
    The intent is not EU market access, but to build a governance foundation that
    scales across jurisdictions and prepares for future regulation.
    """)

    # Disclaimer
    st.divider()
    st.caption(
        "AI Shiksha is a prototype and does not currently place AI systems on the EU market. "
        "These design choices reflect a commitment to responsible AI and prepare the platform "
        "for future regulatory alignment in any jurisdiction."
    )


# ==================== STUDENT UI FUNCTIONS ====================

def get_student_engine():
    if st.session_state.student_engine is None:
        st.session_state.student_engine = StudentOutcomeEngine(st.session_state.country_code)
    return st.session_state.student_engine


def show_student_dashboard():
    st.header(f"🎓 Student Dashboard - {country_code.title()}")

    engine = get_student_engine()

    streak_update = engine.update_streak()
    if streak_update.get('streak', 0) > 0:
        st.session_state.streak = streak_update['streak']

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("📊 Score", f"{st.session_state.student_score}%")
    col2.metric("🔥 Streak", f"{st.session_state.streak} days" if engine.streak_opt_in else "—",
                "Opt-in" if not engine.streak_opt_in else "")
    col3.metric("📚 Lessons", len(st.session_state.completed_lessons))
    col4.metric("🏆 Achievements", len(st.session_state.achievements))
    col5.metric("🧠 Mastered Topics",
                len([c for c, s in engine.profile['concept_mastery'].items() if s == 'mastered']))

    # Opt-in streak control
    with st.expander("⚙️ Streak Settings (opt-in)", expanded=False):
        opt_in = st.checkbox("Enable streak tracking", value=engine.streak_opt_in)
        if opt_in != engine.streak_opt_in:
            engine.set_streak_opt_in(opt_in)
            st.success("Streak tracking preference updated.")
            st.rerun()
        st.caption("Streak tracking is informational only and never tied to rewards.")

    push_notif = engine.get_push_notification()
    if push_notif:
        st.info(f"🔔 {push_notif}")

    st.subheader("🧠 Spaced Repetition Review")
    due_items = []
    for concept in engine.knowledge_graph.keys():
        review = engine.get_review_prompt(concept)
        if review:
            due_items.append(concept)

    if due_items:
        st.warning(f"📚 You have {len(due_items)} concepts due for review!")
        for concept in due_items[:3]:
            if st.button(f"Review '{concept}'", key=f"review_{concept}"):
                st.session_state['selected_review_concept'] = concept
                st.rerun()
    else:
        st.success("✅ All concepts are up to date! Great job!")

    st.subheader("🗺️ Your Learning Path")
    tree = engine.get_mastery_tree()
    available = engine.get_available_topics()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**🔓 Unlocked Topics:**")
        for concept in available[:5]:
            st.markdown(f"<span class='mastery-node mastery-in-progress'>{concept}</span>",
                        unsafe_allow_html=True)
    with col2:
        st.markdown("**🔒 Locked Topics (Prerequisites needed):**")
        locked = [c for c, data in tree.items() if data['status'] == 'locked']
        for concept in locked[:5]:
            prereqs = engine.knowledge_graph.get(concept, [])
            st.markdown(
                f"<span class='mastery-node mastery-locked'>{concept} (needs: {', '.join(prereqs)})</span>",
                unsafe_allow_html=True
            )

    st.subheader("🚀 Quick Practice")
    available = engine.get_available_topics()
    if available:
        selected_concept = st.selectbox("Choose a topic:", available)
        if st.button("🎯 Start Practice", type="primary"):
            st.session_state['current_concept'] = selected_concept
            st.rerun()


def show_student_practice():
    st.header(f"📝 Practice Session - {country_code.title()}")

    engine = get_student_engine()
    concept = st.session_state.get('current_concept', 'addition')

    if not engine.is_prereq_met(concept):
        st.error(f"🚫 '{concept}' is locked. Complete prerequisites first: "
                 f"{', '.join(engine.knowledge_graph.get(concept, []))}")
        return

    st.subheader(f"📚 Topic: {concept.replace('_', ' ').title()}")

    status = engine.profile['concept_mastery'].get(concept, 'in_progress')
    status_colors = {'locked': '🔴', 'in_progress': '🟡', 'mastered': '🟢'}
    st.markdown(f"**Status:** {status_colors.get(status, '⚪')} {status.replace('_', ' ').title()}")

    question_data = {
        'question': f"Solve the following problem related to {concept}:",
        'problem': "3x + 7 = 22. What is x?" if 'algebra' in concept else "5 + 3 × 2 = ?",
        'answer': "5" if 'algebra' in concept else "11"
    }

    st.markdown(f"### {question_data['question']}")
    st.markdown(f"**Problem:** {question_data['problem']}")

    if st.button("💡 Show Socratic Hint"):
        guidance = engine.get_socratic_guidance(question_data['problem'], "")
        st.markdown('<div class="socratic-hint">', unsafe_allow_html=True)
        st.markdown("**🧠 Hints:**")
        for hint in guidance['hints']:
            st.markdown(f"- {hint}")
        st.markdown("**🔍 Analogies:**")
        for analogy in guidance['analogies']:
            st.markdown(f"- {analogy}")
        st.markdown("**📝 Step-by-Step:**")
        for step in guidance['step_by_step']:
            st.markdown(f"- {step}")
        st.markdown('</div>', unsafe_allow_html=True)

        # Disclosure
        if '_ai_disclosure' in guidance:
            st.markdown(f'<div class="ai-disclosure">{guidance["_ai_disclosure"]["disclosure_text"]}</div>',
                        unsafe_allow_html=True)

    student_answer = st.text_input("Your answer:", key=f"answer_{concept}")

    if st.button("📤 Submit Answer", type="primary"):
        if student_answer.strip() == "":
            st.warning("Please enter your answer.")
        else:
            correct = student_answer.strip() == question_data['answer']
            diff_result = engine.adjust_difficulty(concept, correct)
            quality = 5 if correct else 1
            engine.update_review(concept, quality)
            engine.track_gap(concept, solution_time_sec=random.uniform(5, 30),
                             confidence=3 if correct else 2)

            if correct:
                st.success("✅ Correct! Great job!")
                st.session_state.student_score = min(100, st.session_state.student_score + 3)
                if concept not in st.session_state.completed_lessons:
                    st.session_state.completed_lessons.append(concept)
            else:
                st.error(f"❌ Not quite. Correct answer: {question_data['answer']}")
                st.session_state.student_score = max(0, st.session_state.student_score - 2)

            st.info(f"📊 {diff_result['message']}")

            gaps = engine.get_gap_analysis()
            if concept in gaps:
                st.warning(f"🔍 Gap detected in '{concept}': {gaps[concept]['recommendation']}")

    st.divider()
    st.subheader("📝 Instant Step Evaluation")
    student_work = st.text_area("Your work:", height=150, key=f"work_{concept}")
    if st.button("🔍 Evaluate My Work"):
        if student_work:
            eval_result = engine.evaluate_work(student_work)
            st.markdown("### 📋 Feedback")
            for fb in eval_result['feedback']:
                if fb['status'] == 'positive':
                    st.success(f"Line {fb['line']}: {fb['feedback']}")
                else:
                    st.warning(f"Line {fb['line']}: {fb['feedback']}")
            st.info(f"💡 Suggested Improvement: {eval_result['suggested_improvements']}")


def _show_text_mastery_tree(tree):
    st.markdown("### 📋 Concept Status")
    grouped = {'mastered': [], 'in_progress': [], 'locked': []}
    for concept, data in tree.items():
        status = data['status']
        if status in grouped:
            grouped[status].append(concept)

    if grouped['mastered']:
        st.success("✅ **Mastered Concepts:**")
        for concept in grouped['mastered']:
            st.markdown(f"- {concept.replace('_', ' ').title()}")
        st.divider()

    if grouped['in_progress']:
        st.warning("🟡 **In Progress:**")
        for concept in grouped['in_progress']:
            st.markdown(f"- {concept.replace('_', ' ').title()}")
        st.divider()

    if grouped['locked']:
        st.info("🔒 **Locked Concepts:**")
        for concept in grouped['locked']:
            prereqs = tree[concept]['prerequisites']
            if prereqs:
                missing = [p for p in prereqs if tree.get(p, {}).get('status') != 'mastered']
                if missing:
                    st.markdown(f"- {concept.replace('_', ' ').title()} (needs: {', '.join(missing)})")
                else:
                    st.markdown(f"- {concept.replace('_', ' ').title()}")

    total = len(tree)
    if total > 0:
        mastered = len(grouped['mastered'])
        st.progress(mastered / total, text=f"Overall Progress: {mastered/total*100:.1f}%")


def show_student_progress():
    st.header(f"📊 Progress Tracking - {country_code.title()}")

    engine = get_student_engine()
    st.subheader("🗺️ Visual Mastery Tree")
    st.caption("Nodes show concept status: 🔒 Locked | 🟡 In Progress | 🟢 Mastered")

    tree = engine.get_mastery_tree()

    try:
        if HAS_NETWORKX and HAS_MATPLOTLIB and nx is not None and plt is not None:
            G = nx.DiGraph()
            for concept, data in tree.items():
                G.add_node(concept, status=data['status'])
                for prereq in data['prerequisites']:
                    G.add_edge(prereq, concept)

            color_map = {'locked': '#eeeeee', 'in_progress': '#ffcc80', 'mastered': '#81c784'}
            node_colors = [color_map.get(tree.get(c, {}).get('status', 'locked'), '#eeeeee')
                           for c in G.nodes()]

            fig, ax = plt.subplots(figsize=(10, 6))
            pos = nx.spring_layout(G, seed=42)
            nx.draw(G, pos, with_labels=True, node_color=node_colors,
                    node_size=1500, font_size=8, arrows=True, ax=ax)
            st.pyplot(fig)
        else:
            st.info("📦 Visual graph libraries not available. Install `networkx` and `matplotlib` for visual graphs.")
            _show_text_mastery_tree(tree)
    except Exception as e:
        st.warning(f"⚠️ Could not render graph: {str(e)[:100]}")
        _show_text_mastery_tree(tree)

    st.divider()
    st.subheader("🔍 Latent Knowledge Gap Analysis")
    gaps = engine.get_gap_analysis()
    if gaps:
        for concept, data in gaps.items():
            st.markdown(f"""
            <div class="student-progress-card">
            <strong>{concept.replace('_', ' ').title()}</strong>
            <br>Average Time: {data['avg_time']:.1f}s | Confidence: {data['avg_confidence']:.1f}/5 | Attempts: {data['attempts']}
            <br>💡 Recommendation: {data['recommendation']}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.success("✅ No knowledge gaps detected!")


def show_student_achievements():
    st.header(f"🏆 Achievements - {country_code.title()}")
    engine = get_student_engine()

    all_achievements = [
        {"name": "First Steps", "emoji": "👣", "condition": "Complete 1 lesson"},
        {"name": "Knowledge Seeker", "emoji": "📚", "condition": "Complete 5 lessons"},
        {"name": "Mastery Mind", "emoji": "🧠", "condition": "Master 3 concepts"},
        {"name": "Streak Starter", "emoji": "🔥", "condition": "Maintain 3-day streak"},
        {"name": "Problem Solver", "emoji": "💡", "condition": "Get 10 questions correct"},
    ]

    unlocked = []
    for ach in all_achievements:
        if ach["name"] == "First Steps" and len(st.session_state.completed_lessons) >= 1:
            unlocked.append(ach)
        elif ach["name"] == "Knowledge Seeker" and len(st.session_state.completed_lessons) >= 5:
            unlocked.append(ach)
        elif ach["name"] == "Mastery Mind" and len([c for c in engine.profile['concept_mastery'].values() if c == 'mastered']) >= 3:
            unlocked.append(ach)
        elif ach["name"] == "Streak Starter" and st.session_state.streak >= 3 and engine.streak_opt_in:
            unlocked.append(ach)
        elif ach["name"] == "Problem Solver" and engine.profile['total_correct'] >= 10:
            unlocked.append(ach)

    for ach in unlocked:
        if ach["name"] not in st.session_state.achievements:
            st.session_state.achievements.append(ach["name"])

    st.subheader("🏅 Unlocked")
    col1, col2, col3 = st.columns(3)
    for i, ach in enumerate(unlocked):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
            <div style="background: #e8f5e9; border-radius: 10px; padding: 15px; margin: 5px; text-align: center; border: 2px solid #2e7d32;">
                <span style="font-size: 2rem;">{ach['emoji']}</span>
                <br><strong>{ach['name']}</strong>
                <br><span style="font-size: 0.8rem;">{ach['condition']}</span>
            </div>
            """, unsafe_allow_html=True)

    st.subheader("🔒 Locked")
    locked = [a for a in all_achievements if a["name"] not in [u["name"] for u in unlocked]]
    for i, ach in enumerate(locked):
        with [col1, col2, col3][i % 3]:
            st.markdown(f"""
            <div style="background: #f5f5f5; border-radius: 10px; padding: 15px; margin: 5px; text-align: center; opacity: 0.6;">
                <span style="font-size: 2rem;">{ach['emoji']}</span>
                <br><strong>{ach['name']}</strong>
                <br><span style="font-size: 0.8rem;">Need: {ach['condition']}</span>
            </div>
            """, unsafe_allow_html=True)


def show_spaced_repetition():
    st.header(f"🧠 Spaced Repetition Review - {country_code.title()}")
    engine = get_student_engine()

    due_concepts = []
    for concept in engine.knowledge_graph.keys():
        review = engine.get_review_prompt(concept)
        if review:
            due_concepts.append((concept, review))

    if not due_concepts:
        st.success("🎉 All caught up! No concepts due for review.")
        return

    st.info(f"📚 {len(due_concepts)} concepts are due for review.")

    for concept, review_data in due_concepts:
        with st.expander(f"🔄 Review: {concept.replace('_', ' ').title()}"):
            st.markdown(f"**Prompt:** {review_data['prompt']}")
            st.markdown(f"**Current Interval:** {review_data['interval']} days")
            st.markdown(f"**Ease Factor:** {review_data['ease_factor']:.2f}")

            quality = st.slider("Rating (0 = Forgot, 5 = Perfect)", 0, 5, 3, key=f"quality_{concept}")
            if st.button(f"Submit Review for {concept}", key=f"submit_review_{concept}"):
                engine.update_review(concept, quality)
                st.success(f"✅ Review recorded! Next review in "
                           f"{engine.review_data[concept]['interval']} days.")
                st.rerun()


def show_knowledge_graph():
    st.header(f"🗺️ Knowledge Graph - {country_code.title()}")
    engine = get_student_engine()
    tree = engine.get_mastery_tree()

    st.subheader("📋 Concept Dependencies")
    for concept, data in tree.items():
        status_icon = {'locked': '🔒', 'in_progress': '🟡', 'mastered': '🟢'}.get(data['status'], '⚪')
        prereq_str = ", ".join(data['prerequisites']) if data['prerequisites'] else "None"
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 10px; padding: 8px; border-bottom: 1px solid #eee;">
            <span style="font-size: 1.2rem;">{status_icon}</span>
            <span style="font-weight: 600; flex: 1;">{concept.replace('_', ' ').title()}</span>
            <span style="color: #666; font-size: 0.9rem;">Prereqs: {prereq_str}</span>
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("🔍 Check Prerequisites")
    check_concept = st.selectbox("Select a concept:", list(engine.knowledge_graph.keys()))
    if check_concept:
        prereqs = engine.knowledge_graph.get(check_concept, [])
        met = engine.is_prereq_met(check_concept)
        if met:
            st.success(f"✅ All prerequisites for '{check_concept}' are met!")
        else:
            st.warning(f"⚠️ Missing prerequisites for '{check_concept}':")
            for prereq in prereqs:
                status = engine.profile['concept_mastery'].get(prereq, 'locked')
                if status != 'mastered':
                    st.markdown(f"- {prereq} ({status})")


def show_voice_recall():
    st.header(f"🎙️ Voice-First Active Recall - {country_code.title()}")

    st.markdown("""
    <div class="ai-disclosure">
    <strong>AI Disclosure:</strong> This assessment evaluates the <strong>content</strong>
    of spoken answers only. It does <strong>not</strong> infer emotional state, attention,
    or affect. This design avoids the EU AI Act Art. 5(1)(f) prohibited practice of
    emotion recognition in education.
    </div>
    """, unsafe_allow_html=True)

    engine = get_student_engine()
    st.caption("Explain a concept out loud to test your verbal comprehension.")

    concept = st.selectbox("Select a concept to explain:", list(engine.knowledge_graph.keys())[:10])

    if st.button("🎙️ Start Recording (Simulated)"):
        with st.spinner("Processing voice input..."):
            result = engine.process_voice_input(b"simulated_audio_data")

        st.success("✅ Voice Processing Complete!")
        st.markdown(f"**📝 Transcript:** {result['transcript']}")
        st.markdown(f"**🧠 Content Comprehension Score:** {result['content_comprehension_score']*100:.0f}%")
        st.info(f"**💬 Disclosure:** {result['disclosure']}")

        with st.expander("🔒 What this does NOT do"):
            for item in result['explicitly_not_used_for']:
                st.markdown(f"- ❌ {item}")


def show_content_shield():
    st.header(f"🛡️ Content Shield - {country_code.title()}")
    engine = get_student_engine()
    st.caption("Strict filters block non-academic, cheating, or inappropriate prompts.")

    prompt = st.text_input("Enter a prompt or question:", key="shield_prompt")
    if prompt and st.button("🔍 Check Content"):
        result = engine.filter_content(prompt)
        if result['allowed']:
            st.success("✅ Content is appropriate for academic use.")
        else:
            st.error(f"⛔ Content blocked! Terms: {', '.join(result['blocked_terms'])}")


def show_student_document_analysis():
    st.header(f"📄 Document & OCR Analysis - {country_code.title()}")
    engine = get_student_engine()

    tab1, tab2 = st.tabs(["📄 Document Upload", "📸 OCR Image Upload"])

    with tab1:
        uploaded_file = st.file_uploader(
            "📤 Upload Document",
            type=['pdf', 'docx', 'txt', 'csv', 'json'],
            key="student_doc"
        )
        if uploaded_file is not None:
            doc_engine = DocumentIntelligenceEngine(st.session_state.country_code)
            with st.spinner("Analyzing document..."):
                text = doc_engine.extract_text_from_file(uploaded_file)
                analysis = doc_engine.analyze_document(text, 'Student')
            st.success("✅ Document Analysis Complete!")
            col1, col2, col3 = st.columns(3)
            col1.metric("Word Count", analysis.get('word_count', 0))
            col2.metric("Academic Score", f"{analysis.get('academic_language_score', 0)}%")
            col3.metric("Sentiment", analysis.get('sentiment', {}).get('sentiment', 'Neutral'))

    with tab2:
        st.caption("Upload an image of handwritten math, diagrams, or textbook pages")
        uploaded_image = st.file_uploader(
            "📸 Upload Image",
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp'],
            key="ocr_image"
        )
        if uploaded_image is not None:
            st.image(uploaded_image, caption="Uploaded Image", use_container_width=True)
            if st.button("🔍 Process OCR", type="primary"):
                with st.spinner("Processing OCR..."):
                    result = engine.process_ocr_image(uploaded_image.getvalue())
                st.success("✅ OCR Processing Complete!")
                st.markdown(f"**Extracted Text:** {result['extracted_text']}")
                st.markdown(f"**AI Task:** {result['ai_task']}")


# ==================== TEACHER UI FUNCTIONS ====================

def show_teacher_dashboard():
    st.header(f"👨‍🏫 Teacher Intelligence Dashboard - {country_code.title()}")
    teacher_engine = TeacherOutcomeEngine(country_code)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Lesson Plans", len(teacher_engine.intelligence.lesson_plans))
    col2.metric("📝 Quizzes", len(teacher_engine.intelligence.quizzes))
    col3.metric("📊 Rubrics", len(teacher_engine.intelligence.rubrics))
    col4.metric("⏱️ Hours Saved", "7.0 hrs", "↑ 15%")

    st.subheader("⏱️ Time Saved This Week")
    time_saved = teacher_engine.calculate_time_saved()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Hours Saved", f"{time_saved['total_hours_saved']} hrs",
                f"{time_saved['total_percent_saved']}%")
    col2.metric("Lesson Planning", f"{time_saved['breakdown']['lesson_planning']['hours']} hrs")
    col3.metric("Grading", f"{time_saved['breakdown']['grading']['hours']} hrs")
    col4.metric("Admin Work", f"{time_saved['breakdown']['admin_work']['hours']} hrs")

    with st.expander("📚 Recent Lesson Plans", expanded=True):
        for plan in teacher_engine.intelligence.lesson_plans[-3:]:
            st.markdown(f"""
            <div class="teacher-card">
            <strong>{plan.title}</strong>
            <br>Subject: {plan.subject} | Grade: {plan.grade_level} | Duration: {plan.duration} min
            </div>
            """, unsafe_allow_html=True)


def show_teacher_lesson_builder():
    st.header(f"📋 Lesson Builder - {country_code.title()}")
    st.caption("Create complete lesson bundles with slide outlines, worksheets, and answer keys")

    teacher_engine = TeacherOutcomeEngine(country_code)

    st.subheader("🚀 Multi-Asset Bundle Generator")

    col1, col2 = st.columns(2)
    with col1:
        subject = st.selectbox("Subject:", ['Science', 'Mathematics', 'English Language', 'Geography', 'History'])
        grade = st.selectbox("Grade Level:", overlay.get('grade_levels',
                                                        ['Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5',
                                                         'Grade 6', 'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10']))
        topic = st.text_input("Topic:", "Photosynthesis")
    with col2:
        duration = st.slider("Lesson Duration (minutes):", 30, 90, 45)

    if st.button("✨ Generate Complete Lesson Bundle", type="primary"):
        with st.spinner("Generating lesson bundle..."):
            bundle = teacher_engine.generate_lesson_bundle(subject, grade, topic, duration)

        st.success(f"✅ Lesson Bundle Generated! Bundle ID: {bundle['bundle_id']}")

        if '_ai_disclosure' in bundle:
            st.markdown(f'<div class="ai-disclosure">{bundle["_ai_disclosure"]["disclosure_text"]}</div>',
                        unsafe_allow_html=True)

        tabs = st.tabs(["📋 Lesson Plan", "📊 Slide Outline", "📝 Worksheet", "🔑 Answer Key"])

        with tabs[0]:
            st.markdown(f"### {bundle['lesson_plan']['title']}")
            st.markdown(f"**Objectives:**")
            for obj in bundle['lesson_plan']['objectives']:
                st.markdown(f"- {obj}")

        with tabs[1]:
            for slide in bundle['slide_outline']:
                st.markdown(f"**Slide {slide['slide']}:** {slide['title']}")

        with tabs[2]:
            st.markdown(f"### {bundle['worksheet']['title']}")
            for section in bundle['worksheet']['sections']:
                st.markdown(f"**{section['section']}**")

        with tabs[3]:
            st.markdown(f"### {bundle['answer_key']['title']}")


def show_teacher_assessment():
    st.header(f"📝 Assessment Engine - {country_code.title()}")
    teacher_engine = TeacherOutcomeEngine(country_code)

    st.subheader("📊 Rubric Generator")
    col1, col2 = st.columns(2)
    with col1:
        rubric_title = st.text_input("Rubric Title:", "Science Lab Report Rubric")
        criteria_list = st.text_area("Criteria (one per line):",
                                     "Hypothesis\nProcedure\nData Collection\nAnalysis\nConclusion")
    with col2:
        levels_list = st.text_input("Levels (comma-separated):",
                                    "Excellent, Proficient, Developing, Beginning")

    if st.button("✨ Generate Rubric", type="primary"):
        criteria = [c.strip() for c in criteria_list.split('\n') if c.strip()]
        levels = [l.strip() for l in levels_list.split(',') if l.strip()]
        if criteria and levels:
            rubric = teacher_engine.generate_rubric(rubric_title, criteria, levels)
            st.success(f"✅ Rubric Generated: {rubric.title}")

    st.divider()
    st.subheader("📝 Quiz Generator")
    col1, col2 = st.columns(2)
    with col1:
        quiz_subject = st.selectbox("Subject:", ['Science', 'Mathematics', 'English Language'], key="quiz_subject")
        quiz_grade = st.selectbox("Grade Level:",
                                  overlay.get('grade_levels', ['Grade 1', 'Grade 7']),
                                  key="quiz_grade")
        quiz_topic = st.text_input("Topic:", "Photosynthesis")
    with col2:
        num_questions = st.slider("Number of Questions:", 3, 15, 5)

    if st.button("✨ Generate Quiz", type="primary"):
        quiz = teacher_engine.generate_quiz(quiz_subject, quiz_grade, quiz_topic, num_questions)
        st.success(f"✅ Quiz Generated: {quiz.title}")


def show_teacher_hours_saved():
    st.header(f"⏱️ Time-Saved Dashboard - {country_code.title()}")
    teacher_engine = TeacherOutcomeEngine(country_code)
    time_saved = teacher_engine.calculate_time_saved()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Hours Saved", f"{time_saved['total_hours_saved']} hrs",
                f"{time_saved['total_percent_saved']}%")
    col2.metric("Monthly Projection", f"{time_saved['monthly_projection']} hrs")
    col3.metric("Yearly Projection", f"{time_saved['yearly_projection']} hrs")

    st.subheader("📊 Time Saved Breakdown")
    breakdown_data = []
    for category, data in time_saved['breakdown'].items():
        breakdown_data.append({
            'Category': category.replace('_', ' ').title(),
            'Hours Saved': data['hours'],
            'Comparison': data['saved']
        })
    st.dataframe(pd.DataFrame(breakdown_data))

    st.divider()
    st.subheader("🔒 Zero-PII Compliance Layer")
    st.caption("Client-side redaction of names and PII. FERPA/COPPA data-minimisation principles.")

    text_with_pii = st.text_area(
        "Enter text with PII to redact:",
        height=100,
        value="John Smith scored 95%. Contact john.smith@school.com for more info."
    )

    if st.button("🔒 Redact PII"):
        redacted = teacher_engine.redact_pii(text_with_pii)
        st.markdown("**Redacted Text:**")
        st.text(redacted['redacted'])
        st.caption(redacted['compliance_note'])


def show_teacher_lms_integration():
    st.header(f"📑 LMS Integration - {country_code.title()}")
    teacher_engine = TeacherOutcomeEngine(country_code)

    st.subheader("🔗 Connect to LMS")
    lms_options = ['google_classroom', 'canvas', 'schoology', 'microsoft_teams']
    lms_names = {
        'google_classroom': 'Google Classroom 📚',
        'canvas': 'Canvas 🎨',
        'schoology': 'Schoology 📖',
        'microsoft_teams': 'Microsoft Teams 💬'
    }

    for lms in lms_options:
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.markdown(f"**{lms_names.get(lms, lms)}**")
        with col2:
            if st.button(f"Connect", key=f"connect_{lms}"):
                result = teacher_engine.connect_lms(lms, {'api_key': 'demo_key'})
                if result['status'] == 'connected':
                    st.success(f"✅ Connected to {result['config']['name']}")


def show_teacher_standards_mapping():
    st.header(f"🎯 Standards Mapping - {country_code.title()}")
    teacher_engine = TeacherOutcomeEngine(country_code)

    standard_types = {
        'common_core': 'Common Core State Standards',
        'ngss': 'Next Generation Science Standards (NGSS)',
        'teks': 'Texas Essential Knowledge and Skills (TEKS)',
        'cbc': 'Competency Based Curriculum (CBC)',
        'nctb': 'National Curriculum (NCTB)'
    }

    selected_standard = st.selectbox(
        "Select Standards Type:",
        list(standard_types.keys()),
        format_func=lambda x: standard_types.get(x, x)
    )

    if selected_standard in teacher_engine.intelligence.standard_databases:
        db = teacher_engine.intelligence.standard_databases[selected_standard]
        for category, standards in db.items():
            st.markdown(f"### {category}")
            st.markdown(", ".join(standards))


# ==================== PROFESSIONAL UI ====================

def show_professional_dashboard():
    st.header(f"💼 Professional Intelligence Dashboard - {country_code.title()}")
    prof_engine = ProfessionalOutcomeEngine(st.session_state.domain, country_code)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📚 Documents", len(prof_engine.intelligence.documents))
    col2.metric("📊 Portfolio Value", "$75,825")
    col3.metric("⚠️ Watchdog Alerts", len(prof_engine.get_watchdog_alerts()))
    col4.metric("⏱️ Time Saved", "18 hrs")

    st.subheader("📊 Portfolio Overview")
    portfolio_metrics = prof_engine.get_portfolio_metrics()
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Value", f"${portfolio_metrics['total_value']:,.2f}")
    col2.metric("Volatility", f"{portfolio_metrics['volatility']:.2%}")
    col3.metric("Sharpe Ratio", f"{portfolio_metrics['sharpe_ratio']:.2f}")
    col4.metric("Concentration Risk", f"{portfolio_metrics['concentration_risk']:.1%}")

    st.subheader("⚡ Watchdog Alerts")
    for alert in prof_engine.get_watchdog_alerts()[-5:]:
        severity_color = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(alert.severity, '🔵')
        st.markdown(f"""
        <div class="watchdog-alert">
        <strong>{severity_color} {alert.asset_ticker}</strong> - {alert.alert_type.upper()}
        <br>{alert.message}
        <br><small>Source: {alert.source} | {alert.timestamp.strftime('%Y-%m-%d %H:%M')}</small>
        </div>
        """, unsafe_allow_html=True)


def show_professional_research():
    st.header(f"🔬 Research & Analysis - {country_code.title()}")
    prof_engine = ProfessionalOutcomeEngine(st.session_state.domain, country_code)

    st.subheader("🔍 Hybrid Search Engine")
    col1, col2 = st.columns([3, 1])
    with col1:
        search_query = st.text_input("Search query:",
                                     placeholder="e.g., 'TechCorp Q4 2024 earnings revenue'")
    with col2:
        search_type = st.selectbox("Search Type:", ['hybrid', 'keyword', 'vector', 'semantic'])

    if search_query:
        with st.spinner("Searching..."):
            results = prof_engine.hybrid_search(search_query, search_type)

        if results:
            st.success(f"✅ Found {len(results)} results")
            for result in results[:5]:
                doc = result['document']
                with st.expander(f"📄 {doc.title} (Score: {result['score']:.3f})"):
                    st.markdown(f"**Source Type:** {doc.source_type}")
                    st.markdown(f"**Matches:** {', '.join(result['matches'][:5])}")

    st.divider()
    st.subheader("🧮 Data Sandbox")
    st.info("⚠️ Code execution is disabled in this prototype for security reasons. "
            "A production version would use an isolated subprocess sandbox.")
    st.caption("This design reflects security-by-default principles.")


def show_professional_portfolio():
    st.header(f"📊 Portfolio Intelligence - {country_code.title()}")
    prof_engine = ProfessionalOutcomeEngine(st.session_state.domain, country_code)

    portfolio_metrics = prof_engine.get_portfolio_metrics()
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Value", f"${portfolio_metrics['total_value']:,.2f}")
    col2.metric("Volatility", f"{portfolio_metrics['volatility']:.2%}")
    col3.metric("Sharpe Ratio", f"{portfolio_metrics['sharpe_ratio']:.2f}")

    st.subheader("📊 Sector Concentration")
    sector_data = pd.DataFrame({
        'Sector': list(portfolio_metrics['sector_exposure'].keys()),
        'Weight': [f"{v:.1%}" for v in portfolio_metrics['sector_exposure'].values()]
    })
    st.dataframe(sector_data)

    st.divider()
    st.subheader("🌍 Macro Scenario Stress-Testing")

    col1, col2 = st.columns(2)
    with col1:
        scenario_name = st.text_input("Scenario Name:", "Rate Hike Scenario")
        rate_change = st.slider("Rate Change (bps):", -100, 100, 25) / 100
        inflation_change = st.slider("Inflation Change (%):", -5, 5, 2) / 100
        growth_change = st.slider("Growth Change (%):", -5, 5, 1) / 100
        market_shock = st.slider("Market Shock (%):", -20, 20, -5) / 100

    with col2:
        if st.button("🧪 Run Stress Test", type="primary"):
            scenario = MacroScenario(
                name=scenario_name, description="", rate_change=rate_change,
                inflation_change=inflation_change, growth_change=growth_change,
                market_shock=market_shock, portfolio_impact=0.0
            )
            with st.spinner("Running stress test..."):
                stress_results = prof_engine.run_stress_test(scenario)
            st.success("✅ Stress Test Complete!")
            st.metric("Portfolio Impact", f"{stress_results['total_return']:.1f}%")
            st.metric("Risk Assessment", stress_results['risk_assessment'])


def show_professional_workspace():
    st.header(f"📑 Split-Screen Workspace - {country_code.title()}")
    prof_engine = ProfessionalOutcomeEngine(st.session_state.domain, country_code)
    workspace_data = prof_engine.get_workspace_data()

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📝 Working Notes")
        st.text_area("Notes:", height=400, value="# Research Notes\n...")
    with col2:
        st.subheader("📄 Source Documents")
        for doc in workspace_data['documents']:
            with st.expander(f"📄 {doc['title']}"):
                st.markdown(f"**Type:** {doc['type']}")


def show_professional_watchdogs():
    st.header(f"⚡ 24/7 Asset Watchdogs - {country_code.title()}")
    prof_engine = ProfessionalOutcomeEngine(st.session_state.domain, country_code)

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔄 Refresh All Watchdogs", type="primary"):
            new_alerts = prof_engine.refresh_watchdogs()
            if new_alerts:
                st.success(f"✅ {len(new_alerts)} new alerts detected!")
                st.rerun()
            else:
                st.info("No new alerts detected.")

    for alert in prof_engine.get_watchdog_alerts():
        severity_color = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}.get(alert.severity, '🔵')
        st.markdown(f"""
        <div class="watchdog-alert">
        <strong>{severity_color} {alert.asset_ticker}</strong> - {alert.alert_type.upper()}
        <br>{alert.message}
        </div>
        """, unsafe_allow_html=True)

    st.divider()
    st.subheader("📈 Real-Time Market Feeds")
    ticker = st.text_input("Enter Ticker:", "AAPL")
    if ticker:
        tab1, tab2, tab3 = st.tabs(["📊 Market Data", "📄 SEC Filings", "🎙️ Earnings Call"])
        with tab1:
            market_data = prof_engine.get_market_data(ticker)
            st.json(market_data)
        with tab2:
            filings = prof_engine.get_sec_filing(ticker)
            st.json(filings)
        with tab3:
            earnings = prof_engine.get_earnings_call(ticker)
            st.json(earnings)


# ==================== DOCUMENT ANALYSIS COMPONENT ====================

def show_document_analysis():
    st.header(f"📄 Document Intelligence - {user_role}")

    uploaded_file = st.file_uploader(
        "📤 Upload Document",
        type=['pdf', 'docx', 'txt', 'csv', 'json'],
    )

    if uploaded_file is not None:
        st.info(f"📎 **File:** {uploaded_file.name} ({uploaded_file.size / 1024:.2f} KB)")

        doc_engine = DocumentIntelligenceEngine(st.session_state.country_code)
        with st.spinner("📖 Extracting and analyzing document..."):
            text = doc_engine.extract_text_from_file(uploaded_file)

        if text.startswith("Error") or text.startswith("Unsupported"):
            st.error(f"⚠️ {text}")
        else:
            with st.expander("📝 Document Preview"):
                preview = text[:1000] + ("..." if len(text) > 1000 else "")
                st.text_area("Content Preview", preview, height=200)

            with st.spinner("🧠 Analyzing..."):
                analysis = doc_engine.analyze_document(text, user_role)

            st.success("✅ Document Analysis Complete!")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("📊 Word Count", analysis.get('word_count', 0))
            col2.metric("📝 Sentences", analysis.get('sentence_count', 0))
            col3.metric("🎯 Key Phrases", len(analysis.get('key_phrases', [])))
            col4.metric("💬 Sentiment", analysis.get('sentiment', {}).get('sentiment', 'Neutral'))

            st.subheader("📖 Readability Analysis")
            readability = analysis.get('readability', {})
            col1, col2, col3 = st.columns(3)
            col1.metric("Flesch Score", readability.get('flesch_score', 'N/A'))
            col2.metric("Grade Level", readability.get('grade_level', 'Unknown'))


# ==================== SME UI FUNCTIONS ====================

def show_sme_dashboard():
    st.header(f"🏢 SME Growth Automation Engine - {country_code.title()}")

    sme_engine = SMEOutcomeEngine('africa' if country_code in ['kenya', 'bangladesh'] else 'global',
                                  country_code)

    business_data = {
        'inventory': [
            {'id': 'SKU-001', 'name': 'Product A', 'quantity': 45, 'threshold': 50, 'price': 25.00},
            {'id': 'SKU-002', 'name': 'Product B', 'quantity': 12, 'threshold': 20, 'price': 15.00},
            {'id': 'SKU-003', 'name': 'Product C', 'quantity': 3, 'threshold': 10, 'price': 35.00},
        ],
        'invoices': [
            {'id': 'INV-001', 'amount': 150.00, 'status': 'paid', 'due_date': '2024-01-20'},
            {'id': 'INV-002', 'amount': 75.50, 'status': 'overdue', 'due_date': '2024-01-10'},
        ],
        'customers': [
            {'id': 1, 'name': 'John Doe', 'days_since_last_order': 45,
             'avg_order_value': 75, 'order_count': 3, 'months_active': 6, 'frequency': 0.5},
            {'id': 2, 'name': 'Jane Smith', 'days_since_last_order': 12,
             'avg_order_value': 120, 'order_count': 8, 'months_active': 12, 'frequency': 1.5},
        ]
    }

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📊 Revenue", "$15,750", "↑ 12.5%")
    col2.metric("👥 Customers", "342", "↑ 8.3%")
    col3.metric("📦 Inventory Items", "1,247", "↓ 3.2%")
    col4.metric("⚡ Automation Rate", "68%", "↑ 12%")

    st.subheader("🎯 Action-Oriented Task Feed")
    tasks = sme_engine.get_action_tasks(business_data)

    for task in tasks[:10]:
        priority_class = {
            'critical': 'task-critical', 'high': 'task-high',
            'medium': 'task-medium', 'low': 'task-low'
        }.get(task.priority, 'task-medium')

        st.markdown(f'<div class="{priority_class}">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns([5, 2, 1])
        with col1:
            st.markdown(f"**{task.title}**")
            st.caption(task.description)
            st.caption(f"💡 Impact: {task.impact}")
        with col2:
            st.caption(f"Priority: {task.priority.upper()}")
        with col3:
            if task.status == 'pending':
                if st.button(f"✅", key=f"approve_{task.id}"):
                    sme_engine.ux_engine.approve_task(task.id)
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    st.divider()
    st.subheader("💬 AI Business Assistant")
    query = st.text_input("What would you like to know?",
                          placeholder="e.g., 'What's my cash flow forecast?'")

    if query:
        with st.spinner("Analyzing..."):
            response = sme_engine.natural_language_query(query, business_data)

        if '_ai_disclosure' in response:
            st.markdown(f'<div class="ai-disclosure">{response["_ai_disclosure"]["disclosure_text"]}</div>',
                        unsafe_allow_html=True)

        for result in response.get('results', []):
            st.markdown(f"**{result.get('type', 'Analysis').title()}**")
            st.info(result.get('summary', 'No summary'))


def show_sme_growth():
    st.header(f"📈 SME Growth Analytics - {country_code.title()}")
    ai_engine = SMEAIEngine(country_code)

    tab1, tab2, tab3, tab4 = st.tabs(["💰 Cash Flow", "📊 Churn", "📦 Inventory", "💎 LTV"])

    with tab1:
        cash_flow = ai_engine.predict_cash_flow([])
        df = pd.DataFrame(cash_flow['predictions'])
        st.line_chart(df.set_index('day')['balance'])
        col1, col2, col3 = st.columns(3)
        col1.metric("Min Balance", f"${cash_flow['min_balance']:,.2f}",
                    f"Day {cash_flow['min_balance_day']}")
        col2.metric("Avg Daily Balance", f"${cash_flow['avg_daily_balance']:,.2f}")
        col3.metric("Risk Level", cash_flow['risk_level'].upper())
        st.caption(cash_flow.get('note', ''))

    with tab2:
        customers = [
            {'id': 1, 'name': 'John Doe', 'days_since_last_order': 45,
             'avg_order_value': 75, 'order_count': 3},
            {'id': 2, 'name': 'Jane Smith', 'days_since_last_order': 12,
             'avg_order_value': 120, 'order_count': 8},
        ]
        churn_predictions = ai_engine.predict_churn(customers)
        st.dataframe(pd.DataFrame(churn_predictions))

    with tab3:
        inventory_data = [
            {'id': 'SKU-001', 'name': 'Product A', 'quantity': 45, 'threshold': 50, 'daily_sales_avg': 2.5},
            {'id': 'SKU-002', 'name': 'Product B', 'quantity': 12, 'threshold': 20, 'daily_sales_avg': 1.8},
        ]
        inventory_forecast = ai_engine.predict_inventory_depletion(inventory_data)
        st.dataframe(pd.DataFrame(inventory_forecast))

    with tab4:
        customer_data = [
            {'id': 1, 'name': 'John Doe', 'avg_order_value': 75, 'frequency': 0.5, 'months_active': 6},
            {'id': 2, 'name': 'Jane Smith', 'avg_order_value': 120, 'frequency': 1.5, 'months_active': 12},
        ]
        ltv_predictions = ai_engine.predict_customer_ltv(customer_data)
        st.dataframe(pd.DataFrame(ltv_predictions))


def show_sme_automation():
    st.header(f"🤖 SME Automation Solutions - {country_code.title()}")
    sme_engine = SMEOutcomeEngine('africa' if country_code in ['kenya', 'bangladesh'] else 'global',
                                  country_code)

    col1, col2 = st.columns(2)
    with col1:
        business_type = st.selectbox("Business Type:",
                                     ['retail', 'service', 'agriculture', 'manufacturing', 'tech'])
        if st.button("🚀 Generate Automation Plan", type="primary"):
            automations = sme_engine.generate_automation(business_type)
            st.success(f"✅ Automation Plan for {business_type.title()}")
            for key, value in automations.items():
                st.markdown(f"- **{key.title()}:** {value}")

    with col2:
        st.subheader("📊 Expected Impact")
        st.metric("⏱️ Time Savings", "15-25 hours/week")
        st.metric("📈 Revenue Increase", "20-30%")


def show_sme_api_connectors():
    st.header(f"🔌 API Connector Layer - {country_code.title()}")
    sme_engine = SMEOutcomeEngine('africa' if country_code in ['kenya', 'bangladesh'] else 'global',
                                  country_code)

    api_options = ['stripe', 'quickbooks', 'shopify', 'toast', 'jobber']
    api_icons = {'stripe': '💳', 'quickbooks': '📊', 'shopify': '🛍️',
                 'toast': '🍽️', 'jobber': '🔧'}

    for api in api_options:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{api_icons.get(api, '🔌')} {api.title()}**")
        with col2:
            if st.button(f"Connect", key=f"connect_{api}"):
                result = sme_engine.connect_api(api, {'api_key': 'demo'})
                if result['status'] == 'connected':
                    st.success(f"✅ {result['message']}")


def show_sme_webhooks():
    st.header(f"⚡ Webhook Architecture - {country_code.title()}")
    sme_engine = SMEOutcomeEngine('africa' if country_code in ['kenya', 'bangladesh'] else 'global',
                                  country_code)

    webhook_events = [
        {'event': 'checkout.paid', 'description': 'Customer completes a purchase'},
        {'event': 'invoice.overdue', 'description': 'Invoice becomes overdue'},
        {'event': 'inventory.low', 'description': 'Stock drops below threshold'},
        {'event': 'customer.churn_risk', 'description': 'Customer shows churn signals'},
    ]

    st.dataframe(pd.DataFrame(webhook_events))

    st.divider()
    st.subheader("🔧 Test Webhook Simulation")

    event_type = st.selectbox("Event Type:",
                              ['checkout.paid', 'invoice.overdue', 'inventory.low', 'customer.churn_risk'])

    if event_type == 'checkout.paid':
        payload = {'amount': 150.00, 'customer': {'name': 'John Doe'}, 'order_id': 'ORD-12345'}
    elif event_type == 'invoice.overdue':
        payload = {'invoice_id': 'INV-6789', 'amount': 250.00, 'days_overdue': 5}
    elif event_type == 'inventory.low':
        payload = {'product': {'id': 'SKU-001', 'name': 'Product A', 'price': 25.00},
                   'current_qty': 3, 'threshold': 10}
    else:
        payload = {'customer': {'id': 123, 'name': 'Bob Johnson'}, 'churn_score': 0.75,
                   'days_inactive': 45, 'ltv': 500.00}

    st.json(payload)

    if st.button("⚡ Process Webhook Event", type="primary"):
        result = sme_engine.process_webhook(event_type, payload)
        st.success("✅ Webhook Event Processed!")
        st.json(result)


# ==================== MAIN NAVIGATION ====================

def main():
    if choice == '📄 Document Analysis':
        show_document_analysis()
    elif choice == '🛡️ AI Ethics':
        show_ai_ethics()
    elif choice == '🎓 Dashboard':
        show_student_dashboard()
    elif choice == '📝 Practice':
        show_student_practice()
    elif choice == '📊 Progress':
        show_student_progress()
    elif choice == '🏆 Achievements':
        show_student_achievements()
    elif choice == '🧠 Spaced Repetition':
        show_spaced_repetition()
    elif choice == '🗺️ Knowledge Graph':
        show_knowledge_graph()
    elif choice == '🎙️ Voice Recall':
        show_voice_recall()
    elif choice == '👨‍🏫 Dashboard':
        show_teacher_dashboard()
    elif choice == '📋 Lesson Builder':
        show_teacher_lesson_builder()
    elif choice == '📝 Assessment':
        show_teacher_assessment()
    elif choice == '⏱️ Hours Saved':
        show_teacher_hours_saved()
    elif choice == '📑 LMS Integration':
        show_teacher_lms_integration()
    elif choice == '🎯 Standards Mapping':
        show_teacher_standards_mapping()
    elif choice == '💼 Dashboard':
        show_professional_dashboard()
    elif choice == '🔬 Research':
        show_professional_research()
    elif choice == '📊 Portfolio':
        show_professional_portfolio()
    elif choice == '📑 Workspace':
        show_professional_workspace()
    elif choice == '⚡ Watchdogs':
        show_professional_watchdogs()
    elif choice == '🏢 Dashboard':
        show_sme_dashboard()
    elif choice == '📈 Growth':
        show_sme_growth()
    elif choice == '🤖 Automation':
        show_sme_automation()
    elif choice == '🔌 API Connectors':
        show_sme_api_connectors()
    elif choice == '⚡ Webhooks':
        show_sme_webhooks()
    else:
        st.info("Select an option from the sidebar.")


if __name__ == "__main__":
    main()
