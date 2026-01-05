import streamlit as st
import requests
import plotly.graph_objects as go

st.set_page_config(
    page_title="BurnoutGuard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_URL = "http://127.0.0.1:8000"

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Fraunces:opsz,wght@9..144,400;9..144,500;9..144,600;9..144,700&display=swap');
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: #F5F5F0;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #5A7A63 0%, #4A6853 100%);
    }
    
    section[data-testid="stSidebar"] * {
        color: white !important;
    }
    
    /* TEXT AREA FIX - Light background, dark text */
    .stTextArea textarea {
        background: #FFFFFF !important;
        color: #2D3A35 !important;
        border: 2px solid #7C9885 !important;
        border-radius: 12px !important;
        font-family: 'DM Sans', sans-serif !important;
        font-size: 0.95rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #5A7A63 !important;
        box-shadow: 0 0 0 3px rgba(124, 152, 133, 0.15) !important;
    }
    
    .stTextArea textarea::placeholder {
        color: #999 !important;
        opacity: 1 !important;
    }
    
    /* SLIDER FIX - Green theme */
    .stSlider > div > div > div > div {
        background: linear-gradient(to right, #7C9885, #7C9885) !important;
    }
    
    .stSlider [role="slider"] {
        background: #5A7A63 !important;
        border: 2px solid white !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.2) !important;
    }
    
    .stSlider [data-testid="stThumbValue"] {
        color: #5A7A63 !important;
        font-weight: 600 !important;
    }
    
    /* SLIDER LABEL FIX - Visible dark text */
    .stSlider label {
        color: #2D3A35 !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 500 !important;
    }
    
    .welcome-banner {
        background: linear-gradient(135deg, #7C9885 0%, #5A7A63 100%);
        border-radius: 20px;
        padding: 2rem 2.5rem;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 30px rgba(124, 152, 133, 0.3);
    }
    
    .welcome-title {
        font-family: 'Fraunces', serif;
        font-size: 2rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        color: white;
    }
    
    .welcome-subtitle {
        font-family: 'DM Sans', sans-serif;
        font-size: 1rem;
        opacity: 0.9;
        color: white;
    }
    
    .custom-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-family: 'Fraunces', serif;
        font-size: 1.15rem;
        font-weight: 500;
        color: #2D3A35;
        margin-bottom: 1rem;
    }
    
    .score-box {
        text-align: center;
        padding: 1rem;
    }
    
    .score-number {
        font-family: 'Fraunces', serif;
        font-size: 3.5rem;
        font-weight: 600;
        line-height: 1;
    }
    
    .score-low { color: #7BAE7F; }
    .score-moderate { color: #E8C87A; }
    .score-high { color: #D98B8B; }
    
    .score-label {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-top: 0.5rem;
    }
    
    .risk-badge {
        display: inline-block;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .risk-low { background: #E8F5E9; color: #4A7A4E; }
    .risk-moderate { background: #FFF8E1; color: #8A7030; }
    .risk-high { background: #FFEBEE; color: #A04545; }
    
    .emotion-item {
        display: flex;
        align-items: center;
        margin: 0.6rem 0;
        gap: 0.75rem;
    }
    
    .emotion-name {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        color: #555;
        width: 70px;
    }
    
    .emotion-bar-container {
        flex: 1;
        height: 8px;
        background: #EAEAEA;
        border-radius: 4px;
        overflow: hidden;
    }
    
    .emotion-bar {
        height: 100%;
        background: linear-gradient(90deg, #7C9885, #A8C4B0);
        border-radius: 4px;
    }
    
    .emotion-percent {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 600;
        color: #333;
        width: 45px;
        text-align: right;
    }
    
    .insight-box {
        background: #F0F4F1;
        border-radius: 12px;
        padding: 1.25rem;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.95rem;
        line-height: 1.6;
        color: #333;
    }
    
    .rec-item {
        background: #FAFAFA;
        border-left: 3px solid #7C9885;
        padding: 0.9rem 1.1rem;
        margin: 0.6rem 0;
        border-radius: 0 10px 10px 0;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        color: #333;
    }
    
    .stat-box {
        background: white;
        border-radius: 16px;
        padding: 1.5rem 1rem;
        text-align: center;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    }
    
    .stat-number {
        font-family: 'Fraunces', serif;
        font-size: 2.5rem;
        font-weight: 600;
        color: #5A7A63;
    }
    
    .stat-text {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-top: 0.3rem;
    }
    
    .history-item {
        background: white;
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin: 0.75rem 0;
        border-left: 4px solid #7C9885;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    
    .history-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .history-date {
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        color: #333;
        font-size: 0.9rem;
    }
    
    .history-badge {
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-family: 'DM Sans', sans-serif;
        font-size: 0.8rem;
        font-weight: 600;
        color: white;
    }
    
    .history-preview {
        font-family: 'DM Sans', sans-serif;
        color: #666;
        font-size: 0.9rem;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #7C9885 0%, #5A7A63 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 2rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        box-shadow: 0 4px 15px rgba(124, 152, 133, 0.3) !important;
    }
    
    .logo-area {
        text-align: center;
        padding: 1.5rem 0;
    }
    
    .logo-icon { font-size: 3rem; }
    
    .logo-name {
        font-family: 'Fraunces', serif;
        font-size: 1.4rem;
        font-weight: 600;
        margin-top: 0.3rem;
    }
    
    .logo-tagline {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.85rem;
        opacity: 0.8;
    }
    
    .section-header {
        font-family: 'DM Sans', sans-serif;
        font-size: 0.9rem;
        font-weight: 600;
        color: #5A7A63;
        margin: 1rem 0 0.5rem 0;
    }
            
    /* DROPDOWN - White background, black text */
    .stMultiSelect > div > div {
        background: white !important;
        border: 2px solid #7C9885 !important;
        border-radius: 12px !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #7C9885 !important;
        color: white !important;
        border-radius: 20px !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] span {
        color: white !important;
    }
    
    .stMultiSelect svg {
        fill: white !important;
    }
    
    /* Dropdown menu */
    [data-baseweb="popover"] {
        background: white !important;
        border-radius: 12px !important;
    }
    
    [data-baseweb="menu"] {
        background: white !important;
    }
    
    [data-baseweb="menu"] li {
        color: #2D3A35 !important;
        background: white !important;
    }
    
    [data-baseweb="menu"] li:hover {
        background: rgba(124, 152, 133, 0.15) !important;
    }
</style>
""", unsafe_allow_html=True)

POSITIVE_ACTIVITIES = ["Meditation", "Exercise", "Nature Walk", "Reading", "Socializing", 
                       "Music", "Creative Work", "Cooking", "Gaming", "Learning", 
                       "Journaling", "Helping Others", "Rest Day"]

NEGATIVE_ACTIVITIES = ["Overtime Work", "Deadline Pressure", "Conflict", "Poor Sleep", 
                       "Skipped Meals", "Commuting", "Screen Time"]

with st.sidebar:
    st.markdown("""
    <div class="logo-area">
        <div class="logo-icon">🌿</div>
        <div class="logo-name">BurnoutGuard</div>
        <div class="logo-tagline">Wellness Analytics</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    page = st.radio("Menu", ["📝 New Entry", "📊 Dashboard", "📈 History"], label_visibility="collapsed")
    st.divider()
    
    st.markdown("""
    <div style="text-align: center; font-size: 0.8rem; opacity: 0.7; padding: 1rem;">
        Built with ❤️ for wellness<br>v1.0.0
    </div>
    """, unsafe_allow_html=True)

if page == "📝 New Entry":
    st.markdown("""
    <div class="welcome-banner">
        <div class="welcome-title">How are you feeling today?</div>
        <div class="welcome-subtitle">Take a moment to reflect on your day and track your wellbeing.</div>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="custom-card"><div class="card-title">📔 Journal Entry</div></div>', unsafe_allow_html=True)
        journal_text = st.text_area("Write about your day...", height=120, label_visibility="collapsed", placeholder="Write about your day, thoughts, or feelings...")
        
        st.markdown('<div class="custom-card"><div class="card-title">🎯 Today\'s Activities</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="section-header">✨ Wellness Activities</div>', unsafe_allow_html=True)
        positive_selected = st.multiselect("Positive", POSITIVE_ACTIVITIES, label_visibility="collapsed")
        
        st.markdown('<div class="section-header">⚠️ Stress Factors</div>', unsafe_allow_html=True)
        negative_selected = st.multiselect("Negative", NEGATIVE_ACTIVITIES, label_visibility="collapsed")
    
    with col2:
        st.markdown('<div class="custom-card"><div class="card-title">😴 Sleep & Stress</div></div>', unsafe_allow_html=True)
        
        sleep_hours = st.slider("Hours of Sleep", 0.0, 12.0, 7.0, 0.5)
        stress_level = st.slider("Stress Level (1-10)", 1, 10, 5)
        
        if positive_selected or negative_selected:
            st.markdown('<div class="custom-card"><div class="card-title">✓ Selected</div>', unsafe_allow_html=True)
            
            # Create pill-style selected items
            selected_html = '<div style="display: flex; flex-wrap: wrap; gap: 8px;">'
            for act in positive_selected:
                selected_html += f'<span style="background: #7C9885; color: white; padding: 8px 16px; border-radius: 25px; font-size: 0.9rem; font-family: DM Sans, sans-serif;">🌿 {act}</span>'
            for act in negative_selected:
                selected_html += f'<span style="background: #D98B8B; color: white; padding: 8px 16px; border-radius: 25px; font-size: 0.9rem; font-family: DM Sans, sans-serif;">⚠️ {act}</span>'
            selected_html += '</div>'
            
            st.markdown(selected_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    st.write("")
    col_btn = st.columns([1, 2, 1])[1]
    with col_btn:
        analyze_clicked = st.button("🔍 Analyze My Wellbeing", use_container_width=True)
    
    if analyze_clicked:
        all_activities = positive_selected + negative_selected
        
        if not journal_text and not all_activities:
            st.warning("Please enter some text or select activities.")
        else:
            with st.spinner("Analyzing..."):
                try:
                    response = requests.post(
                        f"{API_URL}/api/analyze",
                        json={
                            "text": journal_text,
                            "activities": all_activities,
                            "sleep_hours": sleep_hours,
                            "stress_level": stress_level
                        }
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        
                        st.success("✨ Analysis complete!")
                        st.write("")
                        
                        c1, c2, c3 = st.columns(3)
                        
                        with c1:
                            score = result["burnout_score"]
                            risk = result["risk_level"]
                            score_class = "score-low" if risk == "Low" else "score-moderate" if risk == "Moderate" else "score-high"
                            risk_class = "risk-low" if risk == "Low" else "risk-moderate" if risk == "Moderate" else "risk-high"
                            
                            st.markdown(f"""
                            <div class="custom-card">
                                <div class="card-title" style="text-align:center;">Burnout Score</div>
                                <div class="score-box">
                                    <div class="score-number {score_class}">{score:.0f}</div>
                                    <div class="score-label">out of 100</div>
                                    <div class="risk-badge {risk_class}">{risk} Risk</div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        with c2:
                            emotions = result.get("emotions", {})
                            sorted_emotions = sorted(emotions.items(), key=lambda x: x[1], reverse=True)[:5]
                            
                            st.markdown('<div class="custom-card"><div class="card-title">💭 Emotions</div>', unsafe_allow_html=True)
                            
                            for emo, val in sorted_emotions:
                                st.markdown(f"""
                                <div class="emotion-item">
                                    <span class="emotion-name">{emo.title()}</span>
                                    <div class="emotion-bar-container">
                                        <div class="emotion-bar" style="width:{val}%"></div>
                                    </div>
                                    <span class="emotion-percent">{val:.0f}%</span>
                                </div>
                                """, unsafe_allow_html=True)
                            
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        with c3:
                            st.markdown(f"""
                            <div class="custom-card">
                                <div class="card-title">💡 Insights</div>
                                <div class="insight-box">{result.get("insights", "")}</div>
                            </div>
                            """, unsafe_allow_html=True)
                        
                        recs = result.get("recommendations", [])
                        if recs:
                            st.markdown('<div class="custom-card"><div class="card-title">🌱 Recommendations</div>', unsafe_allow_html=True)
                            rec_cols = st.columns(2)
                            for i, rec in enumerate(recs):
                                with rec_cols[i % 2]:
                                    st.markdown(f'<div class="rec-item">{rec}</div>', unsafe_allow_html=True)
                            st.markdown('</div>', unsafe_allow_html=True)
                    else:
                        st.error("Error analyzing. Please try again.")
                
                except requests.exceptions.ConnectionError:
                    st.error("Cannot connect to API. Make sure backend is running!")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

elif page == "📊 Dashboard":
    st.markdown("""
    <div class="welcome-banner">
        <div class="welcome-title">Your Wellness Dashboard</div>
        <div class="welcome-subtitle">Track your progress and understand your patterns.</div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_URL}/api/history")
        
        if response.status_code == 200:
            data = response.json()
            entries = data.get("entries", [])
            
            if not entries:
                st.info("📝 No entries yet. Start by creating a new entry!")
            else:
                total = len(entries)
                avg = sum(e["burnout_score"] for e in entries) / total
                latest = entries[0]["burnout_score"]
                trend_icon = "📈" if total > 1 and entries[0]["burnout_score"] > entries[1]["burnout_score"] else "📉"
                
                c1, c2, c3, c4 = st.columns(4)
                
                with c1:
                    st.markdown(f'<div class="stat-box"><div class="stat-number">{total}</div><div class="stat-text">Total Entries</div></div>', unsafe_allow_html=True)
                with c2:
                    st.markdown(f'<div class="stat-box"><div class="stat-number">{avg:.0f}</div><div class="stat-text">Avg Score</div></div>', unsafe_allow_html=True)
                with c3:
                    st.markdown(f'<div class="stat-box"><div class="stat-number">{latest:.0f}</div><div class="stat-text">Latest</div></div>', unsafe_allow_html=True)
                with c4:
                    st.markdown(f'<div class="stat-box"><div class="stat-number">{trend_icon}</div><div class="stat-text">Trend</div></div>', unsafe_allow_html=True)
                
                st.write("")
                st.markdown('<div class="custom-card"><div class="card-title">📈 Score Trend</div></div>', unsafe_allow_html=True)
                
                if total >= 2:
                    dates = [e["timestamp"][:10] for e in reversed(entries)][-14:]
                    scores = [e["burnout_score"] for e in reversed(entries)][-14:]
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=list(range(len(scores))),
                        y=scores,
                        mode='lines+markers',
                        fill='tozeroy',
                        fillcolor='rgba(124, 152, 133, 0.2)',
                        line=dict(color='#7C9885', width=3),
                        marker=dict(size=8, color='#5A7A63'),
                        hovertemplate='Score: %{y}<extra></extra>'
                    ))
                    
                    fig.update_layout(
                        height=280,
                        margin=dict(l=40, r=20, t=20, b=40),
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        xaxis=dict(
                            tickmode='array',
                            tickvals=list(range(len(dates))),
                            ticktext=dates,
                            showgrid=False,
                            tickangle=-45
                        ),
                        yaxis=dict(range=[0, 100], showgrid=True, gridcolor='rgba(0,0,0,0.06)'),
                        font=dict(family='DM Sans', color='#333')
                    )
                    
                    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                else:
                    st.info("Add more entries to see your trend chart!")
    
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure backend is running!")
    except Exception as e:
        st.error(f"Error: {str(e)}")

elif page == "📈 History":
    st.markdown("""
    <div class="welcome-banner">
        <div class="welcome-title">Your Journal History</div>
        <div class="welcome-subtitle">Review your past entries and track your journey.</div>
    </div>
    """, unsafe_allow_html=True)
    
    try:
        response = requests.get(f"{API_URL}/api/history")
        
        if response.status_code == 200:
            data = response.json()
            entries = data.get("entries", [])
            
            if not entries:
                st.info("📝 No entries yet. Start by creating a new entry!")
            else:
                st.write(f"**Total entries:** {len(entries)}")
                
                for entry in entries:
                    score = entry["burnout_score"]
                    risk = entry["risk_level"]
                    color = "#7BAE7F" if risk == "Low" else "#E8C87A" if risk == "Moderate" else "#D98B8B"
                    
                    text = entry.get("text", "No text")
                    if text and len(text) > 120:
                        text = text[:120] + "..."
                    
                    st.markdown(f"""
                    <div class="history-item">
                        <div class="history-top">
                            <span class="history-date">📅 {entry["timestamp"][:10]} at {entry["timestamp"][11:16]}</span>
                            <span class="history-badge" style="background:{color};">Score: {score:.0f} | {risk}</span>
                        </div>
                        <div class="history-preview">{text}</div>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.error("Error fetching history.")
    
    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to API. Make sure backend is running!")
    except Exception as e:
        st.error(f"Error: {str(e)}")