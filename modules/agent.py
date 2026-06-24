"""
Learning Agent Module for AI Shiksha
Tracks user progress and provides AI insights
"""

import streamlit as st
import json
import os  # ← ADD THIS LINE
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
    
    # ... rest of the class methods ...
