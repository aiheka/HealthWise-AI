import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

from src.analyzer.wellness_score import calculate_wellness_score, get_wellness_category
from src.recommendations.recommendation_engine import generate_recommendations
from src.recommendations.daily_plan import generate_daily_plan
from src.rag.simple_search import search_health_docs, get_system_stats

# Page config
st.set_page_config(
    page_title="HealthWise AI",
    page_icon="💚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .sdg-badge {
        background-color: #4CAF50;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 0.25rem;
        display: inline-block;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'health_data' not in st.session_state:
    st.session_state.health_data = []
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Sidebar
with st.sidebar:
    st.markdown("### 💚 HealthWise AI")
    st.markdown("**AI-Powered Preventive Healthcare Platform**")
    st.markdown("*Promoting Health & Well-being Through AI*")
    
    st.markdown("---")
    
    st.markdown("### 🎯 Features")
    st.markdown("""
    ✅ Daily Health Check-In
    ✅ Wellness Score Analysis
    ✅ Personalized Recommendations
    ✅ Weekly Health Insights
    ✅ Trend Analysis
    ✅ AI Health Assistant
    ✅ Smart Health Alerts
    """)
    
    st.markdown("---")
    
    st.markdown('<div class="sdg-badge">🌍 SDG 3: Good Health & Well-being</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("### 🤖 Powered By")
    st.markdown("- IBM Watson AI")
    st.markdown("- Streamlit")
    st.markdown("- Python 3.13")
    
    st.markdown("---")
    
    st.markdown("### 👨‍💻 Developed By")
    st.markdown("*Aiheka Gadde*")
 

# Main header
st.markdown('<div class="main-header">💚 HealthWise AI</div>', unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #666;'>Your Personalized Preventive Health Companion</p>", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🏠 Daily Check-In",
    "📊 Health Dashboard", 
    "📈 Weekly Insights",
    "🧠 AI Assistant",
    "🔮 Future Scope",
    "ℹ️ About & Responsible AI"
])

# TAB 1: Daily Check-In
with tab1:
    st.header("📝 Daily Health Check-In")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sleep = st.number_input("Sleep Hours", 0.0, 12.0, 7.0, 0.5, help="How many hours did you sleep?")
        water = st.number_input("Water Intake (Liters)", 0.0, 5.0, 2.0, 0.1, help="How much water did you drink?")
        exercise = st.number_input("Exercise Minutes", 0, 120, 30, 5, help="How many minutes did you exercise?")
    
    with col2:
        energy = st.slider("Energy Level", 1, 10, 5, help="How energetic do you feel?")
        stress = st.slider("Stress Level", 1, 10, 5, help="How stressed do you feel?")
        mood = st.select_slider("Mood", ["😔 Low", "😐 Okay", "🙂 Good", "😊 Great"], value="🙂 Good")
    
    if st.button("🚀 Analyze My Health", type="primary", use_container_width=True):
        score = calculate_wellness_score(sleep, water, exercise, energy, stress)
        category = get_wellness_category(score)
        insights, action = generate_recommendations(sleep, water, exercise, energy, stress)
        daily_plan = generate_daily_plan(sleep, stress, exercise, energy)
        
        # Store data
        st.session_state.health_data.append({
            'date': datetime.now(),
            'sleep': sleep,
            'water': water,
            'exercise': exercise,
            'energy': energy,
            'stress': stress,
            'score': score
        })
        
        st.markdown("---")
        
        # Results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Wellness Score", f"{score}/100", help="Your overall health score")
        
        with col2:
            if category == "Excellent":
                st.success(f"Category: {category}")
            elif category == "Good":
                st.info(f"Category: {category}")
            elif category == "Needs Attention":
                st.warning(f"Category: {category}")
            else:
                st.error(f"Category: {category}")
        
        with col3:
            if score >= 85:
                st.metric("Status", "🌟 Excellent")
            elif score >= 70:
                st.metric("Status", "✅ Good")
            elif score >= 50:
                st.metric("Status", "⚠️ Attention")
            else:
                st.metric("Status", "🚨 Alert")
        
        # Smart Health Alert
        if score < 55:
            st.error("""
            ### 🚨 Smart Health Alert
            Your wellness score is low. Immediate actions recommended:
            - Prioritize 7-8 hours of sleep tonight
            - Drink at least 2 liters of water today
            - Take a 20-minute walk
            - Practice 5 minutes of deep breathing
            """)
        
        # Insights
        st.subheader("📊 Today's Insights")
        for insight in insights:
            st.write(f"• {insight}")
        
        # Priority Action
        st.subheader("🎯 Most Impactful Action")
        st.info(action)
        
        # Daily Plan
        st.subheader("📋 Your Daily Action Plan")
        st.success(daily_plan)

# TAB 2: Health Dashboard
with tab2:
    st.header("📊 Health Dashboard")
    
    if len(st.session_state.health_data) > 0:
        df = pd.DataFrame(st.session_state.health_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            avg_score = df['score'].mean()
            st.metric("Avg Wellness Score", f"{avg_score:.1f}")
        
        with col2:
            avg_sleep = df['sleep'].mean()
            st.metric("Avg Sleep", f"{avg_sleep:.1f}h")
        
        with col3:
            avg_water = df['water'].mean()
            st.metric("Avg Hydration", f"{avg_water:.1f}L")
        
        with col4:
            avg_exercise = df['exercise'].mean()
            st.metric("Avg Exercise", f"{avg_exercise:.0f}min")
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='date', y='score', title='Wellness Score Trend',
                         labels={'score': 'Wellness Score', 'date': 'Date'})
            fig.update_traces(line_color='#1f77b4', line_width=3)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.bar(df, x='date', y='sleep', title='Sleep Pattern',
                        labels={'sleep': 'Hours', 'date': 'Date'})
            fig.update_traces(marker_color='#2ca02c')
            st.plotly_chart(fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.line(df, x='date', y=['energy', 'stress'], title='Energy vs Stress',
                         labels={'value': 'Level', 'date': 'Date'})
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.scatter(df, x='sleep', y='score', size='exercise', color='stress',
                           title='Sleep vs Wellness Score',
                           labels={'sleep': 'Sleep Hours', 'score': 'Wellness Score'})
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("📝 Complete your first daily check-in to see your health dashboard!")

# TAB 3: Weekly Insights
with tab3:
    st.header("📈 Weekly Health Insights")
    
    if len(st.session_state.health_data) >= 3:
        df = pd.DataFrame(st.session_state.health_data)
        
        st.subheader("🎯 Key Findings")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Performance Metrics")
            
            best_score = df['score'].max()
            worst_score = df['score'].min()
            trend = "improving" if df['score'].iloc[-1] > df['score'].iloc[0] else "declining"
            
            st.write(f"**Best Score:** {best_score:.0f}/100")
            st.write(f"**Lowest Score:** {worst_score:.0f}/100")
            st.write(f"**Trend:** {trend.title()}")
            
            if df['sleep'].mean() < 7:
                st.warning("⚠️ Sleep deficit detected")
            if df['water'].mean() < 2:
                st.warning("⚠️ Hydration below recommended")
            if df['exercise'].mean() < 30:
                st.warning("⚠️ Exercise below target")
        
        with col2:
            st.markdown("### 💡 Personalized Recommendations")
            
            if df['sleep'].mean() < 7:
                st.write("🌙 **Sleep:** Aim for 7-8 hours nightly")
            if df['water'].mean() < 2.5:
                st.write("💧 **Hydration:** Increase water intake to 2.5L")
            if df['exercise'].mean() < 45:
                st.write("🏃 **Exercise:** Target 45 minutes daily")
            if df['stress'].mean() > 6:
                st.write("🧘 **Stress:** Practice daily relaxation")
            
            st.success("Keep tracking to unlock more insights!")
        
        # Correlation Analysis
        st.subheader("🔗 Health Correlations")
        
        corr_data = df[['sleep', 'water', 'exercise', 'energy', 'stress', 'score']].corr()
        
        fig = px.imshow(corr_data, 
                       labels=dict(color="Correlation"),
                       x=corr_data.columns,
                       y=corr_data.columns,
                       color_continuous_scale='RdBu',
                       title="How Your Health Metrics Relate")
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.info("📊 Track your health for at least 3 days to unlock weekly insights!")

# TAB 4: AI Assistant
with tab4:
    st.header("🧠 AI Health Assistant")
    
    stats = get_system_stats()
    
    if stats.get('status') == 'active':
        st.success(f"✅ AI Assistant Active | {stats.get('documents', 0)} Health Topics Available")
    
    st.markdown("Ask me anything about:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("- 😴 Sleep & Rest")
        st.markdown("- 💧 Hydration")
    with col2:
        st.markdown("- 🥗 Nutrition & Diet")
        st.markdown("- 🏃 Exercise & Fitness")
    with col3:
        st.markdown("- 🧘 Stress Management")
        st.markdown("- 💪 General Wellness")
    
    st.markdown("---")
    
    user_question = st.text_input(
        "Ask your health question:",
        placeholder="e.g., How much sleep do I need? What are benefits of exercise?"
    )
    
    col1, col2 = st.columns([1, 4])
    with col1:
        ask_button = st.button("🔍 Ask AI", type="primary")
    with col2:
        if st.button("🗑️ Clear History"):
            st.session_state.conversation_history = []
            st.rerun()
    
    if ask_button and user_question:
        with st.spinner("🤔 Analyzing your question..."):
            response = search_health_docs(user_question)
        
        st.session_state.conversation_history.append({
            'question': user_question,
            'answer': response
        })
        
        st.markdown("---")
        st.markdown(response)
    
    # Conversation History
    if st.session_state.conversation_history:
        st.markdown("---")
        st.subheader("📜 Recent Conversations")
        
        for i, conv in enumerate(reversed(st.session_state.conversation_history[-3:]), 1):
            with st.expander(f"Q{len(st.session_state.conversation_history) - i + 1}: {conv['question'][:50]}..."):
                st.markdown(f"**Q:** {conv['question']}")
                st.markdown(f"**A:** {conv['answer'][:300]}...")

# TAB 5: Future Scope
with tab5:
    st.header("🔮 Future Enhancements")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📱 Smartwatch Integration")
        st.markdown("""
        **Planned Features:**
        - Real-time heart rate monitoring
        - Automatic sleep tracking
        - Step count integration
        - Calorie burn tracking
        - Activity detection
        - Smart notifications
        
        **Compatible Devices:**
        - Apple Watch
        - Fitbit
        - Samsung Galaxy Watch
        - Garmin devices
        """)
        
        st.subheader("🔔 Smart Health Alerts")
        st.markdown("""
        - Hydration reminders
        - Movement prompts
        - Sleep schedule notifications
        - Medication reminders
        - Stress level warnings
        - Achievement celebrations
        """)
    
    with col2:
        st.subheader("🎯 Wellness Prediction")
        st.markdown("""
        **AI-Powered Predictions:**
        - 7-day wellness forecast
        - Risk assessment
        - Personalized goal setting
        - Habit formation tracking
        - Health trend prediction
        - Preventive recommendations
        
        **Machine Learning Models:**
        - Time series forecasting
        - Anomaly detection
        - Pattern recognition
        - Behavioral analysis
        """)
        
        st.subheader("🌐 Community Features")
        st.markdown("""
        - Health challenges
        - Peer support groups
        - Expert consultations
        - Progress sharing
        - Leaderboards
        - Social motivation
        """)
    
    st.markdown("---")
    st.info("💡 These features will be implemented in future versions based on user feedback and technological advancements.")

# TAB 6: About & Responsible AI
with tab6:
    st.header("ℹ️ About HealthWise AI")
    
    st.markdown("""
    ### 🎓 Internship Project
    
    This project is developed as part of the **1M1B + IBM SkillsBuild + AICTE AI for Sustainability Internship Program**.
    
    **Objective:** Leverage AI technology to promote preventive healthcare and contribute to UN Sustainable Development Goal 3: Good Health and Well-being.
    """)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌍 SDG 3 Alignment")
        st.markdown("""
        **Target 3.4:** Reduce premature mortality from non-communicable diseases through prevention and treatment.
        
        **Target 3.d:** Strengthen capacity for early warning, risk reduction, and management of health risks.
        
        **How HealthWise AI Contributes:**
        - Promotes preventive healthcare
        - Encourages healthy lifestyle habits
        - Provides accessible health information
        - Enables early detection of health issues
        - Supports informed health decisions
        """)
    
    with col2:
        st.subheader("🤖 IBM BOB Contribution")
        st.markdown("""
        **IBM Build on Basics (BOB) Framework:**
        
        This project demonstrates:
        - **AI Ethics:** Responsible AI implementation
        - **Data Privacy:** No personal data storage
        - **Accessibility:** Free and open access
        - **Transparency:** Clear AI explanations
        - **Inclusivity:** Designed for all users
        
        **Technologies Used:**
        - Python 3.13
        - Streamlit Framework
        - Scikit-learn (TF-IDF)
        - Plotly Visualization
        """)
    
    st.markdown("---")
    
    st.subheader("🛡️ Responsible AI Principles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Transparency**
        - Clear AI decision-making
        - Explainable recommendations
        - Source attribution
        - Method disclosure
        """)
    
    with col2:
        st.markdown("""
        **Privacy**
        - No data collection
        - Local processing only
        - No third-party sharing
        - User control
        """)
    
    with col3:
        st.markdown("""
        **Safety**
        - Health disclaimers
        - Professional advice encouraged
        - Evidence-based information
        - Risk warnings
        """)
    
    st.markdown("---")
    
    st.subheader("⚠️ Important Disclaimers")
    
    st.warning("""
    **Medical Disclaimer:**
    
    HealthWise AI provides general health information for educational purposes only. It is NOT a substitute for professional medical advice, diagnosis, or treatment.
    
    - Always consult qualified healthcare providers for medical concerns
    - Do not disregard professional medical advice based on this app
    - In case of emergency, contact emergency services immediately
    - This app does not diagnose, treat, or prevent any disease
    """)
    
    st.info("""
    **Data Privacy:**
    
    - All data is stored locally in your browser session
    - No personal information is collected or transmitted
    - No user accounts or authentication required
    - Data is cleared when you close the browser
    """)
    
    st.markdown("---")
    
    st.subheader("👨‍💻 Developer Information")
    
    st.markdown("""
    **Developed By:** Aiheka Gadde
    
    
    **Program:** AI for Sustainability
    
    **Year:** 2026
    
    **Contact:** aihekagadde@gmail.com

    
    **GitHub:** https://github.com/aiheka
    """)
    
    st.markdown("---")
    
    st.markdown("""
    <div style='text-align: center; padding: 2rem; background-color: #1e1e1e; border-radius: 0.5rem;'>
        <h3>🌟 Thank You for Using HealthWise AI!</h3>
        <p>Together, we can build a healthier future through AI and preventive care.</p>
        <p><strong>Stay Healthy, Stay Happy! 💚</strong></p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>💚 HealthWise AI</p>
    <p>🌍 Contributing to SDG 3: Good Health and Well-being</p>
</div>
""", unsafe_allow_html=True)

# Made with Bob
