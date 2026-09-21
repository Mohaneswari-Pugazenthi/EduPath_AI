import json
from typing import Dict, Any, Optional
from core.models import LearnerProfile, SkillGapReport, LearningRoadmap, WeeklyPlan

def build_fallback_roadmap(
    learner_profile: LearnerProfile,
    skill_gap_report: SkillGapReport,
    duration_weeks: int = 4
) -> LearningRoadmap:
    """
    Build a deterministic, personalized 4-week roadmap directly from identified gaps
    when Gemini API is unavailable or returns an error.
    """
    all_gaps = (
        skill_gap_report.missing_core_skills +
        skill_gap_report.missing_supporting_skills +
        skill_gap_report.technology_gaps
    )
    if not all_gaps:
        all_gaps = ["Advanced Topics & System Optimization"]

    target_role = skill_gap_report.target_role
    weeks_list = []
    
    # Partition gaps across 4 weeks
    core_gaps = skill_gap_report.missing_core_skills or ["Core Role Competencies"]
    supp_gaps = skill_gap_report.missing_supporting_skills or ["Supporting Competencies"]
    tool_gaps = skill_gap_report.technology_gaps or ["Relevant Tools"]

    # Week 1: Foundational Critical Core Gaps
    w1_skills = core_gaps[:2]
    w1_name = w1_skills[0] if w1_skills else "Core Skill"
    weeks_list.append(WeeklyPlan(
        week_number=1,
        title=f"Core Foundations: {', '.join(w1_skills[:1])}",
        learning_objectives=[f"Master foundational principles of {s}" for s in w1_skills],
        skills_targeted=w1_skills,
        topics=[f"Introduction to {w1_name}", f"Core mechanics & implementation of {w1_name}", "Hands-on exercises"],
        estimated_hours=9,
        practice_task=f"Build a standalone working demo implementing {w1_name}.",
        resource_recommendations=[f"Official documentation for {s}" for s in w1_skills] + [f"Google {w1_name} crash course"],
        expected_outcome=f"Working knowledge and practical implementation of {', '.join(w1_skills)}."
    ))

    # Week 2: Advanced Core Gaps & Dependencies
    w2_skills = core_gaps[2:4] if len(core_gaps) > 2 else core_gaps[:1]
    w2_name = w2_skills[0] if w2_skills else "Advanced Core Skill"
    weeks_list.append(WeeklyPlan(
        week_number=2,
        title=f"Advanced Core Concepts: {', '.join(w2_skills[:1])}",
        learning_objectives=[f"Develop end-to-end expertise in {s}" for s in w2_skills],
        skills_targeted=w2_skills,
        topics=[f"{s} architectural patterns" for s in w2_skills] + ["Performance optimization", "Error handling"],
        estimated_hours=10,
        practice_task=f"Create a mini-project integrating {w2_name} with python backend.",
        resource_recommendations=[f"Deep dive tutorial on {s}" for s in w2_skills] + ["GitHub reference repositories"],
        expected_outcome=f"Production-ready understanding of {', '.join(w2_skills)}."
    ))

    # Week 3: Supporting Skills & Workflow
    w3_skills = supp_gaps[:3]
    w3_name = w3_skills[0] if w3_skills else "Supporting Skill"
    weeks_list.append(WeeklyPlan(
        week_number=3,
        title=f"Supporting Competencies: {', '.join(w3_skills[:1])}",
        learning_objectives=[f"Integrate {s} into workflow" for s in w3_skills],
        skills_targeted=w3_skills,
        topics=[f"Best practices for {s}" for s in w3_skills] + ["System integration"],
        estimated_hours=8,
        practice_task=f"Implement workflow enhancements using {w3_name}.",
        resource_recommendations=[f"{s} best practices guide" for s in w3_skills],
        expected_outcome=f"Seamless application of {', '.join(w3_skills)}."
    ))

    # Week 4: Tool Mastery & Capstone Integration
    w4_skills = tool_gaps[:3]
    w4_name = w4_skills[0] if w4_skills else "Tool Stack"
    weeks_list.append(WeeklyPlan(
        week_number=4,
        title=f"Tool Stack & Capstone Project: {', '.join(w4_skills[:1])}",
        learning_objectives=[f"Master {s} tool stack" for s in w4_skills] + ["Build capstone project"],
        skills_targeted=w4_skills,
        topics=[f"{s} configuration & deployment" for s in w4_skills] + ["Capstone project synthesis"],
        estimated_hours=10,
        practice_task=f"Build and deploy a capstone project targeting {target_role} requirements.",
        resource_recommendations=[f"{s} official developer documentation" for s in w4_skills],
        expected_outcome=f"Portfolio capstone project demonstrating readiness for {target_role}."
    ))

    return LearningRoadmap(
        target_role=target_role,
        duration_weeks=4,
        readiness_score_before=skill_gap_report.readiness_percentage,
        weeks=weeks_list,
        generated_from_gaps=all_gaps[:6],
        summary=f"Personalized 4-week learning path designed to bridge your {len(all_gaps)} identified skill gaps for {target_role}."
    )

