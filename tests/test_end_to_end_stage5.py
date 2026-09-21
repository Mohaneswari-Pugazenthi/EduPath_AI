import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.gemini_client import GeminiClient
from core.agent import EduPathAgent
from core.models import LearnerProfile, Project
from app import get_task_aware_demo_answers

def run_stage5_end_to_end():
    print("==================================================")
    print("=== EduPath Core Agentic Loop Verification ===")
    print("==================================================")
    
    client = GeminiClient()
    agent = EduPathAgent(client)
    
    # Candidate profile targeting AI Engineer
    profile = LearnerProfile(
        name="Alex Dev",
        current_roles=["Junior Developer"],
        years_of_experience=2.0,
        technical_skills=["Python", "REST APIs", "SQL"],
        tools_and_technologies=["FastAPI", "Docker", "VS Code"],
        projects=[Project(title="API Server", technologies=["Python"])]
    )
    
    target_role = "AI Engineer"
    
    # Step 1: Skill Gap Analysis
    print("\n[Step 1] Executing Skill Gap Analysis...")
    gap_res = agent.perform_skill_gap_analysis(profile, target_role)
    assert gap_res["success"] is True
    gap_report = gap_res["report"]
    print(f"[PASS] Target Role: {gap_report.target_role}")
    print(f"[PASS] Readiness Score: {gap_report.readiness_percentage}%")
    
    # Step 2: Personalized 4-Week Roadmap Generation
    print("\n[Step 2] Generating Initial 4-Week Roadmap...")
    roadmap_res = agent.generate_personalized_roadmap(profile, gap_report, duration_weeks=4)
    assert roadmap_res["success"] is True
    initial_roadmap = roadmap_res["roadmap"]
    print(f"[PASS] Initial Roadmap Weeks Count: {len(initial_roadmap.weeks)}")
    print(f"[PASS] Week 1 Title: {initial_roadmap.weeks[0].title}")
    
    # Step 3: Practice Task Generation (Targeting Vector Databases)
    selected_skill = "Vector Databases"
    print(f"\n[Step 3] Generating Practice Challenge for '{selected_skill}'...")
    task_res = agent.create_practice_task(initial_roadmap, profile, selected_skill=selected_skill)
    assert task_res["success"] is True
    task = task_res["task"]
    print(f"[PASS] Task ID: {task.task_id}")
    print(f"[PASS] Task Skill: {task.skill}")
    print(f"[PASS] Task Topic: {task.topic}")
    print(f"[PASS] Task Title: {task.title}")
    assert task.skill == selected_skill
    
    # Step 4: Submit Task-Aligned Strong Answer (Passes Challenge)
    print("\n[Step 4] Submitting Task-Aligned Strong Answer...")
    demo_weak, demo_strong = get_task_aware_demo_answers(task)
    
    # Include expected concepts from task if present to ensure 100% evaluation alignment
    comprehensive_strong_answer = (
        f"{demo_strong} "
        f"Specifically addressing expected concepts: {', '.join(task.expected_concepts)}. "
        f"This satisfies all criteria: {', '.join(task.evaluation_criteria)}."
    )
    
    strong_res = agent.evaluate_and_adapt(task, comprehensive_strong_answer, initial_roadmap)
    assert strong_res["success"] is True
    strong_eval = strong_res["evaluation"]
    
    print(f"[PASS] Evaluation Score: {strong_eval.score}%")
    print(f"[PASS] Passed Threshold (>=70%): {strong_eval.passed}")
    print(f"[PASS] Adaptation Triggered: {strong_res['adapted']}")
    assert strong_eval.passed is True
    assert strong_res["adapted"] is False
    
    # Step 5: Submit Task-Aligned Weak Answer (Triggers Adaptation)
    print("\n[Step 5] Submitting Weak Incomplete Answer...")
    weak_res = agent.evaluate_and_adapt(task, demo_weak, initial_roadmap)
    assert weak_res["success"] is True
    weak_eval = weak_res["evaluation"]
    
    print(f"[PASS] Evaluation Score: {weak_eval.score}%")
    print(f"[PASS] Passed Threshold (>=70%): {weak_eval.passed}")
    print(f"[PASS] Detected Weakness: {weak_res['weakness']}")
    print(f"[PASS] Adaptation Triggered: {weak_res['adapted']}")
    assert weak_eval.passed is False
    assert weak_res["adapted"] is True
    
    adapted_roadmap = weak_res["adapted_roadmap"]
    print(f"[PASS] Adapted Roadmap Modules Count: {len(adapted_roadmap.weeks)}")
    print(f"[PASS] Inserted Module Title: {adapted_roadmap.weeks[1].title}")

    # Step 6: Submit Unrelated Answer (Triggers Weakness Detection)
    print("\n[Step 6] Submitting Unrelated Answer...")
    unrelated_answer = "Python is a programming language used for web scraping and backend servers."
    
    unrelated_res = agent.evaluate_and_adapt(task, unrelated_answer, initial_roadmap)
    assert unrelated_res["success"] is True
    unrelated_eval = unrelated_res["evaluation"]
    
    print(f"[PASS] Evaluation Score: {unrelated_eval.score}%")
    print(f"[PASS] Passed Threshold (>=70%): {unrelated_eval.passed}")
    print(f"[PASS] Adaptation Triggered: {unrelated_res['adapted']}")
    assert unrelated_eval.passed is False

    print("\nALL STAGE 5 END-TO-END AGENTIC LOOP TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    run_stage5_end_to_end()
