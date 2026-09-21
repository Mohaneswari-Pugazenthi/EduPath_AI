import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.models import LearnerProfile, SkillGapReport, PrioritizedGap
from tools.roadmap_generator import generate_roadmap, build_fallback_roadmap

def test_fallback_roadmap_generation():
    profile = LearnerProfile(
        name="Alex Johnson",
        technical_skills=["Python", "SQL"],
        tools_and_technologies=["Git"]
    )
    
    gap_report = SkillGapReport(
        target_role="AI Engineer",
        acquired_core_skills=["Python"],
        missing_core_skills=["LLM Application Development", "Prompt Engineering", "RAG", "Vector Databases"],
        acquired_supporting_skills=["Git"],
        missing_supporting_skills=["REST APIs", "Data Preprocessing"],
        technology_gaps=["LangChain", "Pinecone"],
        prioritized_gaps=[
            PrioritizedGap(skill="LLM Application Development", priority="Critical", category="Core Skill"),
            PrioritizedGap(skill="Vector Databases", priority="Critical", category="Core Skill"),
        ],
        readiness_percentage=25.0,
        gap_summary="Test gap summary"
    )
    
    roadmap = build_fallback_roadmap(profile, gap_report, duration_weeks=4)
    assert roadmap.target_role == "AI Engineer"
    assert len(roadmap.weeks) == 4
    assert roadmap.readiness_score_before == 25.0
    
    # Verify that Week 1 targets missing core skills, not Python basics
    w1 = roadmap.weeks[0]
    assert w1.week_number == 1
    assert "LLM Application Development" in w1.skills_targeted or "Prompt Engineering" in w1.skills_targeted
    print("[PASS] Fallback roadmap generation test passed!")

def test_generate_roadmap_wrapper():
    profile = LearnerProfile(name="Test User", technical_skills=["Python"])
    gap_report = SkillGapReport(
        target_role="Machine Learning Engineer",
        acquired_core_skills=["Python"],
        missing_core_skills=["PyTorch", "Deep Learning", "MLOps"],
        acquired_supporting_skills=[],
        missing_supporting_skills=["Linux"],
        technology_gaps=["Docker", "MLflow"],
        prioritized_gaps=[],
        readiness_percentage=20.0,
        gap_summary="ML gap summary"
    )
    
    res = generate_roadmap(profile, gap_report, duration_weeks=4)
    assert res["success"] is True
    roadmap = res["roadmap"]
    assert len(roadmap.weeks) == 4
    assert roadmap.target_role == "Machine Learning Engineer"
    print("[PASS] Generate roadmap wrapper test passed!")

if __name__ == "__main__":
    test_fallback_roadmap_generation()
    test_generate_roadmap_wrapper()
    print("ALL STAGE 4 UNIT TESTS PASSED!")
