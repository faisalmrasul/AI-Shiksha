"""
Helper Functions for AI Shiksha Application
Contains reusable utility functions
"""

import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

def format_time(minutes: int) -> str:
    """
    Convert minutes to a human-readable time format
    
    Args:
        minutes: Number of minutes
        
    Returns:
        Formatted time string (e.g., "2h 30m", "45m")
    """
    if minutes >= 60:
        hours = minutes // 60
        remaining_minutes = minutes % 60
        if remaining_minutes > 0:
            return f"{hours}h {remaining_minutes}m"
        return f"{hours}h"
    return f"{minutes}m"

def calculate_percentage(part: float, whole: float) -> float:
    """
    Calculate percentage
    
    Args:
        part: The part value
        whole: The whole value
        
    Returns:
        Percentage value
    """
    if whole == 0:
        return 0.0
    return (part / whole) * 100

def validate_email(email: str) -> bool:
    """
    Validate email format
    
    Args:
        email: Email string to validate
        
    Returns:
        True if valid, False otherwise
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_phone(phone: str) -> bool:
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

def generate_progress_bar(percentage: float, width: int = 30) -> str:
    """
    Generate a text-based progress bar
    
    Args:
        percentage: Progress percentage (0-100)
        width: Width of the progress bar in characters
        
    Returns:
        Progress bar string
    """
    filled_length = int(width * percentage // 100)
    bar = '█' * filled_length + '░' * (width - filled_length)
    return f"[{bar}] {percentage:.1f}%"

def get_learning_recommendations(
    user_type: str,
    progress_data: Dict[str, Any],
    content_data: Dict[str, Any]
) -> List[str]:
    """
    Generate personalized learning recommendations
    
    Args:
        user_type: Type of user (student, teacher, professional, business)
        progress_data: User's progress data
        content_data: Available content data
        
    Returns:
        List of recommendation strings
    """
    recommendations = []
    
    if user_type == "student":
        # Get user's weak subjects
        mcq_scores = progress_data.get('mcq_scores', {})
        weak_subjects = []
        
        for subject, score in mcq_scores.items():
            if score < 60:
                weak_subjects.append(subject)
        
        if weak_subjects:
            recommendations.append(f"📚 Focus on improving: {', '.join(weak_subjects)}")
        else:
            recommendations.append("🌟 Great job! Try advanced topics in your favorite subjects")
        
        # Study time recommendation
        daily_study = progress_data.get('daily_study_time', 0)
        if daily_study < 30:
            recommendations.append("⏰ Try to study at least 30 minutes daily for better results")
    
    elif user_type == "teacher":
        tools_used = progress_data.get('tools_used', {})
        if len(tools_used) < 3:
            recommendations.append("💡 Explore more AI tools for your teaching practice")
        else:
            recommendations.append("👏 You're using multiple AI tools - great adoption!")
    
    elif user_type == "professional":
        skill_level = progress_data.get('skill_level', 0)
        if skill_level < 50:
            recommendations.append("📈 Complete more courses to advance your AI skills")
        elif skill_level < 75:
            recommendations.append("🎯 You're making good progress - try applying skills in projects")
        else:
            recommendations.append("🏆 Advanced level - consider becoming a mentor")
    
    elif user_type == "business":
        tools_adopted = progress_data.get('tools_adopted', 0)
        if tools_adopted < 3:
            recommendations.append("🚀 Consider adopting more AI tools for business growth")
        else:
            recommendations.append("📊 Your business is becoming AI-driven - explore advanced automation")
    
    return recommendations

def format_date(date_string: str) -> str:
    """
    Format date string to a readable format
    
    Args:
        date_string: ISO format date string
        
    Returns:
        Formatted date string (e.g., "January 15, 2026")
    """
    try:
        date_obj = datetime.fromisoformat(date_string)
        return date_obj.strftime("%B %d, %Y")
    except:
        return date_string

def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a maximum length with ellipsis
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."

def load_json_file(file_path: str) -> Dict[str, Any]:
    """
    Load JSON file safely
    
    Args:
        file_path: Path to JSON file
        
    Returns:
        Dictionary containing JSON data
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def save_json_file(file_path: str, data: Dict[str, Any]) -> bool:
    """
    Save data to JSON file safely
    
    Args:
        file_path: Path to JSON file
        data: Data to save
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def get_user_level(progress_data: Dict[str, Any]) -> str:
    """
    Determine user's learning level based on progress
    
    Args:
        progress_data: User progress data
        
    Returns:
        Level string (Beginner, Intermediate, Advanced)
    """
    if not progress_data:
        return "Beginner"
    
    # Calculate overall progress
    progress_score = 0
    count = 0
    
    if 'mcq_average' in progress_data:
        progress_score += progress_data['mcq_average']
        count += 1
    
    if 'skill_level' in progress_data:
        progress_score += progress_data['skill_level']
        count += 1
    
    if 'completed_chapters' in progress_data and 'total_chapters' in progress_data:
        chapter_progress = (progress_data['completed_chapters'] / progress_data['total_chapters']) * 100
        progress_score += chapter_progress
        count += 1
    
    if count == 0:
        return "Beginner"
    
    average = progress_score / count
    
    if average >= 75:
        return "Advanced"
    elif average >= 50:
        return "Intermediate"
    else:
        return "Beginner"

def generate_study_plan(
    user_type: str,
    progress_data: Dict[str, Any],
    available_hours: int = 5
) -> Dict[str, List[str]]:
    """
    Generate a weekly study plan
    
    Args:
        user_type: User type
        progress_data: User progress data
        available_hours: Total available study hours per week
        
    Returns:
        Dictionary with days as keys and study activities as values
    """
    plan = {}
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    if user_type == "student":
        subjects = ["Mathematics", "Science", "English"]
        daily_hours = available_hours / 7
        
        for i, day in enumerate(days):
            subject = subjects[i % len(subjects)]
            plan[day] = [f"Study {subject} - {daily_hours:.1f} hours"]
            
            # Add practice if needed
            if i % 2 == 0:
                plan[day].append("Practice MCQ questions")
            if i % 3 == 0:
                plan[day].append("Review previous topics")
    
    elif user_type == "professional":
        courses = progress_data.get('in_progress_courses', [])
        if not courses:
            courses = ["Introduction to AI"]
        
        for i, day in enumerate(days):
            course = courses[i % len(courses)]
            plan[day] = [f"Complete Module: {course}", "Review key concepts"]
    
    else:
        for day in days:
            plan[day] = ["Review learning materials", "Practice with AI tools"]
    
    return plan

# Bengali language helper functions
def get_bengali_greeting() -> str:
    """Get Bengali greeting based on time of day"""
    hour = datetime.now().hour
    if hour < 12:
        return "সুপ্রভাত"  # Good morning
    elif hour < 17:
        return "শুভ বিকাল"  # Good afternoon
    else:
        return "শুভ সন্ধ্যা"  # Good evening

def translate_to_bengali(text: str) -> str:
    """
    Translate common phrases to Bengali
    Note: For full translation, use a translation API
    
    Args:
        text: English text
        
    Returns:
        Bengali translation (simplified)
    """
    translations = {
        "Welcome": "স্বাগতম",
        "Login": "লগইন",
        "Register": "নিবন্ধন",
        "Dashboard": "ড্যাশবোর্ড",
        "Learning": "শিক্ষা",
        "Progress": "অগ্রগতি",
        "Settings": "সেটিংস",
        "Student": "শিক্ষার্থী",
        "Teacher": "শিক্ষক",
        "Professional": "পেশাদার",
        "Business": "ব্যবসা",
        "AI": "কৃত্রিম বুদ্ধিমত্তা",
        "Learning Path": "শিক্ষা পথ",
        "Study Plan": "পড়াশোনার পরিকল্পনা"
    }
    
    # Simple word replacement (for demo purposes)
    for eng, bengali in translations.items():
        if eng.lower() in text.lower():
            return text.replace(eng, bengali)
    return text
