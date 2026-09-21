import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.gemini_client import GeminiClient
from core.agent import EduPathAgent
from core.models import LearnerProfile, Project

def run_stage4_end_to_end():
    print("--- Stage 4 End-to-End Verification ---")
    client = GeminiClient()
    agent = EduPathAgent(client)
    
    # Candidate profile targeting AI Engineer
    profile = LearnerProfile(
        name="Alex Johnson",
        current_roles=["Python Developer"],
        years_of_experience=3.0,
        technical_skills=["Python", "SQL", "Git"],
        tools_and_technologies=["FastAPI", "PostgreSQL", "Docker"],
        projects=[Project(title="API Gateway", technologies=["Python", "FastAPI"])]
    )
    
    target_role = "AI Engineer"
    
    # Step 1: Skill Gap Analysis
    gap_res = agent.perform_skill_gap_analysis(profile, target_role)
    assert gap_res["success"] is True
    gap_report = gap_res["report"]
    print(f"[SUCCESS] Baseline Readiness Score: {gap_report.readiness_percentage}%")
    print(f"[SUCCESS] Identified Critical Gaps: {gap_report.missing_core_skills}")
    
    # Step 2: Personalized Roadmap Generation
    roadmap_res = agent.generate_personalized_roadmap(profile, gap_report, duration_weeks=4)
    assert roadmap_res["success"] is True
    roadmap = roadmap_res["roadmap"]
    
    print(f"[SUCCESS] Target Role: {roadmap.target_role}")
    print(f"[SUCCESS] Roadmap Duration: {roadmap.duration_weeks} Weeks")
    print(f"[SUCCESS] Weeks Count: {len(roadmap.weeks)}")
    print(f"[SUCCESS] Summary: {roadmap.summary}")
    
    for w in roadmap.weeks:
        print(f"\n--- Week {w.week_number}: {w.title} ---")
        print(f"Targeted Skills: {w.skills_targeted}")
        print(f"Learning Objectives: {w.learning_objectives}")
        print(f"Estimated Hours: {w.estimated_hours}")
        print(f"Practice Task: {w.practice_task}")
        print(f"Resource Recommendations: {w.resource_recommendations}")

    print("\nStage 4 end-to-end verification completed successfully!")

if __name__ == "__main__":
    run_stage4_end_to_end()
