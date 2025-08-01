import os
import streamlit as st
import requests
import pandas as pd
#import plotly.express as px
#import plotly.graph_objects as go
from datetime import datetime
import json

# Page config
st.set_page_config(
    page_title="Smart Routing Engine Dashboard",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configure Gemini API
api_key = st.secrets["mykey"]
genai.configure(api_key=api_key)

# API Configuration - Get from Streamlit secrets
#try:
    #API_BASE_URL = st.secrets["API_BASE_URL"]
#except:
    #API_BASE_URL = "https://your-api-url.loca.lt"
    #st.error("⚠️ API_BASE_URL not found in secrets. Please configure in Streamlit settings.")

def main():
    st.title("🤖 Smart Routing Engine Dashboard")
    
    # API Status indicator
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("**Real-time chat routing and ALPS scoring system**")
    with col2:
        check_api_status()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    st.sidebar.markdown(f"**API:** `{API_BASE_URL}`")
    
    page = st.sidebar.selectbox("Choose a page", [
        "🏠 Overview", 
        "🧪 Test Routing", 
        "👥 Agent Status", 
        "📈 Analytics",
        "⚙️ API Test"
    ])
    
    # Route to pages
    if page == "🏠 Overview":
        show_overview()
    elif page == "🧪 Test Routing":
        show_test_routing()
    elif page == "👥 Agent Status":
        show_agent_status()
    elif page == "📈 Analytics":
        show_analytics()
    elif page == "⚙️ API Test":
        show_api_test()

def check_api_status():
    """Check API status and show indicator"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            st.success("🟢 API Online")
        else:
            st.error("🔴 API Error")
    except:
        st.error("🔴 API Offline")

def show_overview():
    st.header("📊 System Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📬 Messages Today", "127", "12")
    with col2:
        st.metric("⚡ Avg Response Time", "2.3 min", "-0.5 min")
    with col3:
        st.metric("🎯 ALPS Avg Score", "74.2", "3.1")
    with col4:
        st.metric("🚨 SLA Breaches", "3", "-2")
    
    # Recent activity
    st.subheader("🔴 Live Activity Feed")
    
    activity_data = [
        {"time": "14:32", "message": "New sales lead → Sarah Chen (ALPS: 85.2)", "status": "✅"},
        {"time": "14:30", "message": "Urgent support → John Smith (Escalated)", "status": "⚠️"},
        {"time": "14:28", "message": "Sales lead → Mike Johnson (ALPS: 72.1)", "status": "✅"},
        {"time": "14:25", "message": "SLA breach → Chat reassigned", "status": "❌"},
    ]
    
    for activity in activity_data:
        st.write(f"{activity['status']} **{activity['time']}** - {activity['message']}")

def show_test_routing():
    st.header("🧪 Interactive Routing Test")
    
    # Predefined scenarios
    scenarios = {
        "🔥 Urgent Sales Lead": "Hi, I need a room near TARUC ASAP! Moving in next week, budget around RM800-1200",
        "😠 Angry Support": "This is ridiculous! My air conditioning has been broken for 3 days and nobody is fixing it!",
        "💼 Premium Lead": "I need a luxury studio apartment near KLCC, budget up to RM3000, flexible timing",
        "❓ General Inquiry": "Hello, can you tell me more about your room rental services?",
        "🏠 Maintenance": "Hi, the water heater in my room is not working properly. Can someone check it?",
        "💰 Budget Query": "What are your cheapest rooms available near KL? I'm a student with limited budget"
    }
    
    # Input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        scenario = st.selectbox("Choose test scenario:", list(scenarios.keys()))
        message = st.text_area("Message:", value=scenarios[scenario], height=120)
        
    with col2:
        channel = st.selectbox("Channel:", ["whatsapp", "web", "facebook", "telegram"])
        is_repeat = st.checkbox("Repeat Customer")
        st.write(f"**Message Length:** {len(message)} chars")
    
    # Test button
    if st.button("🚀 Test Routing", type="primary"):
        with st.spinner("🤖 Processing message with Gemini AI..."):
            result = route_test_message(message, channel, is_repeat)
            
            if result:
                display_routing_result(result)

def show_agent_status():
    st.header("👥 Agent Status & Load Balancing")
    
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/agents/status", timeout=10)
        if response.status_code == 200:
            agents_data = response.json().get("agents", {})
            
            # Sales team
            if "sales" in agents_data:
                st.subheader("💼 Sales Team")
                for agent in agents_data["sales"]:
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        load_pct = (agent["active_chats"] / agent["max_chats"]) * 100
                        if load_pct >= 80:
                            status_icon = "🔴"
                            status = "Overloaded"
                        elif load_pct >= 60:
                            status_icon = "🟡"
                            status = "Busy"
                        else:
                            status_icon = "🟢"
                            status = "Available"
                        
                        st.write(f"{status_icon} **{agent['name']}**")
                        st.progress(load_pct / 100, text=f"{status} ({load_pct:.0f}%)")
                    
                    with col2:
                        st.metric("Chats", f"{agent['active_chats']}/{agent['max_chats']}")
                    
                    with col3:
                        st.metric("Performance", f"{agent['performance']}%")
                    
                    with col4:
                        if load_pct >= 80:
                            st.error("Overloaded")
                        elif load_pct >= 60:
                            st.warning("Busy")
                        else:
                            st.success("Ready")
                
                st.divider()
            
            # Support team
            if "support" in agents_data:
                st.subheader("🛠️ Support Team")
                for agent in agents_data["support"]:
                    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
                    
                    with col1:
                        load_pct = (agent["active_chats"] / agent["max_chats"]) * 100
                        if load_pct >= 80:
                            status_icon = "🔴"
                            status = "Overloaded"
                        elif load_pct >= 60:
                            status_icon = "🟡"
                            status = "Busy"
                        else:
                            status_icon = "🟢"
                            status = "Available"
                        
                        st.write(f"{status_icon} **{agent['name']}**")
                        st.progress(load_pct / 100, text=f"{status} ({load_pct:.0f}%)")
                    
                    with col2:
                        st.metric("Chats", f"{agent['active_chats']}/{agent['max_chats']}")
                    
                    with col3:
                        st.metric("Performance", f"{agent['performance']}%")
                    
                    with col4:
                        if load_pct >= 80:
                            st.error("Overloaded")
                        elif load_pct >= 60:
                            st.warning("Busy")
                        else:
                            st.success("Ready")
        else:
            st.error(f"Failed to fetch agent status: {response.status_code}")
    
    except Exception as e:
        st.error(f"Error connecting to API: {e}")

def show_analytics():
    st.header("📈 Analytics & Insights")
    
    # Date range selector
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", value=pd.Timestamp.now() - pd.Timedelta(days=7))
    with col2:
        end_date = st.date_input("End Date", value=pd.Timestamp.now())
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Intent distribution
        intent_data = pd.DataFrame({
            'Intent': ['Sales', 'Support'],
            'Count': [78, 49]
        })
        fig = px.pie(intent_data, values='Count', names='Intent', 
                    title="Message Intent Distribution",
                    color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
        
        # Priority distribution
        priority_data = pd.DataFrame({
            'Priority': ['High', 'Medium', 'Low'],
            'Count': [23, 45, 32]
        })
        fig = px.bar(priority_data, x='Priority', y='Count',
                    title="Lead Priority Distribution",
                    color='Priority',
                    color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # ALPS score distribution
        alps_scores = [85.2, 72.1, 91.3, 68.7, 79.4, 83.1, 76.8, 88.9, 65.3, 92.1]
        fig = px.histogram(x=alps_scores, nbins=10, 
                          title="ALPS Score Distribution",
                          labels={'x': 'ALPS Score', 'y': 'Frequency'})
        fig.update_traces(marker_color='lightblue')
        st.plotly_chart(fig, use_container_width=True)
        
        # Daily message volume
        dates = pd.date_range(start=start_date, end=end_date)
        daily_data = pd.DataFrame({
            'Date': dates,
            'Messages': [45, 52, 38, 63, 71, 44, 58, 61][:len(dates)]
        })
        fig = px.line(daily_data, x='Date', y='Messages',
                     title="Daily Message Volume",
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)

def show_api_test():
    st.header("⚙️ API Test & Configuration")
    
    st.write(f"**Current API URL:** `{API_BASE_URL}`")
    
    # Test all endpoints
    if st.button("🧪 Test All Endpoints"):
        test_all_endpoints()
    
    st.subheader("📋 API Endpoints")
    endpoints = {
        "Health Check": f"{API_BASE_URL}/health",
        "Route Message": f"{API_BASE_URL}/api/v1/route",
        "Agent Status": f"{API_BASE_URL}/api/v1/agents/status",
        "Chatwoot Webhook": f"{API_BASE_URL}/api/v1/webhook/chatwoot",
        "API Documentation": f"{API_BASE_URL}/docs"
    }
    
    for name, url in endpoints.items():
        st.write(f"**{name}:** `{url}`")
    
    st.subheader("🔗 Integration URLs")
    st.code(f"""
Chatwoot Webhook URL:
{API_BASE_URL}/api/v1/webhook/chatwoot

API Documentation:
{API_BASE_URL}/docs
    """)

def test_all_endpoints():
    """Test all API endpoints"""
    st.write("🧪 Testing API endpoints...")
    
    endpoints = [
        ("Health", "GET", "/health"),
        ("Agent Status", "GET", "/api/v1/agents/status"),
    ]
    
    for name, method, path in endpoints:
        try:
            url = f"{API_BASE_URL}{path}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                st.success(f"✅ {name}: OK")
            else:
                st.error(f"❌ {name}: {response.status_code}")
        except Exception as e:
            st.error(f"❌ {name}: Connection failed")

def route_test_message(message: str, channel: str, is_repeat: bool = False):
    """Route a test message through the API"""
    try:
        payload = {
            "chat_id": f"test_{datetime.now().strftime('%H%M%S')}",
            "message": message,
            "channel": channel,
            "is_repeat_customer": is_repeat
        }
        
        response = requests.post(f"{API_BASE_URL}/api/v1/route", json=payload, timeout=15)
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: {response.status_code}")
            st.code(response.text)
            return None
            
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def display_routing_result(result):
    """Display routing result in a beautiful format"""
    st.success("✅ Message Processed Successfully!")
    
    # Classification results
    st.subheader("🧠 AI Classification")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        intent = result.get('intent', 'N/A').title()
        st.metric("Intent", intent)
        
    with col2:
        sentiment = result.get('sentiment', 'N/A').title()
        sentiment_color = {"Positive": "🟢", "Negative": "🔴", "Neutral": "🟡"}.get(sentiment, "⚪")
        st.metric("Sentiment", f"{sentiment_color} {sentiment}")
        
    with col3:
        urgency = result.get('urgency', 'N/A').title()
        urgency_color = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(urgency, "⚪")
        st.metric("Urgency", f"{urgency_color} {urgency}")
        
    with col4:
        confidence = result.get('confidence', 0)
        st.metric("Confidence", f"{confidence:.1%}")
    
    # ALPS Score (if sales)
    if result.get('intent') == 'sales' and 'alps_score' in result:
        st.subheader("🏆 ALPS Scoring Analysis")
        
        alps_score = result['alps_score']
        priority = result.get('priority_level', 'medium')
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            # ALPS score gauge
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = alps_score,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "ALPS Score"},
                gauge = {
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "yellow"},
                        {'range': [75, 100], 'color': "green"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 90
                    }
                }
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Priority indicator
            if alps_score >= 80:
                st.error("🔥 HIGH PRIORITY LEAD")
                st.write("Route to top sales agent immediately!")
            elif alps_score >= 60:
                st.warning("⚡ MEDIUM PRIORITY LEAD")
                st.write("Route to available sales agent")
            else:
                st.info("📝 STANDARD LEAD")
                st.write("Route to general sales queue")
            
            # Score breakdown
            if 'score_breakdown' in result:
                st.write("**Score Breakdown:**")
                breakdown = result['score_breakdown']
                for criteria, score in breakdown.items():
                    criteria_name = criteria.replace('_', ' ').title()
                    st.write(f"• {criteria_name}: {score:.2f}")
    
    # Routing Decision
    st.subheader("🎯 Routing Decision")
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"**👤 Assigned Agent:** {result.get('assigned_agent', 'N/A')}")
        
    with col2:
        if result.get('escalated'):
            st.warning("⚠️ **Escalated to Manager**")
        else:
            st.success("✅ **Standard Routing**")
    
    st.write(f"**📝 Routing Reason:** {result.get('routing_reason', 'N/A')}")
    
    # Raw JSON (expandable)
    with st.expander("🔍 View Raw Response"):
        st.json(result)

if __name__ == "__main__":
    main()






