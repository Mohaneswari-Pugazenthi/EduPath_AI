import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.gemini_client import GeminiClient
from core.agent import EduPathAgent
from core.models import LearnerProfile, Project

def run_stage3_end_to_end():
    print("--- Stage 3 End-to-End Verification ---")
    client = GeminiClient()
    agent = EduPathAgent(client)
    
    # Create sample Learner Profile targeting AI Engineer
    profile = LearnerProfile(
        name="Alex Dev",
        current_roles=["Junior Python Developer"],
        years_of_experience=2.0,
        technical_skills=["Python", "REST APIs", "SQL", "Git"],
        tools_and_technologies=["FastAPI", "Docker", "VS Code", "PostgreSQL"],
        projects=[Project(title="API Gateway", technologies=["Python", "FastAPI"])]
    )
    
    target_role = "AI Engineer"
    print(f"Target Role: {target_role}")
    
    result = agent.perform_skill_gap_analysis(profile, target_role)
    assert result["success"] is True
    report = result["report"]
    
    print(f"[SUCCESS] Target Role: {report.target_role}")
    print(f"[SUCCESS] Readiness Percentage: {report.readiness_percentage}%")
    print(f"[SUCCESS] Acquired Core: {report.acquired_core_skills}")
    print(f"[SUCCESS] Missing Core (Critical): {report.missing_core_skills}")
    print(f"[SUCCESS] Missing Supporting (Important): {report.missing_supporting_skills}")
    print(f"[SUCCESS] Technology Gaps: {report.technology_gaps}")
    print(f"[SUCCESS] AI Summary: {report.gap_summary}")
    print("Stage 3 verification completed successfully!")

if __name__ == "__main__":
    run_stage3_end_to_end()
