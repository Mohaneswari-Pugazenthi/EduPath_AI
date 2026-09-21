import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.models import LearnerProfile, Project
from tools.gap_analyzer import analyze_skill_gaps

def test_high_matching_learner():
    profile = LearnerProfile(
        name="AI Engineer Prospect",
        technical_skills=["Python", "LLM Application Development", "Prompt Engineering", "Retrieval-Augmented Generation (RAG)", "Vector Databases"],
        tools_and_technologies=["LangChain", "LlamaIndex", "FastAPI", "Git & Version Control", "REST APIs"],
        projects=[Project(title="RAG Bot", technologies=["Python", "ChromaDB"])]
    )
    
    report = analyze_skill_gaps(profile, "AI Engineer")
    assert report.target_role == "AI Engineer"
    assert "Python" in report.acquired_core_skills
    assert "Prompt Engineering" in report.acquired_core_skills
    assert report.readiness_percentage >= 70.0
    print(f"[PASS] High matching test passed! Score: {report.readiness_percentage}%")

def test_low_matching_learner():
    profile = LearnerProfile(
        name="Beginner Learner",
        technical_skills=["HTML", "CSS"],
        tools_and_technologies=["Git"],
        projects=[]
    )
    
    report = analyze_skill_gaps(profile, "AI Engineer")
    assert len(report.acquired_core_skills) == 0
    assert report.readiness_percentage < 15.0
    assert len(report.missing_core_skills) == 6
    print(f"[PASS] Low matching test passed! Score: {report.readiness_percentage}%")

def test_partial_matching_and_normalization():
    profile = LearnerProfile(
        name="Data Analyst Switching to Data Scientist",
        technical_skills=["Python", "SQL", "Exploratory Data Analysis (EDA)"],
        tools_and_technologies=["Pandas", "NumPy", "Jupyter Notebooks", "PostgreSQL"],
        projects=[]
    )
    
    report = analyze_skill_gaps(profile, "Data Scientist")
    assert "Python" in report.acquired_core_skills
    assert "Machine Learning Algorithms" in report.missing_core_skills
    assert 20.0 <= report.readiness_percentage <= 80.0
    print(f"[PASS] Partial matching test passed! Score: {report.readiness_percentage}%")

def test_gap_prioritization():
    profile = LearnerProfile(
        name="Test Learner",
        technical_skills=["Python"],
        tools_and_technologies=[],
        projects=[]
    )
    report = analyze_skill_gaps(profile, "Machine Learning Engineer")
    critical_gaps = [g for g in report.prioritized_gaps if g.priority == "Critical"]
    assert len(critical_gaps) > 0
    assert all(g.category == "Core Skill" for g in critical_gaps)
    print(f"[PASS] Prioritization test passed! Critical Gaps Count: {len(critical_gaps)}")

if __name__ == "__main__":
    test_high_matching_learner()
    test_low_matching_learner()
    test_partial_matching_and_normalization()
    test_gap_prioritization()
    print("ALL STAGE 3 UNIT TESTS PASSED!")
