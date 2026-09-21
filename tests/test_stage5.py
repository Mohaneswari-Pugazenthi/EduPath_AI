import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.models import LearnerProfile, LearningRoadmap, WeeklyPlan, PracticeTask, EvaluationReport
from tools.practice_generator import build_fallback_practice_task
from tools.evaluator import evaluate_submission_fallback
from tools.adapter import adapt_roadmap

def create_mock_roadmap():
    return LearningRoadmap(
        target_role="AI Engineer",
        readiness_score_before=25.0,
        weeks=[
            WeeklyPlan(
                week_number=1,
                title="Vector Databases & Similarity Search",
                learning_objectives=["Understand Vector Databases"],
                skills_targeted=["Vector Databases"],
                topics=["Cosine Similarity", "Embeddings Indexing"],
                estimated_hours=8,
                practice_task="Explain vector databases and similarity search",
                resource_recommendations=["Guide"],
                expected_outcome="Outcome"
            ),
            WeeklyPlan(
                week_number=2,
                title="RAG Systems Architecture",
                learning_objectives=["Build RAG"],
                skills_targeted=["RAG"],
                topics=["Chunking", "Retrieval"],
                estimated_hours=10,
                practice_task="Build RAG pipeline",
                resource_recommendations=["RAG Guide"],
                expected_outcome="RAG System"
            )
        ],
        generated_from_gaps=["Vector Databases", "RAG"],
        summary="Mock roadmap for testing"
    )

def test_a_strong_answer():
    """TEST A: Strong answer aligned with the task skill."""
    roadmap = create_mock_roadmap()
    task = build_fallback_practice_task(roadmap, 0, selected_skill="Vector Databases")
    
    strong_answer = (
        "Vector databases store high-dimensional embedding vectors representing semantic content. "
        "They utilize vector representation and similarity search techniques like cosine similarity "
        "to perform fast nearest-neighbor retrieval of related context for LLM queries."
    )
    
    eval_report = evaluate_submission_fallback(task, strong_answer)
    assert eval_report.score >= 70.0
    assert eval_report.passed is True
    assert eval_report.detected_weakness is None
    
    adaptation = adapt_roadmap(roadmap, eval_report)
    assert adaptation["adapted"] is False
    assert len(adaptation["roadmap"].weeks) == 2
    print(f"[PASS] TEST A (Strong Answer) passed! Score: {eval_report.score}%, Passed: {eval_report.passed}")

def test_b_weak_answer():
    """TEST B: Incomplete/weak answer for the task skill."""
    roadmap = create_mock_roadmap()
    task = build_fallback_practice_task(roadmap, 0, selected_skill="Vector Databases")
    
    weak_answer = "Vector databases are used to compare data."
    
    eval_report = evaluate_submission_fallback(task, weak_answer)
    assert eval_report.score < 70.0
    assert eval_report.passed is False
    assert eval_report.detected_weakness is not None
    
    adaptation = adapt_roadmap(roadmap, eval_report)
    assert adaptation["adapted"] is True
    adapted_rm = adaptation["roadmap"]
    assert len(adapted_rm.weeks) == 3
    assert "Remedial Focus" in adapted_rm.weeks[1].title
    print(f"[PASS] TEST B (Weak Answer) passed! Score: {eval_report.score}%, Weakness: {eval_report.detected_weakness}")

def test_c_unrelated_answer():
    """TEST C: Unrelated answer (e.g. submitting Python answer for Vector Databases task)."""
    roadmap = create_mock_roadmap()
    task = build_fallback_practice_task(roadmap, 0, selected_skill="Vector Databases")
    
    unrelated_answer = "Python is a popular programming language used for web development and machine learning."
    
    eval_report = evaluate_submission_fallback(task, unrelated_answer)
    assert eval_report.score < 70.0
    assert eval_report.passed is False
    assert eval_report.detected_weakness is not None
    
    adaptation = adapt_roadmap(roadmap, eval_report)
    assert adaptation["adapted"] is True
    print(f"[PASS] TEST C (Unrelated Answer) passed! Score: {eval_report.score}%, Weakness: {eval_report.detected_weakness}")

def test_d_repeated_weakness():
    """TEST D: Repeated weak answer for the same skill (Max 1 remedial module cap)."""
    roadmap = create_mock_roadmap()
    task = build_fallback_practice_task(roadmap, 0, selected_skill="Vector Databases")
    weak_answer = "I don't know."
    
    eval_report = evaluate_submission_fallback(task, weak_answer)
    
    # 1st adaptation: inserts remedial module
    adaptation1 = adapt_roadmap(roadmap, eval_report)
    assert adaptation1["adapted"] is True
    adapted_rm1 = adaptation1["roadmap"]
    assert len(adapted_rm1.weeks) == 3
    
    # 2nd adaptation: should NOT add a duplicate remedial module
    adaptation2 = adapt_roadmap(adapted_rm1, eval_report)
    assert adaptation2["adapted"] is False
    assert len(adaptation2["roadmap"].weeks) == 3
    print(f"[PASS] TEST D (Repeated Weakness Cap) passed! Max 1 remedial module enforced.")

if __name__ == "__main__":
    test_a_strong_answer()
    test_b_weak_answer()
    test_c_unrelated_answer()
    test_d_repeated_weakness()
    print("ALL MANDATORY STAGE 5 UNIT TESTS (A, B, C, D) PASSED!")