def generate_roadmap(
    learner_profile: LearnerProfile,
    skill_gap_report: SkillGapReport,
    duration_weeks: int = 4,
    gemini_client: Optional[Any] = None
) -> Dict[str, Any]:
    """
    Generate a personalized 4-week learning roadmap targeting the learner's specific gaps.
    
    Returns:
        dict: {
            "success": bool,
            "roadmap": LearningRoadmap or None,
            "error": str or None
        }
    """
    if not learner_profile:
        return {"success": False, "roadmap": None, "error": "Learner profile is missing."}
    if not skill_gap_report:
        return {"success": False, "roadmap": None, "error": "Skill gap report is missing."}

    # Attempt Gemini generation if client is available
    if gemini_client and gemini_client.is_configured():
        prompt = f"""
You are an expert technical curriculum designer creating a personalized {duration_weeks}-week learning roadmap.

STRICT PERSONALIZATION RULES:
1. Target Role: '{skill_gap_report.target_role}'
2. Learner's Baseline Readiness Score: {skill_gap_report.readiness_percentage}%
3. Already Acquired Skills (DO NOT TEACH THESE): {skill_gap_report.acquired_core_skills + skill_gap_report.acquired_supporting_skills}
4. MISSING SKILLS TO TARGET IN THIS ROADMAP:
   - Missing Core Skills (Critical): {skill_gap_report.missing_core_skills}
   - Missing Supporting Skills (Important): {skill_gap_report.missing_supporting_skills}
   - Technology Gaps: {skill_gap_report.technology_gaps}

DESIGN REQUIREMENTS:
- Create exactly {duration_weeks} weekly plans (week_number 1 through {duration_weeks}).
- Place Critical Core Skills in Week 1 and Week 2.
- Place Important Supporting Skills in Week 3.
- Place Technology Gaps & Capstone Project in Week 4.
- DO NOT waste time teaching beginner concepts that the learner already possesses (e.g. if they know Python, start directly with missing topics).
- Keep estimated_hours realistic (8-10 hours per week).
- For resource_recommendations, provide 2-3 specific search queries or official documentation titles (DO NOT generate fake web URLs).

Generate a complete structured JSON matching the LearningRoadmap schema.
"""
        try:
            response, err = gemini_client._generate_with_fallback(prompt, LearningRoadmap)
            if response:
                parsed_roadmap = None
                if hasattr(response, "parsed") and response.parsed is not None:
                    parsed_roadmap = response.parsed
                    if isinstance(parsed_roadmap, dict):
                        parsed_roadmap = LearningRoadmap.model_validate(parsed_roadmap)
                elif response.text:
                    parsed_roadmap = LearningRoadmap.model_validate_json(response.text)

                if parsed_roadmap:
                    return {"success": True, "roadmap": parsed_roadmap, "error": None}
        except Exception as e:
            print(f"Gemini roadmap generation fallback triggered: {e}")

    # Fallback to deterministic personalized roadmap if Gemini is unconfigured or fails
    fallback_roadmap = build_fallback_roadmap(learner_profile, skill_gap_report, duration_weeks)
    return {"success": True, "roadmap": fallback_roadmap, "error": None}
