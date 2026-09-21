"""
EduPath AI - Modern Dark-First Design System & CSS Helper Module
"""

import streamlit as st
import textwrap

def apply_custom_css():
    """Inject modern Dark-First SaaS CSS styles into the Streamlit application."""
    css = """
    <style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Outfit:wght@400;500;600;700;800&display=swap');

    /* Global Color Palette & Variables */
    :root {
        --bg-main: #070A12;
        --bg-sidebar: #0B0E14;
        --bg-card: #0D111C;
        --bg-card-hover: #151C2C;
        --bg-elevated: #111827;
        --border-color: rgba(255, 255, 255, 0.08);
        --border-accent: rgba(124, 58, 237, 0.35);
        --text-primary: #F8FAFC;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --accent-purple: #7C3AED;
        --accent-violet: #8B5CF6;
        --accent-cyan: #06B6D4;
        --accent-blue: #2563EB;
        --color-success: #10B981;
        --color-warning: #F59E0B;
        --color-danger: #EF4444;
    }

    /* Main App Background & Typography */
    .stApp {
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    /* Hide standard Streamlit header & footer */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    footer {
        visibility: hidden !important;
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-sidebar) !important;
        border-right: 1px solid var(--border-color) !important;
    }
    section[data-testid="stSidebar"] .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 1.5rem !important;
    }

    /* Sidebar Brand Box */
    .sidebar-brand-box {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.14) 0%, rgba(37, 99, 235, 0.12) 100%);
        border: 1px solid var(--border-accent);
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 20px;
    }
    .sidebar-brand-title {
        font-family: 'Outfit', sans-serif;
        font-size: 20px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #C4B5FD 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
    }
    .sidebar-brand-sub {
        font-size: 12px;
        color: var(--text-secondary);
        margin-top: 2px;
    }

    /* Top Application Header Banner */
    .app-header-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 24px;
        background: rgba(13, 17, 28, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid var(--border-color);
        border-radius: 16px;
        margin-bottom: 24px;
        box-shadow: 0 4px 24px rgba(0, 0, 0, 0.4);
    }
    .app-header-title {
        font-family: 'Outfit', sans-serif;
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(135deg, #FFFFFF 0%, #DDD6FE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: -0.5px;
        margin: 0;
    }
    .app-header-subtitle {
        font-size: 13px;
        color: var(--text-secondary);
        margin-top: 2px;
    }
    .agent-status-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #34D399;
        font-size: 13px;
        font-weight: 600;
        padding: 6px 14px;
        border-radius: 20px;
    }
    .status-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 10px #10B981;
    }

    /* Welcome Hero Banner */
    .welcome-hero-card {
        background: linear-gradient(135deg, rgba(124, 58, 237, 0.18) 0%, rgba(37, 99, 235, 0.1) 50%, rgba(6, 182, 212, 0.14) 100%);
        border: 1px solid rgba(124, 58, 237, 0.35);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 24px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    .welcome-title {
        font-family: 'Outfit', sans-serif;
        font-size: 26px;
        font-weight: 800;
        color: #FFFFFF;
        margin-bottom: 4px;
    }
    .welcome-subtitle {
        font-size: 14px;
        color: #CBD5E1;
        margin-bottom: 16px;
    }

    /* Visual Learning Path Stepper */
    .path-stepper-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: rgba(13, 17, 28, 0.6);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 12px 18px;
        margin-top: 14px;
        gap: 6px;
    }
    .path-step {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12px;
        font-weight: 600;
        color: var(--text-secondary);
    }
    .path-step-active {
        color: #C4B5FD;
    }
    .path-step-icon {
        width: 24px;
        height: 24px;
        border-radius: 50%;
        background: rgba(124, 58, 237, 0.2);
        border: 1px solid var(--accent-purple);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
    }
    .path-arrow {
        color: var(--text-muted);
        font-size: 12px;
    }

    /* Metric Cards */
    div[data-testid="stMetric"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 14px !important;
        padding: 16px !important;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2) !important;
        transition: transform 0.2s ease, border-color 0.2s ease !important;
    }
    div[data-testid="stMetric"]:hover {
        border-color: var(--accent-purple) !important;
        transform: translateY(-2px);
    }
    div[data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif !important;
        font-size: 28px !important;
        font-weight: 800 !important;
        color: var(--text-primary) !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 13px !important;
        font-weight: 500 !important;
        color: var(--text-secondary) !important;
    }

    /* Custom Cards */
    .ep-card {
        background-color: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
    }
    .ep-card-title {
        font-family: 'Outfit', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* Skill & Tech Badges / Chips */
    .badge-chip {
        display: inline-flex;
        align-items: center;
        background: rgba(124, 58, 237, 0.12);
        border: 1px solid rgba(124, 58, 237, 0.3);
        color: #DDD6FE;
        font-size: 12px;
        font-weight: 600;
        padding: 5px 12px;
        border-radius: 20px;
        margin: 3px 6px 3px 0;
        transition: all 0.2s ease;
    }
    .badge-chip:hover {
        background: rgba(124, 58, 237, 0.25);
        border-color: var(--accent-purple);
        color: #FFFFFF;
    }
    .badge-chip-success {
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.35);
        color: #6EE7B7;
    }
    .badge-chip-critical {
        background: rgba(239, 68, 68, 0.14);
        border: 1px solid rgba(239, 68, 68, 0.4);
        color: #FCA5A5;
    }
    .badge-chip-important {
        background: rgba(245, 158, 11, 0.14);
        border: 1px solid rgba(245, 158, 11, 0.4);
        color: #FDE047;
    }
    .badge-chip-tool {
        background: rgba(6, 182, 212, 0.12);
        border: 1px solid rgba(6, 182, 212, 0.35);
        color: #67E8F9;
    }

    /* Tabs Styling */
    div[data-baseweb="tab-list"] {
        background-color: var(--bg-card) !important;
        border-radius: 14px !important;
        padding: 6px !important;
        border: 1px solid var(--border-color) !important;
        gap: 6px !important;
    }
    button[data-baseweb="tab"] {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 20px !important;
        color: var(--text-secondary) !important;
        border: none !important;
        transition: all 0.2s ease !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: var(--bg-elevated) !important;
        color: var(--text-primary) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35) !important;
    }

    /* Button Styling */
    .stButton > button {
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 20px !important;
        border: 1px solid var(--border-color) !important;
        background-color: var(--bg-elevated) !important;
        color: var(--text-primary) !important;
        transition: all 0.2s ease-in-out !important;
    }
    .stButton > button:hover {
        border-color: var(--accent-purple) !important;
        background-color: var(--bg-card-hover) !important;
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.25) !important;
    }

    /* Primary Action Buttons */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, var(--accent-purple) 0%, #6D28D9 100%) !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 4px 16px rgba(124, 58, 237, 0.4) !important;
    }
    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #6D28D9 0%, #5B21B6 100%) !important;
        box-shadow: 0 6px 24px rgba(124, 58, 237, 0.6) !important;
        transform: translateY(-1px);
    }

    /* Expander Styling */
    div[data-testid="stExpander"] {
        background-color: var(--bg-card) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 14px !important;
        margin-bottom: 12px !important;
        overflow: hidden !important;
    }
    div[data-testid="stExpander"] details summary {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: var(--text-primary) !important;
        padding: 14px 18px !important;
    }

    /* Prioritized Action Item List */
    .action-item-card {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 14px 20px;
        margin-bottom: 10px;
        transition: border-color 0.2s ease;
    }
    .action-item-card:hover {
        border-color: var(--accent-purple);
    }
    .action-item-num {
        font-family: 'Outfit', sans-serif;
        font-size: 16px;
        font-weight: 800;
        color: #C4B5FD;
        width: 32px;
    }
    .action-item-title {
        font-size: 14px;
        font-weight: 600;
        color: var(--text-primary);
        flex: 1;
    }

    /* Adaptive Loop Horizontal Diagram */
    .loop-diagram-container {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: var(--bg-card);
        border: 1px solid var(--border-color);
        border-radius: 14px;
        padding: 16px 24px;
        margin: 16px 0 24px 0;
        gap: 8px;
    }
    .loop-step {
        display: flex;
        flex-direction: column;
        align-items: center;
        gap: 6px;
        text-align: center;
        flex: 1;
    }
    .loop-step-icon {
        width: 38px;
        height: 38px;
        border-radius: 50%;
        background: rgba(124, 58, 237, 0.15);
        border: 1px solid var(--accent-purple);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        color: #C4B5FD;
    }
    .loop-step-label {
        font-size: 12px;
        font-weight: 600;
        color: var(--text-primary);
    }
    .loop-arrow {
        color: var(--text-muted);
        font-size: 16px;
        font-weight: bold;
    }

    /* Evaluation Result Prominent Cards */
    .eval-card-pass {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(6, 78, 59, 0.3) 100%);
        border: 1px solid rgba(16, 185, 129, 0.45);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(16, 185, 129, 0.15);
    }
    .eval-card-fail {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(120, 53, 15, 0.3) 100%);
        border: 1px solid rgba(245, 158, 11, 0.45);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(245, 158, 11, 0.15);
    }
    .eval-score-number {
        font-family: 'Outfit', sans-serif;
        font-size: 46px;
        font-weight: 800;
        margin: 8px 0;
        letter-spacing: -1px;
    }
    .adaptation-alert-banner {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.18) 0%, rgba(127, 29, 29, 0.35) 100%);
        border: 1px solid rgba(239, 68, 68, 0.45);
        border-radius: 14px;
        padding: 20px 24px;
        margin-top: 18px;
        display: flex;
        align-items: flex-start;
        gap: 16px;
        box-shadow: 0 6px 24px rgba(239, 68, 68, 0.2);
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

def render_app_header():
    """Render the top clean application header."""
    header_html = textwrap.dedent("""
    <div class="app-header-container">
    <div>
    <div class="app-header-title">◆ EduPath AI</div>
    <div class="app-header-subtitle">Your adaptive AI-powered learning companion</div>
    </div>
    <div style="flex: 1; max-width: 320px; margin: 0 24px;">
    <input type="text" placeholder="🔍 Search skills, topics, or resources..." style="width: 100%; background: #0D111C; border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; padding: 6px 16px; font-size: 13px; color: #F8FAFC;" />
    </div>
    <div class="agent-status-badge">
    <span class="status-dot"></span>
    Gemini AI Agent Online
    </div>
    </div>
    """)
    st.markdown(header_html, unsafe_allow_html=True)

def render_welcome_hero(learner_name, target_role):
    """Render the top welcome hero section for analyzed users."""
    hero_html = textwrap.dedent(f"""
    <div class="welcome-hero-card">
    <div class="welcome-title">Welcome, {learner_name}! 👋</div>
    <div class="welcome-subtitle">Your adaptive AI-powered learning companion for a stronger career.</div>
    <div style="display: flex; align-items: center; gap: 10px;">
    <span style="font-size: 18px;">🎯</span>
    <span style="font-weight: 700; color: #FFFFFF; font-size: 16px;">Target Role: <span style="color: #C4B5FD;">{target_role}</span></span>
    <span style="font-size: 12px; color: #94A3B8;">— Your current career goal</span>
    </div>
    </div>
    """)
    st.markdown(hero_html, unsafe_allow_html=True)

def render_fresh_user_hero():
    """Render the hero section for fresh users before resume analysis."""
    html = textwrap.dedent("""
    <div class="welcome-hero-card">
    <div class="welcome-title">Turn Your Skills Into Global Opportunities 🚀</div>
    <div class="welcome-subtitle">Upload your resume, discover your skill gaps, and get a personalized learning roadmap powered by AI.</div>
    <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(124, 58, 237, 0.2); border: 1px solid #7C3AED; color: #DDD6FE; font-size: 13px; font-weight: 600; padding: 6px 14px; border-radius: 20px;">
    ✨ Get Started Below → Upload your resume to begin your personalized journey.
    </div>
    </div>
    """)
    st.markdown(html, unsafe_allow_html=True)

def render_workflow_steps():
    """Render the 5-step visual workflow for fresh users."""
    html = textwrap.dedent("""
    <div style="margin-top: 14px;">
    <div style="font-size: 14px; font-weight: 700; color: #F8FAFC; margin-bottom: 8px;">🔄 How EduPath AI Works</div>
    <div class="loop-diagram-container">
    <div class="loop-step">
    <div class="loop-step-icon">📄</div>
    <div class="loop-step-label">1. Upload Resume</div>
    </div>
    <div class="loop-arrow">→</div>
    <div class="loop-step">
    <div class="loop-step-icon">🔍</div>
    <div class="loop-step-label">2. Analyze Skills</div>
    </div>
    <div class="loop-arrow">→</div>
    <div class="loop-step">
    <div class="loop-step-icon">⚠️</div>
    <div class="loop-step-label">3. Identify Gaps</div>
    </div>
    <div class="loop-arrow">→</div>
    <div class="loop-step">
    <div class="loop-step-icon">🗺️</div>
    <div class="loop-step-label">4. Generate Roadmap</div>
    </div>
    <div class="loop-arrow">→</div>
    <div class="loop-step">
    <div class="loop-step-icon">🚀</div>
    <div class="loop-step-label">5. Start Learning</div>
    </div>
    </div>
    </div>
    """)
    st.markdown(html, unsafe_allow_html=True)

def render_empty_state_card(title="No Resume Analyzed Yet", description="Upload your resume and select a target role to generate your personalized learning profile, identify skill gaps, and build your adaptive roadmap."):
    """Render a clean empty state component."""
    html = textwrap.dedent(f"""
    <div class="ep-card" style="text-align: center; padding: 40px 24px; margin-top: 16px;">
    <div style="font-size: 44px; margin-bottom: 12px;">📂</div>
    <div style="font-family: 'Outfit', sans-serif; font-size: 20px; font-weight: 700; color: #FFFFFF; margin-bottom: 8px;">{title}</div>
    <div style="font-size: 14px; color: #94A3B8; max-width: 520px; margin: 0 auto;">{description}</div>
    </div>
    """)
    st.markdown(html, unsafe_allow_html=True)

def render_donut_chart(percentage, label="Role Readiness", subtitle="", size=120, stroke_width=10):
    """Render a clean SVG radial donut chart for readiness or evaluation scores."""
    percentage = max(0.0, min(100.0, float(percentage)))
    radius = (size - stroke_width) / 2
    circumference = 2 * 3.14159265 * radius
    dash_offset = circumference * (1 - (percentage / 100.0))
    
    color = "#10B981" if percentage >= 70 else ("#F59E0B" if percentage > 0 else "#7C3AED")
    
    svg = textwrap.dedent(f"""
    <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; margin: 6px 0;">
    <div style="position: relative; width: {size}px; height: {size}px;">
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" style="transform: rotate(-90deg);">
    <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="#111827" stroke-width="{stroke_width}" />
    <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none" stroke="{color}" stroke-width="{stroke_width}" stroke-dasharray="{circumference}" stroke-dashoffset="{dash_offset}" stroke-linecap="round" style="transition: stroke-dashoffset 0.8s ease;" />
    </svg>
    <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center;">
    <span style="font-family: 'Outfit', sans-serif; font-size: 22px; font-weight: 800; color: #FFFFFF;">{percentage:.0f}%</span>
    </div>
    </div>
    <div style="margin-top: 6px; font-weight: 700; font-size: 13px; color: #F8FAFC;">{label}</div>
    {"<div style='font-size: 11px; color: #94A3B8; margin-top: 2px;'>" + subtitle + "</div>" if subtitle else ""}
    </div>
    """)
    st.markdown(svg, unsafe_allow_html=True)

def render_agentic_loop_visualizer():
    """Render a visual step diagram explaining the adaptive agentic loop."""
    html = textwrap.dedent("""
    <div class="loop-diagram-container">
    <div class="loop-step">
    <div class="loop-step-icon">🧪</div>
    <div class="loop-step-label">1. Practice</div>
    </div>
    <div class="loop-arrow">→</div>
    <div class="loop-step">
    <div class="loop-step-icon">🤖</div>
    <div class="loop-step-label">2. Evaluate</div>
    </div>
    <div class="loop-arrow">→</div>
    <div class="loop-step">
    <div class="loop-step-icon">🔍</div>
    <div class="loop-step-label">3. Detect Weakness</div>
    </div>
    <div class="loop-arrow">→</div>
    <div class="loop-step">
    <div class="loop-step-icon">⚡</div>
    <div class="loop-step-label">4. Adapt Roadmap</div>
    </div>
    <div class="loop-arrow">→</div>
    <div class="loop-step">
    <div class="loop-step-icon">🎯</div>
    <div class="loop-step-label">5. Remedial Focus</div>
    </div>
    </div>
    """)
    st.markdown(html, unsafe_allow_html=True)
