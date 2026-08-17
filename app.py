# app.py - AI Shiksha Global Platform with Universal Core + Local Overlay Architecture
# Built for global scalability with country-specific curriculum overlays
# Enhanced with Document Intelligence for all segments

import streamlit as st
import json
import os
import random
import pandas as pd
from datetime import datetime
import hashlib
import io
import re
from typing import Dict, List, Any, Optional

# Try to import PDF and DOCX libraries with fallback
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None

# ==================== DOCUMENT INTELLIGENCE ENGINE ====================

class DocumentIntelligenceEngine:
    """Advanced document processing and analysis for all segments"""
    
    def __init__(self, country_code='kenya'):
        self.country = country_code
        self.overlay = LocalCurriculumOverlay.get_overlay(country_code)
        self.context = LocalCurriculumOverlay.get_local_context(country_code)
    
    def extract_text_from_file(self, uploaded_file) -> str:
        """Extract text from uploaded file (PDF, DOCX, TXT)"""
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
        """Analyze document content based on user segment"""
        
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
        
        # Segment-specific analysis
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
        """Extract key phrases from text"""
        # Simple keyword extraction - can be enhanced with NLP
        stopwords = {'the', 'a', 'an', 'of', 'to', 'for', 'with', 'on', 'at', 'from', 'by', 'in', 'and', 'or', 'but'}
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        
        # Get frequency
        freq = {}
        for word in words:
            if word not in stopwords:
                freq[word] = freq.get(word, 0) + 1
        
        # Get top 5 phrases (simple approach)
        sorted_words = sorted(freq.items(), key=lambda x: x[1], reverse=True)[:10]
        
        # Try to find common bigrams
        bigrams = []
        for i in range(len(words)-1):
            if words[i] not in stopwords and words[i+1] not in stopwords:
                bigram = f"{words[i]} {words[i+1]}"
                if len(bigram) > 5:
                    bigrams.append(bigram)
        
        # Combine and deduplicate
        phrases = [w[0] for w in sorted_words if len(w[0]) > 3][:5]
        
        # Add bigrams that appear frequently
        bigram_freq = {}
        for bg in bigrams:
            bigram_freq[bg] = bigram_freq.get(bg, 0) + 1
        
        top_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)[:3]
        for bg, _ in top_bigrams:
            if bg not in phrases:
                phrases.append(bg)
        
        return phrases[:7]  # Return top 7 key phrases
    
    def _analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Basic sentiment analysis"""
        positive_words = {'good', 'great', 'excellent', 'positive', 'achievement', 'success', 'improve', 'growth', 
                         'happy', 'satisfied', 'excited', 'motivated', 'enjoy', 'love', 'best', 'outstanding'}
        negative_words = {'bad', 'poor', 'difficult', 'challenge', 'struggle', 'fail', 'failure', 'frustrating',
                         'disappointed', 'unhappy', 'stress', 'anxiety', 'worry', 'concern'}
        
        words = text.lower().split()
        positive_count = sum(1 for w in words if w in positive_words)
        negative_count = sum(1 for w in words if w in negative_words)
        
        total = positive_count + negative_count
        if total == 0:
            return {'sentiment_score': 0, 'sentiment': 'Neutral'}
        
        score = (positive_count - negative_count) / total
        sentiment = 'Positive' if score > 0.1 else 'Negative' if score < -0.1 else 'Neutral'
        
        return {'sentiment_score': round(score, 2), 'sentiment': sentiment}
    
    def _calculate_readability(self, text: str) -> Dict[str, Any]:
        """Calculate readability metrics"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s for s in sentences if len(s.strip()) > 0]
        words = text.split()
        
        if len(sentences) == 0 or len(words) == 0:
            return {'flesch_score': 0, 'grade_level': 'Unknown'}
        
        # Flesch Reading Ease (approximate)
        avg_words_per_sentence = len(words) / len(sentences)
        avg_syllables_per_word = self._count_syllables(text) / len(words)
        
        flesch_score = 206.835 - (1.015 * avg_words_per_sentence) - (84.6 * avg_syllables_per_word)
        
        # Grade level mapping
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
        
        return {
            'flesch_score': round(flesch_score, 2),
            'grade_level': grade,
            'avg_words_per_sentence': round(avg_words_per_sentence, 2)
        }
    
    def _count_syllables(self, text: str) -> int:
        """Count syllables in text (approximate)"""
        vowels = 'aeiouy'
        words = text.lower().split()
        count = 0
        for word in words:
            word_vowels = 0
            for char in word:
                if char in vowels:
                    word_vowels += 1
            if word.endswith('e'):
                word_vowels = max(1, word_vowels - 1)
            count += max(1, word_vowels)
        return count
    
    def _analyze_student_document(self, text: str) -> Dict[str, Any]:
        """Analyze student document (essay, assignment, etc.)"""
        # Look for key academic indicators
        academic_keywords = {'analyze', 'evaluate', 'synthesize', 'discuss', 'compare', 'contrast', 
                            'research', 'study', 'experiment', 'hypothesis', 'theory', 'conclusion'}
        
        words = text.lower().split()
        academic_count = sum(1 for w in words if w in academic_keywords)
        
        # Identify topics mentioned
        topics = self._extract_topics(text)
        
        return {
            'academic_language_score': round(min(100, (academic_count / len(words) * 1000)) if words else 0, 2),
            'topics_mentioned': topics[:5],
            'suggested_improvements': self._suggest_student_improvements(text, topics)
        }
    
    def _analyze_teacher_document(self, text: str) -> Dict[str, Any]:
        """Analyze teacher document (lesson plan, curriculum, etc.)"""
        # Look for pedagogical elements
        ped_keywords = {'objective', 'learning', 'outcome', 'assessment', 'rubric', 'activity', 
                       'discussion', 'project', 'group', 'individual', 'differentiation'}
        
        words = text.lower().split()
        ped_count = sum(1 for w in words if w in ped_keywords)
        
        return {
            'pedagogical_score': round(min(100, (ped_count / len(words) * 1000)) if words else 0, 2),
            'curriculum_alignment': self._check_curriculum_alignment(text),
            'suggested_enhancements': self._suggest_teacher_enhancements(text)
        }
    
    def _analyze_professional_document(self, text: str) -> Dict[str, Any]:
        """Analyze professional document (report, research, etc.)"""
        # Look for professional indicators
        prof_keywords = {'strategy', 'analysis', 'implementation', 'results', 'findings', 
                        'recommendation', 'efficiency', 'performance', 'optimization'}
        
        words = text.lower().split()
        prof_count = sum(1 for w in words if w in prof_keywords)
        
        return {
            'professional_score': round(min(100, (prof_count / len(words) * 1000)) if words else 0, 2),
            'business_context': self._extract_business_context(text),
            'actionable_insights': self._extract_actionable_insights(text)
        }
    
    def _analyze_sme_document(self, text: str) -> Dict[str, Any]:
        """Analyze SME document (business plan, operations, etc.)"""
        # Look for business indicators
        sme_keywords = {'revenue', 'cost', 'profit', 'customer', 'market', 'growth', 
                       'operations', 'supply', 'logistics', 'sales', 'marketing'}
        
        words = text.lower().split()
        sme_count = sum(1 for w in words if w in sme_keywords)
        
        return {
            'business_score': round(min(100, (sme_count / len(words) * 1000)) if words else 0, 2),
            'growth_opportunities': self._identify_growth_opportunities(text),
            'automation_candidates': self._identify_automation_candidates(text)
        }
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract topics from text"""
        common_topics = {
            'mathematics': ['algebra', 'geometry', 'calculus', 'statistics', 'arithmetic'],
            'science': ['biology', 'chemistry', 'physics', 'environment', 'experiment'],
            'literature': ['novel', 'poetry', 'drama', 'prose', 'literary'],
            'history': ['historical', 'civilization', 'ancient', 'modern', 'century'],
            'geography': ['map', 'climate', 'population', 'region', 'continent'],
            'economics': ['market', 'trade', 'investment', 'currency', 'finance'],
            'technology': ['computer', 'software', 'digital', 'programming', 'ai', 'automation'],
            'language': ['vocabulary', 'grammar', 'writing', 'reading', 'speaking']
        }
        
        found_topics = []
        text_lower = text.lower()
        
        for category, keywords in common_topics.items():
            for keyword in keywords:
                if keyword in text_lower:
                    found_topics.append(f"{category.title()}")
                    break
        
        return list(dict.fromkeys(found_topics))  # Deduplicate
    
    def _suggest_student_improvements(self, text: str, topics: List[str]) -> List[str]:
        """Suggest improvements for student work"""
        suggestions = []
        words = text.split()
        
        # Check length
        if len(words) < 100:
            suggestions.append("Consider expanding your analysis with more depth and examples.")
        elif len(words) > 1000:
            suggestions.append("Consider condensing your work for clarity and focus.")
        
        # Check academic language
        academic_words = {'analyze', 'evaluate', 'synthesize', 'compare', 'contrast', 'research'}
        has_academic = any(w in text.lower() for w in academic_words)
        if not has_academic:
            suggestions.append("Incorporate more academic language (analyze, evaluate, synthesize).")
        
        # Subject-specific suggestions
        if 'Mathematics' in topics:
            suggestions.append("Include step-by-step working for mathematical problems.")
        if 'Science' in topics:
            suggestions.append("Include more scientific evidence and references.")
        if 'Literature' in topics:
            suggestions.append("Provide more textual evidence to support your arguments.")
        if 'Language' in topics:
            suggestions.append("Include more advanced vocabulary and sentence structures.")
        
        # Country-specific suggestions
        if self.country == 'kenya':
            suggestions.append("Connect your learning to Kenyan community values and context.")
        elif self.country == 'bangladesh':
            suggestions.append("Incorporate Bengali cultural perspectives in your analysis.")
        elif self.country == 'usa':
            suggestions.append("Consider how this applies to American educational standards.")
        elif self.country == 'uk':
            suggestions.append("Align your work with British academic expectations.")
        
        return suggestions[:5]  # Return top 5 suggestions
    
    def _check_curriculum_alignment(self, text: str) -> Dict[str, Any]:
        """Check alignment with local curriculum"""
        curriculum_keywords = {
            'kenya': ['competency', 'cbc', 'knec', 'community', 'values', 'skills'],
            'bangladesh': ['nctb', 'board', 'exam', 'bangladesh', 'curriculum', 'national'],
            'usa': ['common core', 'ngss', 'standards', 'college', 'career'],
            'uk': ['national curriculum', 'gcse', 'a-level', 'academic']
        }
        
        keywords = curriculum_keywords.get(self.country, [])
        text_lower = text.lower()
        
        matched = [kw for kw in keywords if kw in text_lower]
        alignment_score = len(matched) / len(keywords) if keywords else 0
        
        return {
            'score': round(alignment_score * 100, 2),
            'matched_indicators': matched,
            'status': 'Aligned' if alignment_score > 0.5 else 'Partial' if alignment_score > 0.2 else 'Not Aligned'
        }
    
    def _suggest_teacher_enhancements(self, text: str) -> List[str]:
        """Suggest enhancements for teaching materials"""
        suggestions = []
        text_lower = text.lower()
        
        # Check for key elements
        if 'objective' not in text_lower:
            suggestions.append("Add clear learning objectives for each lesson.")
        if 'assessment' not in text_lower:
            suggestions.append("Include assessment criteria and methods.")
        if 'activity' not in text_lower:
            suggestions.append("Add interactive activities to engage students.")
        if 'differentiation' not in text_lower:
            suggestions.append("Include differentiation strategies for diverse learners.")
        
        # Check for digital integration
        if 'technology' not in text_lower and 'digital' not in text_lower:
            suggestions.append("Integrate digital tools and AI resources.")
        
        # Country-specific enhancements
        if self.country == 'kenya':
            suggestions.append("Incorporate community-based learning approaches.")
        elif self.country == 'bangladesh':
            suggestions.append("Include bilingual support (Bengali/English).")
        elif self.country == 'usa':
            suggestions.append("Emphasize college and career readiness.")
        elif self.country == 'uk':
            suggestions.append("Focus on academic rigor and depth of understanding.")
        
        return suggestions[:5]
    
    def _extract_business_context(self, text: str) -> Dict[str, Any]:
        """Extract business context from professional document"""
        context = {
            'industry': 'Not specified',
            'market': 'Not specified',
            'key_metrics': [],
            'timeline': 'Not specified'
        }
        
        text_lower = text.lower()
        
        # Try to identify industry
        industries = {
            'tech': ['software', 'technology', 'digital', 'ai', 'automation'],
            'finance': ['finance', 'banking', 'investment', 'currency'],
            'health': ['health', 'medical', 'wellness', 'clinical'],
            'retail': ['retail', 'store', 'customer', 'sales'],
            'manufacturing': ['manufacture', 'production', 'factory', 'assembly']
        }
        
        for industry, keywords in industries.items():
            if any(kw in text_lower for kw in keywords):
                context['industry'] = industry.title()
                break
        
        # Extract metrics (simple)
        metric_patterns = [
            r'(\d+[\.,]?\d*)\s*%',
            r'\$\s*(\d+[\.,]?\d*)',
            r'(\d+[\.,]?\d*)\s*million',
            r'(\d+[\.,]?\d*)\s*billion'
        ]
        
        for pattern in metric_patterns:
            matches = re.findall(pattern, text)
            if matches:
                context['key_metrics'].extend(matches[:3])
        
        return context
    
    def _extract_actionable_insights(self, text: str) -> List[str]:
        """Extract actionable insights from professional document"""
        insights = []
        
        # Look for action-oriented phrases
        action_patterns = [
            r'(recommend|suggest|should|must|need to)\s+([^.!?]+)',
            r'(implement|adopt|use|apply)\s+([^.!?]+)',
            r'(improve|enhance|optimize)\s+([^.!?]+)'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match) >= 2:
                    insight = f"{match[0]} {match[1]}"
                    if len(insight) > 10 and len(insight) < 100:
                        insights.append(insight.strip())
        
        return list(dict.fromkeys(insights))[:5]  # Deduplicate and limit
    
    def _identify_growth_opportunities(self, text: str) -> List[str]:
        """Identify growth opportunities for SME"""
        opportunities = []
        
        text_lower = text.lower()
        
        # Look for growth indicators
        if any(kw in text_lower for kw in ['new market', 'expansion', 'enter', 'customer']):
            opportunities.append("Market expansion opportunities")
        if any(kw in text_lower for kw in ['product', 'service', 'offer', 'new']):
            opportunities.append("Product/service diversification")
        if any(kw in text_lower for kw in ['digital', 'online', 'e-commerce', 'website']):
            opportunities.append("Digital transformation opportunity")
        if any(kw in text_lower for kw in ['efficiency', 'cost', 'reduce', 'save']):
            opportunities.append("Cost optimization and efficiency improvement")
        if any(kw in text_lower for kw in ['referral', 'repeat', 'loyalty', 'retention']):
            opportunities.append("Customer loyalty and retention program")
        if any(kw in text_lower for kw in ['partner', 'collaborate', 'alliance']):
            opportunities.append("Strategic partnership opportunities")
        
        # Country-specific opportunities
        if self.country == 'kenya':
            opportunities.append("Leverage mobile money and digital payments")
        elif self.country == 'bangladesh':
            opportunities.append("Explore RMG and export opportunities")
        elif self.country == 'usa':
            opportunities.append("Leverage innovation and technology sectors")
        elif self.country == 'uk':
            opportunities.append("Explore creative and financial services")
        
        return list(dict.fromkeys(opportunities))[:5]
    
    def _identify_automation_candidates(self, text: str) -> List[str]:
        """Identify automation candidates for SME"""
        candidates = []
        
        text_lower = text.lower()
        
        # Common automation candidates
        if any(kw in text_lower for kw in ['customer', 'support', 'enquiry', 'help']):
            candidates.append("Customer support chatbot")
        if any(kw in text_lower for kw in ['order', 'receipt', 'invoice', 'payment']):
            candidates.append("Automated billing and invoicing")
        if any(kw in text_lower for kw in ['inventory', 'stock', 'supply', 'warehouse']):
            candidates.append("Inventory management automation")
        if any(kw in text_lower for kw in ['marketing', 'social', 'email', 'content']):
            candidates.append("Marketing automation tools")
        if any(kw in text_lower for kw in ['report', 'analytics', 'dashboard', 'track']):
            candidates.append("Analytics and reporting automation")
        if any(kw in text_lower for kw in ['schedule', 'appointment', 'booking', 'calendar']):
            candidates.append("Scheduling and booking system")
        
        return list(dict.fromkeys(candidates))[:5]


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
        self.doc_engine = DocumentIntelligenceEngine(country_code)
    
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
            'kenya': {90: 'A (Excellent
