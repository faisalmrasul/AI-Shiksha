import streamlit as st
import json

class ProfessionalModule:
    def __init__(self):
        self.role_content = {
            "healthcare": {
                "description": "AI applications in healthcare",
                "courses": [
                    "Medical Imaging and AI",
                    "Healthcare Data Analytics",
                    "Clinical Decision Support Systems",
                    "Patient Care Automation"
                ],
                "skills": ["Medical AI", "Data Analysis", "Clinical Decision Support"]
            },
            "finance": {
                "description": "AI applications in finance",
                "courses": [
                    "AI for Financial Analysis",
                    "Algorithmic Trading",
                    "Risk Assessment with AI",
                    "Fraud Detection Systems"
                ],
                "skills": ["Financial AI", "Algorithmic Trading", "Risk Management"]
            },
            "marketing": {
                "description": "AI applications in marketing",
                "courses": [
                    "AI-Powered Campaign Management",
                    "Customer Behavior Analysis",
                    "Predictive Marketing Analytics",
                    "Content Generation with AI"
                ],
                "skills": ["Marketing AI", "Analytics", "Campaign Optimization"]
            },
            "legal": {
                "description": "AI applications in legal",
                "courses": [
                    "Legal Research with AI",
                    "Contract Analysis",
                    "Case Law Prediction",
                    "Legal Document Automation"
                ],
                "skills": ["Legal AI", "Document Analysis", "Case Research"]
            }
        }
        
    def show_learning_path(self):
        """Display professional learning path"""
        st.markdown("<h2 class='sub-header'>💼 Professional AI Training</h2>", unsafe_allow_html=True)
        
        # Role selection
        role = st.selectbox(
            "Select your profession:",
            ["Healthcare", "Finance", "Marketing", "Legal", "Technology", "Education"]
        ).lower()
        
        if role in self.role_content:
            content = self.role_content[role]
            
            st.markdown(f"### {role.title()} AI Training")
            st.info(content['description'])
            
            # Show learning path
            st.subheader("🎯 Recommended Learning Path")
            for i, course in enumerate(content['courses'], 1):
                with st.expander(f"Module {i}: {course}"):
                    st.write(f"**Module {i}:** {course}")
                    st.write("**Estimated Time:** 2-3 hours")
                    st.write("**Skill Level:** Intermediate")
                    if st.button(f"Start Module {i}", key=f"start_{role}_{i}"):
                        st.success(f"Started Module {i}: {course}")
            
            # Skill assessment
            st.subheader("📊 Your Skills")
            for skill in content['skills']:
                st.progress(random.random())
                st.write(f"- {skill}")
        else:
            st.info("More professions being added soon!")
    
    def show_training(self):
        """Show role-specific training"""
        st.markdown("<h2 class='sub-header'>🎓 Role-Specific Training</h2>", unsafe_allow_html=True)
        
        role = st.selectbox(
            "Select your profession for specialized training:",
            ["Healthcare", "Finance", "Marketing", "Legal", "Technology"]
        ).lower()
        
        if role in self.role_content:
            content = self.role_content[role]
            
            st.markdown(f"### {role.title()} - Recommended Training")
            
            # Show interactive training modules
            for i, course in enumerate(content['courses'], 1):
                with st.container():
                    st.markdown(f"**Module {i}: {course}**")
                    col1, col2, col3 = st.columns([2, 1, 1])
                    with col2:
                        st.button(f"📖 Learn", key=f"learn_{role}_{i}")
                    with col3:
                        st.button(f"📝 Quiz", key=f"quiz_{role}_{i}")
                    st.markdown("---")
    
    def show_skill_assessment(self):
        """Show skill assessment"""
        st.markdown("<h2 class='sub-header'>📊 Skill Assessment</h2>", unsafe_allow_html=True)
        
        role = st.selectbox("Select your profession:", ["Healthcare", "Finance", "Marketing", "Legal", "Technology"])
        
        st.subheader("Current Skill Level")
        
        # Simulated skill levels
        skills = {
            "Data Analysis": 0.6,
            "AI Understanding": 0.4,
            "Industry Knowledge": 0.7,
            "Practical Application": 0.3
        }
        
        for skill, level in skills.items():
            st.write(f"**{skill}**")
            st.progress(level)
            st.write(f"Level: {int(level * 100)}%")
            st.markdown("---")
        
        if st.button("Take Comprehensive Assessment"):
            st.info("Starting comprehensive skill assessment...")
            st.progress(0)
            for i in range(5):
                st.write(f"Question {i+1}: Sample question about your field")
                st.radio("Select answer:", ["A", "B", "C", "D"], key=f"q_{i}")
            if st.button("Submit Assessment"):
                st.success("Assessment complete! Your results will be sent to your email.")
