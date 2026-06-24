"""
Teacher Module for AI Shiksha
Handles teacher features: lesson planning, assessment, feedback
"""

import streamlit as st
import json
import os  # ← ADD THIS LINE
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
    
    # ... rest of the class methods ...
