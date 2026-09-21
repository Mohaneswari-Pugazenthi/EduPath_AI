import streamlit as st
import config
from core.gemini_client import GeminiClient
from core.agent import EduPathAgent
from tools.practice_generator import generate_strong_demo_answer, generate_weak_demo_answer
import styles

# Page Configuration
st.set_page_config(
    page_title=f"{config.APP_NAME} AI - {config.APP_TAGLINE}",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

def init_session_state():
    """Initialize session state variables."""
    if "gemini_client" not in st.session_state:
        st.session_state.gemini_client = GeminiClient()

    if "agent" not in st.session_state or not hasattr(st.session_state.agent, "evaluate_and_adapt"):
        st.session_state.agent = EduPathAgent(st.session_state.gemini_client)

    if "profile_analyzed" not in st.session_state:
        st.session_state.profile_analyzed = False

    if "learner_profile" not in st.session_state:
        st.session_state.learner_profile = None

    if "target_role" not in st.session_state:
        st.session_state.target_role = config.TARGET_ROLES[0]

    if "raw_resume_text" not in st.session_state:
        st.session_state.raw_resume_text = ""

    if "skill_gap_report" not in st.session_state:
        st.session_state.skill_gap_report = None

    if "learning_roadmap" not in st.session_state:
        st.session_state.learning_roadmap = None

    if "current_practice_skill" not in st.session_state:
        st.session_state.current_practice_skill = None

    if "current_practice_task" not in st.session_state:
        st.session_state.current_practice_task = None

    if "latest_evaluation" not in st.session_state:
        st.session_state.latest_evaluation = None

    if "latest_adaptation" not in st.session_state:
        st.session_state.latest_adaptation = None

def get_task_aware_demo_answers(task):
    """Generate task-aware weak and strong demo answers corresponding to the current task skill."""
    return generate_weak_demo_answer(task), generate_strong_demo_answer(task)

def render_profile_display(profile, target_role):
    """Render the extracted Learner Profile in modern dark dashboard cards."""
    learner_name = profile.name or "Learner"
    styles.render_welcome_hero(learner_name, target_role)

    readiness_num = st.session_state.skill_gap_report.readiness_percentage if st.session_state.skill_gap_report else 0.0
    gap_count = len(st.session_state.skill_gap_report.missing_core_skills) if st.session_state.skill_gap_report else 0
    modules_count = len(st.session_state.learning_roadmap.weeks) if st.session_state.learning_roadmap else 0
    skills_count = (len(profile.technical_skills) + len(profile.tools_and_technologies)) if (profile and (profile.technical_skills or profile.tools_and_technologies)) else 0

    # KPI / Metric Cards Grid
    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("🎯 Target Role", target_role)
    with k2:
        donut_html = styles.render_donut_chart(readiness_num, label="Role Readiness", subtitle="Benchmark Score")
        st.markdown(donut_html, unsafe_allow_html=True)
    with k3:
        st.metric("📚 Skills Identified", skills_count)
    with k4:
        st.metric("⚠️ Critical Gaps", gap_count)
    with k5:
        st.metric("🧩 Active Modules", modules_count)

    st.markdown("<br>", unsafe_allow_html=True)

    # Learning Profile Section
    st.markdown("<div class='ep-card'>", unsafe_allow_html=True)
    st.markdown("<div class='ep-card-title'>👤 Your Learning Profile</div>", unsafe_allow_html=True)

    c_sk, c_tl = st.columns(2)
    with c_sk:
        st.markdown("**Technical Skills:**")
        if profile.technical_skills:
            badges_html = "".join([f"<span class='badge-chip'>{s}</span>" for s in profile.technical_skills])
            st.markdown(f"<div>{badges_html}</div><br>", unsafe_allow_html=True)
        else:
            st.info("No technical skills extracted yet.")

    with c_tl:
        st.markdown("**Tools & Technologies:**")
        if profile.tools_and_technologies:
            tools_html = "".join([f"<span class='badge-chip badge-chip-tool'>{t}</span>" for t in profile.tools_and_technologies])
            st.markdown(f"<div>{tools_html}</div>", unsafe_allow_html=True)
        else:
            st.info("No tools or technologies extracted yet.")

    st.markdown("</div>", unsafe_allow_html=True)

    # Project Experience Section
    if profile.projects:
        st.markdown("### 📂 Project Experience")
        p_cols = st.columns(min(3, max(1, len(profile.projects))))
        for idx, proj in enumerate(profile.projects[:3]):
            with p_cols[idx % len(p_cols)]:
                st.markdown("<div class='ep-card'>", unsafe_allow_html=True)
                st.markdown(f"<div class='ep-card-title'>📌 {proj.title}</div>", unsafe_allow_html=True)
                if proj.description:
                    st.write(proj.description)
                if proj.technologies:
                    tech_badges = "".join([f"<span class='badge-chip'>{t}</span>" for t in proj.technologies])
                    st.markdown(f"<div style='margin-top: 10px;'>{tech_badges}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)

    # Education + Certifications Section
    if profile.education or profile.certifications:
        col_edu, col_cert = st.columns(2)
        with col_edu:
            st.markdown("<div class='ep-card'>", unsafe_allow_html=True)
            st.markdown("<div class='ep-card-title'>🎓 Education</div>", unsafe_allow_html=True)
            if profile.education:
                for edu in profile.education:
                    inst = f" ({edu.institution})" if edu.institution else ""
                    yr = f" - {edu.year}" if edu.year else ""
                    st.write(f"• **{edu.degree}**{inst}{yr}")
            else:
                st.caption("No formal education records listed.")
            st.markdown("</div>", unsafe_allow_html=True)

        with col_cert:
            st.markdown("<div class='ep-card'>", unsafe_allow_html=True)
            st.markdown("<div class='ep-card-title'>🏆 Certifications</div>", unsafe_allow_html=True)
            if profile.certifications:
                for cert in profile.certifications:
                    issuer = f" ({cert.issuer})" if cert.issuer else ""
                    st.write(f"• **{cert.title}**{issuer}")
            else:
                st.caption("No professional certifications listed.")
            st.markdown("</div>", unsafe_allow_html=True)

def render_gap_analysis_display(report):
    """Render the Skill Gap Matrix in clean categorized chip containers."""
    st.markdown(f"### 📊 Skill Gap Matrix — `:blue[{report.target_role}]`")

    m1, m2 = st.columns([1, 2])
    with m1:
        donut_html = styles.render_donut_chart(report.readiness_percentage, label="Role Readiness", subtitle="Target Benchmark Score", size=140)
        st.markdown(donut_html, unsafe_allow_html=True)
    with m2:
        st.markdown("**Role Readiness Benchmark Progress**")
        st.progress(min(1.0, max(0.0, report.readiness_percentage / 100.0)))
        st.caption("Calculated deterministically: Core Skills 60% weight | Supporting 25% | Tools 15%")

    st.info(f"💡 **AI Skill Gap Summary:**\n\n{report.gap_summary}")

    st.markdown("<br>", unsafe_allow_html=True)

    c_acq, c_crit = st.columns(2)
    with c_acq:
        st.markdown("<div class='ep-card'>", unsafe_allow_html=True)
        st.markdown("<div class='ep-card-title'>✅ Acquired Skills</div>", unsafe_allow_html=True)
        if report.acquired_core_skills:
            acq_html = "".join([f"<span class='badge-chip badge-chip-success'>✓ {s}</span>" for s in report.acquired_core_skills])
            st.markdown(f"<div>{acq_html}</div>", unsafe_allow_html=True)
        else:
            st.caption("No core benchmark skills matched yet.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c_crit:
        st.markdown("<div class='ep-card'>", unsafe_allow_html=True)
        st.markdown("<div class='ep-card-title'>⚠️ Critical Skill Gaps</div>", unsafe_allow_html=True)
        if report.missing_core_skills:
            crit_html = "".join([f"<span class='badge-chip badge-chip-critical'>! {s}</span>" for s in report.missing_core_skills])
            st.markdown(f"<div>{crit_html}</div>", unsafe_allow_html=True)
        else:
            st.success("All core benchmark skills acquired!")
        st.markdown("</div>", unsafe_allow_html=True)

    c_supp, c_tech = st.columns(2)
    with c_supp:
        st.markdown("<div class='ep-card'>", unsafe_allow_html=True)
        st.markdown("<div class='ep-card-title'>🟡 Supporting Gaps</div>", unsafe_allow_html=True)
        if report.missing_supporting_skills:
            supp_html = "".join([f"<span class='badge-chip badge-chip-important'>⚡ {s}</span>" for s in report.missing_supporting_skills])
            st.markdown(f"<div>{supp_html}</div>", unsafe_allow_html=True)
        else:
            st.caption("No supporting gaps.")
        st.markdown("</div>", unsafe_allow_html=True)

    with c_tech:
        st.markdown("<div class='ep-card'>", unsafe_allow_html=True)
        st.markdown("<div class='ep-card-title'>🔵 Technology Gaps</div>", unsafe_allow_html=True)
        if report.technology_gaps:
            tech_html = "".join([f"<span class='badge-chip badge-chip-tool'>🛠️ {t}</span>" for t in report.technology_gaps])
            st.markdown(f"<div>{tech_html}</div>", unsafe_allow_html=True)
        else:
            st.caption("No tool gaps.")
        st.markdown("</div>", unsafe_allow_html=True)

    # Prioritized Action Plan
    if report.prioritized_gaps:
        st.markdown("### 📋 Recommended Action Plan")
        for idx, item in enumerate(report.prioritized_gaps):
            num_str = f"{idx+1:02d}"
            badge_cls = "badge-chip-critical" if item.priority == "Critical" else "badge-chip-important"
            st.markdown(
                f"""
                <div class="action-item-card">
                    <div class="action-item-num">{num_str}</div>
                    <div class="action-item-title">{item.skill}</div>
                    <div style="display: flex; gap: 8px;">
                        <span class="badge-chip {badge_cls}">{item.priority}</span>
                        <span class="badge-chip">{item.category}</span>
                    </div>
                    <div style="color: #A5B4FC; font-weight: bold; margin-left: 12px;">→</div>
                </div>
                """,
                unsafe_allow_html=True
            )

def render_roadmap_display(roadmap):
    """Render the Personalized Learning Roadmap with visual journey stepper & remedial banners."""
    st.markdown(f"### 🗓️ Personalized Learning Roadmap")

    is_adapted = any("remedial" in w.title.lower() for w in roadmap.weeks)
    if is_adapted:
        st.markdown(
            """
            <div class="adaptation-alert-banner">
                <div style="font-size: 28px;">🤖</div>
                <div>
                    <div style="font-weight: 800; color: #EF4444; font-size: 16px;">AI ADAPTATION DETECTED</div>
                    <div style="color: #F3F4F6; font-size: 14px; margin-top: 4px;">
                        We identified a concept gap from your Practice Lab evaluation.<br/>
                        <b>REMEDIAL MODULE INSERTED:</b> A targeted remedial module (<i>Status: 🔴 Needs Attention</i>) has been dynamically added to your roadmap.
                    </div>
                </div>
            </div>
            <br>
            """,
            unsafe_allow_html=True
        )

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Target Role", roadmap.target_role)
    with m2:
        st.metric("Readiness Before Plan", f"{roadmap.readiness_score_before}%")
    with m3:
        status_txt = f"{len(roadmap.weeks)} Modules (Adapted)" if is_adapted else f"{len(roadmap.weeks)} Weeks"
        st.metric("Duration / Modules", status_txt)

    st.info(f"📌 **Roadmap Summary:**\n\n{roadmap.summary}")

    # Visual Stepper Banner
    st.markdown("#### 🗺️ Learning Path Journey")
    st.markdown(
        """
        <div class="path-stepper-container">
            <div class="path-step path-step-active"><div class="path-step-icon">01</div><span>Foundations</span></div>
            <div class="path-arrow">→</div>
            <div class="path-step path-step-active"><div class="path-step-icon">02</div><span>LLM App Dev</span></div>
            <div class="path-arrow">→</div>
            <div class="path-step path-step-active"><div class="path-step-icon">03</div><span>RAG & Vector Search</span></div>
            <div class="path-arrow">→</div>
            <div class="path-step path-step-active"><div class="path-step-icon">04</div><span>Engineering Infra</span></div>
            <div class="path-arrow">→</div>
            <div class="path-step path-step-active"><div class="path-step-icon">05</div><span>Advanced Frameworks</span></div>
        </div>
        <br>
        """,
        unsafe_allow_html=True
    )

    for week in roadmap.weeks:
        is_remedial_week = "remedial" in week.title.lower()
        badge = "🔴 REMEDIAL MODULE" if is_remedial_week else f"WEEK {week.week_number}"
        
        with st.expander(f"📌 {badge}: {week.title}", expanded=is_remedial_week or week.week_number == 1):
            if is_remedial_week:
                st.warning("⚠️ **Remedial Focus Area**: Inserted dynamically to reinforce detected weak concepts.")
                
            col_left, col_right = st.columns([2, 1])
            
            with col_left:
                st.markdown("#### 🎯 Learning Objectives")
                for obj in week.learning_objectives:
                    st.markdown(f"- {obj}")

                st.markdown("#### 📚 Core Topics")
                for topic in week.topics:
                    st.markdown(f"- {topic}")

                st.markdown("#### 🧪 Hands-On Practice Task")
                st.info(week.practice_task)

            with col_right:
                st.markdown("#### 🛠️ Skills Targeted")
                for sk in week.skills_targeted:
                    st.markdown(f"- `:blue[{sk}]`")

                st.markdown(f"#### ⏱️ Estimated Time\n**{week.estimated_hours} hours**")

                st.markdown("#### 🔍 Recommended Resources")
                for res in week.resource_recommendations:
                    st.markdown(f"- 📖 *{res}*")

                st.markdown("#### ✅ Expected Outcome")
                st.success(week.expected_outcome)

def main():
    init_session_state()

    # Apply Custom CSS
    styles.apply_custom_css()

    # App Header
    styles.render_app_header()

    agent_status = st.session_state.agent.get_agent_status()
    profile_analyzed = st.session_state.get("profile_analyzed", False) and (st.session_state.learner_profile is not None)

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-brand-box">
                <div class="sidebar-brand-title">🎓 EDUPATH AI</div>
                <div class="sidebar-brand-sub">Adaptive Learning Agent</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        if agent_status["ready"]:
            st.markdown("<span style='color: #34D399; font-weight: 600;'>🟢 Gemini AI Agent Online</span>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ API Key Pending / Offline")

        st.divider()

        st.caption(f"Model: `{agent_status['gemini_status']['model']}`")
        if profile_analyzed:
            st.caption("Learner Profile: **Loaded**")
            if st.session_state.skill_gap_report:
                st.caption(f"Readiness Score: **{st.session_state.skill_gap_report.readiness_percentage}%**")
        else:
            st.caption("Learner Profile: **Not Analyzed**")

        st.divider()

        # Learner Status Card at bottom of sidebar
        target_role_display = st.session_state.target_role if profile_analyzed else (st.session_state.get("target_role", "Not selected"))
        readiness_val = f"{st.session_state.skill_gap_report.readiness_percentage}%" if (profile_analyzed and st.session_state.skill_gap_report) else "0%"
        mod_val = len(st.session_state.learning_roadmap.weeks) if (profile_analyzed and st.session_state.learning_roadmap) else 0
        skills_val = (len(st.session_state.learner_profile.technical_skills) + len(st.session_state.learner_profile.tools_and_technologies)) if (profile_analyzed and st.session_state.learner_profile) else 0

        st.markdown(
            f"""
            <div class="ep-card" style="padding: 14px; margin-bottom: 0;">
                <div style="font-size: 11px; color: #9CA3AF; text-transform: uppercase; font-weight: 700;">YOUR GOAL</div>
                <div style="font-size: 15px; font-weight: 700; color: #FFFFFF;">{target_role_display}</div>
                <hr style="margin: 8px 0; border-color: rgba(255,255,255,0.08);"/>
                <div style="display: flex; justify-content: space-between; font-size: 12px;">
                    <span style="color: #9CA3AF;">Readiness:</span>
                    <span style="font-weight: 700; color: #34D399;">{readiness_val}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-top: 4px;">
                    <span style="color: #9CA3AF;">Active Modules:</span>
                    <span style="font-weight: 700; color: #A5B4FC;">{mod_val}</span>
                </div>
                <div style="display: flex; justify-content: space-between; font-size: 12px; margin-top: 4px;">
                    <span style="color: #9CA3AF;">Skills Identified:</span>
                    <span style="font-weight: 700; color: #F3F4F6;">{skills_val}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 Dashboard & Profile",
        "📊 Skill Gap Matrix",
        "🗺️ Adaptive Roadmap",
        "🧪 Practice Lab & Evaluator"
    ])

    with tab1:
        # Hero Section
        if profile_analyzed:
            learner_name = st.session_state.learner_profile.name or "Learner"
            styles.render_welcome_hero(learner_name, st.session_state.target_role)
        else:
            styles.render_fresh_user_hero()
            styles.render_workflow_steps()

        # Step 1: Resume Upload Workspace
        st.markdown("<div class='ep-card'>", unsafe_allow_html=True)
        st.markdown("<div class='ep-card-title'>⚡ Start Your Career Journey — Upload Resume & Select Target Role</div>", unsafe_allow_html=True)
        
        col_up, col_role = st.columns([2, 1])
        with col_up:
            uploaded_file = st.file_uploader("Upload Resume (PDF)", type=["pdf"], help="Select a text-based PDF resume.")
            if uploaded_file:
                st.markdown(f"📄 `{uploaded_file.name}` ({round(uploaded_file.size / 1024, 1)} KB) — <span style='color: #34D399;'>✓ Ready to analyze</span>", unsafe_allow_html=True)
        with col_role:
            target_role = st.selectbox("Select Target Role", config.TARGET_ROLES, index=0)
            st.session_state.target_role = target_role

        analyze_clicked = st.button("✨ Analyze My Profile →", type="primary")

        if analyze_clicked:
            if not uploaded_file:
                st.error("Please upload a PDF resume before analyzing.")
            elif not agent_status["ready"]:
                st.error("Gemini API key is missing or invalid. Please check your `.env` configuration.")
            else:
                with st.spinner("Parsing resume text and invoking Gemini Agent to build structured profile..."):
                    result = st.session_state.agent.analyze_resume_and_build_profile(
                        uploaded_file, target_role
                    )

                if result["success"]:
                    st.session_state.learner_profile = result["profile"]
                    st.session_state.target_role = result["target_role"]
                    st.session_state.raw_resume_text = result["raw_text"]
                    st.session_state.profile_analyzed = True
                    
                    gap_res = st.session_state.agent.perform_skill_gap_analysis(
                        st.session_state.learner_profile, st.session_state.target_role
                    )
                    if gap_res["success"]:
                        st.session_state.skill_gap_report = gap_res["report"]
                        
                        roadmap_res = st.session_state.agent.generate_personalized_roadmap(
                            st.session_state.learner_profile, st.session_state.skill_gap_report
                        )
                        if roadmap_res["success"]:
                            st.session_state.learning_roadmap = roadmap_res["roadmap"]
                            
                            first_skill = roadmap_res["roadmap"].weeks[0].skills_targeted[0] if roadmap_res["roadmap"].weeks[0].skills_targeted else "Vector Databases"
                            st.session_state.current_practice_skill = first_skill
                            
                            task_res = st.session_state.agent.create_practice_task(
                                st.session_state.learning_roadmap,
                                st.session_state.learner_profile,
                                selected_skill=first_skill
                            )
                            if task_res["success"]:
                                st.session_state.current_practice_task = task_res["task"]

                    skills_found_cnt = len(st.session_state.learner_profile.technical_skills) + len(st.session_state.learner_profile.tools_and_technologies)
                    gaps_found_cnt = len(st.session_state.skill_gap_report.missing_core_skills) if st.session_state.skill_gap_report else 0
                    st.success(f"✓ Resume analyzed successfully | {skills_found_cnt} skills identified | {gaps_found_cnt} critical gaps detected")
                    st.rerun()
                else:
                    st.error(f"Analysis Failed: {result['error']}")

        st.markdown("</div>", unsafe_allow_html=True)

        # Profile View Conditional Rendering
        if profile_analyzed and st.session_state.learner_profile:
            render_profile_display(st.session_state.learner_profile, st.session_state.target_role)
        else:
            # Fresh User Quick Stats Row (All 0s)
            k1, k2, k3, k4, k5 = st.columns(5)
            with k1:
                st.metric("🎯 Target Role", st.session_state.target_role if uploaded_file else "Not selected")
            with k2:
                donut_html = styles.render_donut_chart(0.0, label="Role Readiness", subtitle="Upload resume to start")
                st.markdown(donut_html, unsafe_allow_html=True)
            with k3:
                st.metric("📚 Skills Identified", 0)
            with k4:
                st.metric("⚠️ Critical Gaps", 0)
            with k5:
                st.metric("🧩 Active Modules", 0)
                
            styles.render_empty_state_card(
                title="No Resume Analyzed Yet",
                description="Upload your resume above and click 'Analyze My Profile' to extract your current skills, compute role readiness, and generate your adaptive roadmap."
            )

    with tab2:
        if not profile_analyzed or not st.session_state.skill_gap_report:
            styles.render_empty_state_card(
                title="No Skill Gap Analysis Yet",
                description="Upload your resume and click 'Analyze My Profile' in Tab 1 to compute your readiness score and skill gap matrix against target role benchmarks."
            )
        else:
            st.markdown(f"Target Role Selected: **{st.session_state.target_role}**")
            
            recalculate = st.button("🔄 Recalculate Skill Gap Analysis")
            if recalculate:
                with st.spinner("Evaluating skill gaps against target role benchmark..."):
                    gap_res = st.session_state.agent.perform_skill_gap_analysis(
                        st.session_state.learner_profile, st.session_state.target_role
                    )
                    if gap_res["success"]:
                        st.session_state.skill_gap_report = gap_res["report"]
                    else:
                        st.error(f"Skill gap calculation failed: {gap_res['error']}")

            render_gap_analysis_display(st.session_state.skill_gap_report)

    with tab3:
        if not profile_analyzed or not st.session_state.learning_roadmap:
            styles.render_empty_state_card(
                title="No Adaptive Roadmap Yet",
                description="Complete resume analysis in Tab 1 to generate a personalized 4-week learning roadmap addressing your specific skill gaps."
            )
        else:
            btn_gen_roadmap = st.button("🚀 Generate / Refresh Roadmap", type="primary")
            if btn_gen_roadmap:
                with st.spinner("Generating personalized learning roadmap from identified gaps..."):
                    roadmap_res = st.session_state.agent.generate_personalized_roadmap(
                        st.session_state.learner_profile, st.session_state.skill_gap_report
                    )
                    if roadmap_res["success"]:
                        st.session_state.learning_roadmap = roadmap_res["roadmap"]
                    else:
                        st.error(f"Roadmap generation failed: {roadmap_res['error']}")

            render_roadmap_display(st.session_state.learning_roadmap)

    with tab4:
        st.markdown("### 🧪 Practice Lab & AI Evaluator")
        st.caption("Test your understanding. EduPath AI evaluates your answer strictly and adapts your roadmap based on performance.")
        
        available_skills = []
        if profile_analyzed and st.session_state.learning_roadmap:
            if hasattr(st.session_state.learning_roadmap, "generated_from_gaps") and st.session_state.learning_roadmap.generated_from_gaps:
                for s in st.session_state.learning_roadmap.generated_from_gaps:
                    if s and s not in available_skills and not s.lower().startswith("missing knowledge") and "remedial" not in s.lower():
                        available_skills.append(s)

            if not available_skills:
                for w in st.session_state.learning_roadmap.weeks:
                    if "remedial" not in w.title.lower():
                        for s in w.skills_targeted:
                            if s and s not in available_skills and not s.lower().startswith("missing knowledge") and "remedial" not in s.lower():
                                available_skills.append(s)

        if not available_skills:
            available_skills = ["Vector Databases", "Prompt Engineering", "Retrieval-Augmented Generation (RAG)", "Deep Learning Architectures"]

        selected_skill = st.selectbox(
            "Select Skill to Practice:",
            options=available_skills,
            index=0
        )

        if selected_skill != st.session_state.current_practice_skill or not st.session_state.current_practice_task:
            st.session_state.current_practice_skill = selected_skill
            with st.spinner(f"Generating practice task for '{selected_skill}'..."):
                task_res = st.session_state.agent.create_practice_task(
                    st.session_state.learning_roadmap,
                    st.session_state.learner_profile,
                    selected_skill=selected_skill
                )
                if task_res["success"]:
                    st.session_state.current_practice_task = task_res["task"]

        task = st.session_state.current_practice_task
        
        if task:
            st.markdown("<div class='ep-card'>", unsafe_allow_html=True)
            st.markdown(f"<div class='ep-card-title'>Practice Challenge: {task.title}</div>", unsafe_allow_html=True)
            
            col_info1, col_info2, col_info3 = st.columns(3)
            with col_info1:
                st.markdown(f"**Target Skill:** `:blue[{task.skill}]`")
            with col_info2:
                st.markdown(f"**Topic Focus:** `{task.topic}`")
            with col_info3:
                st.markdown(f"**Difficulty Level:** `{task.difficulty}`")

            st.info(f"📋 **Instructions:**\n\n{task.instructions}")
            st.markdown("</div>", unsafe_allow_html=True)

            # Task-Aware Demo Shortcuts
            demo_weak, demo_strong = get_task_aware_demo_answers(task)

            st.markdown("#### ✍️ Your Submission")
            col_demo1, col_demo2 = st.columns(2)
            with col_demo1:
                if st.button("💡 Demo: Fill Incomplete Answer"):
                    st.session_state.demo_text_input = demo_weak
            with col_demo2:
                if st.button("✅ Demo: Fill Strong Answer"):
                    st.session_state.demo_text_input = demo_strong

            default_input = st.session_state.get("demo_text_input", "")
            user_answer = st.text_area("Type your technical response below:", value=default_input, height=180)

            btn_eval = st.button("✨ Submit for AI Evaluation", type="primary")

            if btn_eval:
                if not user_answer or len(user_answer.strip()) < 5:
                    st.error("Please enter a response before submitting.")
                else:
                    with st.spinner("Gemini Agent evaluating submission strictly against task criteria..."):
                        eval_res = st.session_state.agent.evaluate_and_adapt(
                            task=task,
                            user_submission=user_answer,
                            current_roadmap=st.session_state.learning_roadmap
                        )

                    if eval_res["success"]:
                        st.session_state.latest_evaluation = eval_res["evaluation"]
                        st.session_state.latest_adaptation = eval_res
                        
                        if eval_res["adapted"]:
                            st.session_state.learning_roadmap = eval_res["adapted_roadmap"]

            st.markdown("---")

            if st.session_state.latest_evaluation:
                ev = st.session_state.latest_evaluation
                st.markdown("### 📝 Evaluation Result")

                donut_eval_html = styles.render_donut_chart(ev.score, label="Evaluation Score", subtitle="Score Threshold: 70%", size=140)
                st.markdown(donut_eval_html, unsafe_allow_html=True)

                if ev.passed:
                    st.markdown(
                        f"""
                        <div class="eval-card-pass">
                            <div style="color: #34D399; font-weight: 800; font-size: 20px;">✓ PASSED EVALUATION</div>
                            <div style="color: #F3F4F6; font-size: 15px; font-weight: 600; margin-top: 4px;">Strong Technical Understanding Demonstrated (Score &ge; 70%)</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f"""
                        <div class="eval-card-fail">
                            <div style="color: #FBBF24; font-weight: 800; font-size: 20px;">⚠️ NEEDS IMPROVEMENT</div>
                            <div style="color: #F3F4F6; font-size: 15px; font-weight: 600; margin-top: 4px;">Conceptual Gap Detected (Score &lt; 70%)</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                c_wk, c_act = st.columns(2)
                with c_wk:
                    if ev.detected_weakness:
                        st.warning(f"**Detected Weakness:** {ev.detected_weakness}")
                    else:
                        st.success("**Weakness Detected:** None")
                with c_act:
                    st.info(f"**Recommended Action:** {ev.recommended_action}")

                st.info(f"💡 **AI Evaluator Feedback:**\n\n{ev.feedback}")

                if st.session_state.latest_adaptation and st.session_state.latest_adaptation["adapted"]:
                    ad = st.session_state.latest_adaptation
                    st.markdown(
                        f"""
                        <div class="adaptation-alert-banner">
                            <div style="font-size: 28px;">🤖</div>
                            <div>
                                <div style="font-weight: 800; color: #EF4444; font-size: 16px;">EDUPATH AI ADAPTED YOUR LEARNING PLAN</div>
                                <div style="color: #F3F4F6; font-size: 14px; margin-top: 4px;">
                                    Because your evaluation score ({ev.score}%) fell below 70%, EduPath detected a key weakness in <b>{ad['weakness']}</b>.<br/>
                                    <b>ACTION TAKEN:</b> A targeted remedial module (<i>Remedial Focus: {ad['weakness']}</i>) has been dynamically inserted into your roadmap.
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.info("👉 Switch to the **🗺️ Adaptive Roadmap** tab to view your updated learning plan.")

if __name__ == "__main__":
    main()
