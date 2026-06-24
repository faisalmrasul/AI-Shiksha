"""
Student Module for AI Shiksha
Handles student learning features, subjects, MCQs, and study plans
"""

import streamlit as st
import json
import os  # ← ADD THIS LINE
import random
from datetime import datetime, timedelta

class StudentModule:
    def __init__(self):
        self.content_file = "data/content.json"
        self.progress_file = "data/progress.json"
        self.ensure_data_files()
        
    def ensure_data_files(self):
        """Ensure data files exist with sample content"""
        if not os.path.exists("data"):
            os.makedirs("data")
            
        # Sample content for students
        if not os.path.exists(self.content_file):
            sample_content = {
                "subjects": {
                    "mathematics": {
                        "chapters": [
                            {
                                "id": "math_ch1",
                                "title": "Algebra",
                                "topics": ["Linear Equations", "Quadratic Equations", "Polynomials"],
                                "simplified": "Algebra is the study of mathematical symbols and rules for manipulating these symbols.",
                                "mcqs": [
                                    {
                                        "question": "What is the solution to 2x + 3 = 7?",
                                        "options": ["x = 2", "x = 3", "x = 4", "x = 5"],
                                        "correct": 0,
                                        "explanation": "2x + 3 = 7 → 2x = 4 → x = 2"
                                    },
                                    {
                                        "question": "What is the value of x in x² = 25?",
                                        "options": ["5", "-5", "±5", "25"],
                                        "correct": 2,
                                        "explanation": "x² = 25 → x = ±5"
                                    }
                                ]
                            },
                            {
                                "id": "math_ch2",
                                "title": "Geometry",
                                "topics": ["Triangles", "Circles", "Coordinate Geometry"],
                                "simplified": "Geometry is the branch of mathematics concerned with shapes, sizes, and properties of space.",
                                "mcqs": [
                                    {
                                        "question": "What is the sum of angles in a triangle?",
                                        "options": ["90°", "180°", "270°", "360°"],
                                        "correct": 1,
                                        "explanation": "The sum of interior angles in a triangle is always 180°"
                                    }
                                ]
                            }
                        ]
                    },
                    "science": {
                        "chapters": [
                            {
                                "id": "sci_ch1",
                                "title": "Physics Basics",
                                "topics": ["Motion", "Force", "Energy"],
                                "simplified": "Physics is the study of matter, energy, and their interactions.",
                                "mcqs": [
                                    {
                                        "question": "What is Newton's first law of motion?",
                                        "options": ["F = ma", "Every action has an equal and opposite reaction", "An object in motion stays in motion", "Energy cannot be created or destroyed"],
                                        "correct": 2,
                                        "explanation": "Newton's first law states that an object at rest stays at rest and an object in motion stays in motion unless acted upon by an external force."
                                    }
                                ]
                            }
                        ]
                    },
                    "english": {
                        "chapters": [
                            {
                                "id": "eng_ch1",
                                "title": "Grammar Fundamentals",
                                "topics": ["Parts of Speech", "Tenses", "Sentence Structure"],
                                "simplified": "English grammar helps us communicate effectively and clearly.",
                                "mcqs": [
                                    {
                                        "question": "Which of these is a verb?",
                                        "options": ["Run", "Book", "Table", "Apple"],
                                        "correct": 0,
                                        "explanation": "'Run' is an action word, making it a verb."
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
            
            with open(self.content_file, "w") as f:
                json.dump(sample_content, f, indent=2)
    
    # ... rest of the class methods (keep all your existing methods) ...
