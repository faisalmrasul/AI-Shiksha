import streamlit as st

class BusinessModule:
    def __init__(self):
        self.tools = {
            "Customer Service Automation": {
                "description": "AI chatbots and automated customer support",
                "benefits": "24/7 customer support, reduced response time, cost savings",
                "difficulty": "Easy"
            },
            "AI-Assisted Marketing": {
                "description": "Content generation, email marketing, and social media management",
                "benefits": "Increased engagement, consistent content, better targeting",
                "difficulty": "Moderate"
            },
            "Inventory Management": {
                "description": "AI-powered demand forecasting and stock optimization",
                "benefits": "Reduced waste, optimal stock levels, better cash flow",
                "difficulty": "Moderate"
            },
            "Business Decision Support": {
                "description": "Data analytics and predictive insights for strategic decisions",
                "benefits": "Data-driven decisions, risk reduction, competitive advantage",
                "difficulty": "Advanced"
            }
        }
        
    def show_learning_path(self):
        """Display business learning path"""
        st.markdown("<h2 class='sub-header'>🏢 Small Business AI Training</h2>", unsafe_allow_html=True)
        
        st.info("""
        **AI for Small Businesses**: Transform your business with AI tools
        - 🤖 Automate customer service
        - 📱 AI-powered marketing
        - 📊 Optimize inventory
        - 💡 Data-driven decision making
        """)
        
        # Business assessment
        st.subheader("📊 Business AI Readiness Assessment")
        
        col1, col2 = st.columns(2)
        with col1:
            business_size = st.selectbox("Business Size", ["Solo", "2-10 employees", "11-50 employees"])
            business_type = st.text_input("Business Industry")
        with col2:
            current_tech = st.multiselect("Current Technology Use", ["Website", "Social Media", "CRM", "Accounting Software", "None"])
            primary_goal = st.selectbox("Primary Business Goal", ["Growth", "Efficiency", "Customer Satisfaction", "Cost Reduction"])
        
        if st.button("Get AI Recommendations"):
            st.success("Personalized AI recommendations generated!")
            st.markdown("""
            Based on your responses, we recommend starting with:
            1. **Customer Service Automation** - Set up an AI chatbot for your website
            2. **AI-Assisted Marketing** - Use AI tools for social media content
            3. **Basic Analytics** - Track key business metrics with AI insights
            """)
    
    def show_tools(self):
        """Show business tools"""
        st.markdown("<h2 class='sub-header'>🛠️ AI Business Tools</h2>", unsafe_allow_html=True)
        
        for tool_name, tool_info in self.tools.items():
            with st.expander(f"🤖 {tool_name}"):
                st.write(tool_info['description'])
                st.write(f"**Benefits:** {tool_info['benefits']}")
                st.write(f"**Difficulty:** {tool_info['difficulty']}")
                if st.button(f"Learn More about {tool_name}", key=f"learn_{tool_name}"):
                    st.success(f"Starting {tool_name} training module...")
                st.markdown("---")
    
    def show_automation(self):
        """Show automation tools"""
        st.markdown("<h2 class='sub-header'>⚡ Business Automation</h2>", unsafe_allow_html=True)
        
        automation_tools = {
            "Email Marketing Automation": {
                "description": "Automated email campaigns with AI personalization",
                "benefits": "Increase engagement, save time, improve conversions",
                "complexity": "Medium"
            },
            "Social Media Automation": {
                "description": "Schedule and optimize social media posts with AI",
                "benefits": "Consistent posting, better timing, content optimization",
                "complexity": "Low"
            },
            "Lead Generation Automation": {
                "description": "AI-powered lead scoring and nurturing",
                "benefits": "Better leads, improved conversion rates",
                "complexity": "Medium"
            },
            "Workflow Automation": {
                "description": "Automate repetitive tasks with AI agents",
                "benefits": "Increased productivity, reduced errors",
                "complexity": "High"
            }
        }
        
        for tool_name, tool_info in automation_tools.items():
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.markdown(f"**{tool_name}**")
                    st.write(tool_info['description'])
                with col2:
                    st.write(f"Difficulty: {tool_info['complexity']}")
                with col3:
                    if st.button("Try Automation", key=f"auto_{tool_name}"):
                        st.success(f"Setting up {tool_name}...")
                st.markdown("---")
