import streamlit as st

st.set_page_config('Study app', page_icon='📚', layout='wide')

# Header principal
st.markdown("""
<div style='background: linear-gradient(90deg, #4F46E5 0%, #7C3AED 100%); 
            padding: 2rem; border-radius: 10px; margin-bottom: 2rem;'>
    <h1 style='color: white; text-align: center; margin: 0;'>📚 Study Tracker 100 Days</h1>
    <p style='color: white; text-align: center; margin: 0.5rem 0 0 0; opacity: 0.9;'>
        Improving as a Data Analyst | Physics Review | Master's Preparation
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown('This app is a tool to help me track my study sessions during the 100 Days of Learning challenge.')

st.info("""
        👋 Hello! Welcome to your Study Tracker.
        
        This is your space to document your learning during the next 100 days.
        From data analysis to physics, here you can keep a complete record of your progress.
        
        **To get started:**
        1. Click on "➕ New Session" in the sidebar
        2. Register your first study session
        3. Start your challenge!
        """)

st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 2rem; border-radius: 10px; text-align: center; margin-top: 2rem;'>
            <h2 style='color: white;'>🏆 Let's go! Complete this challenge!</h2>
            <p style='color: white; font-size: 1.2rem;'>
                Each day counts. Each session brings you closer to your goal.
            </p>
        </div>
        """, unsafe_allow_html=True)