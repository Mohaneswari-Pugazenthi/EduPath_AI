import re
from typing import Optional, Any
from core.models import PracticeTask, EvaluationReport

def evaluate_submission_fallback(task: PracticeTask, user_submission: str) -> EvaluationReport:
    """Deterministic fallback evaluator comparing submission strictly against task.expected_concepts and task.skill."""
    text = user_submission.strip().lower() if user_submission else ""
    skill_clean = task.skill.strip().lower()
    
    # 1. Incomplete / empty answer
    if len(text) < 15 or "don't know" in text or "not sure" in text or "idk" in text:
        return EvaluationReport(
            task_id=task.task_id,
            score=20.0,
            passed=False,
            feedback=f"Incomplete answer. No technical explanation was provided for '{task.skill}'.",
            detected_weakness=f"Core fundamentals of {task.skill}",
            mastered_topics=[],
            recommended_action=f"Study foundational concepts of {task.skill} before retrying."
        )

    # 2. Check keyword alignment against expected_concepts and task skill
    matched_concepts = []
    missing_concepts = []
    
    for concept in task.expected_concepts:
        concept_clean = concept.strip().lower()
        words = [w for w in re.split(r'\W+', concept_clean) if len(w) > 2]
        if any(w in text for w in words):
            matched_concepts.append(concept)
        else:
            missing_concepts.append(concept)

    # Check if answer is completely off-topic
    skill_words = [w for w in re.split(r'\W+', skill_clean) if len(w) > 2]
    skill_mentioned = any(w in text for w in skill_words)

    if not skill_mentioned and len(matched_concepts) == 0:
        return EvaluationReport(
            task_id=task.task_id,
            score=10.0,
            passed=False,
            feedback=f"Unrelated submission. Your answer does not address the practice task for '{task.skill}'.",
            detected_weakness=f"{task.skill} mechanics and implementation",
            mastered_topics=[],
            recommended_action=f"Review the problem instructions and study '{task.skill}' concepts."
        )

    total_expected = max(len(task.expected_concepts), 1)
    match_ratio = len(matched_concepts) / total_expected
    raw_score = round(match_ratio * 100.0, 1)

    # Score threshold: >= 70% of expected concepts required for passing grade (score >= 70)
    if raw_score >= 70.0:
        return EvaluationReport(
            task_id=task.task_id,
            score=max(75.0, raw_score),
            passed=True,
            feedback=f"Excellent response! You clearly demonstrated technical understanding of {task.skill}.",
            detected_weakness=None,
            mastered_topics=matched_concepts,
            recommended_action="Proceed to the next module in your roadmap."
        )
    else:
        weakness = missing_concepts[0] if missing_concepts else f"{task.skill} core concepts"
        return EvaluationReport(
            task_id=task.task_id,
            score=min(60.0, max(25.0, raw_score)),
            passed=False,
            feedback=f"Your submission addresses some points but lacks key details regarding '{weakness}' for '{task.skill}'.",
            detected_weakness=weakness,
            mastered_topics=matched_concepts,
            recommended_action=f"Focus on strengthening your understanding of {weakness}."
        )

def evaluate_practice_submission(
    task: PracticeTask,
    user_submission: str,
    gemini_client: Optional[Any] = None
) -> EvaluationReport:
    """
    Evaluate user's text submission strictly against the provided PracticeTask (its skill, topic, and criteria).
    Enforces score >= 70 threshold for passing.
    """
    if not user_submission or len(user_submission.strip()) < 15:
        return EvaluationReport(
            task_id=task.task_id,
            score=20.0,
            passed=False,
            feedback=f"Incomplete answer. No technical explanation was provided for '{task.skill}'.",
            detected_weakness=f"Core principles of {task.skill}",
            mastered_topics=[],
            recommended_action=f"Study the foundational mechanics of {task.skill}."
        )

    if gemini_client and gemini_client.is_configured():
        prompt = f"""
You are an expert technical evaluator grading a student's conceptual response for a specific practice task.

MANDATORY EVALUATION RULES:
1. Evaluate ONLY how well the user's answer addresses the provided practice task for '{task.skill}' ({task.topic}).
2. Do NOT evaluate the answer against unrelated knowledge. If the student submits an answer about a completely different skill/topic than '{task.skill}', score it 0% and detect the weakness as missing knowledge of '{task.skill}'.
3. Be fair and encouraging for text-based responses: If the student demonstrates solid conceptual understanding of '{task.skill}' and addresses the expected concepts ({task.expected_concepts}), award a passing score >= 70.0 (e.g. 80-90%).
4. If score >= 70.0 -> set passed = True, detected_weakness = null.
5. If score < 70.0 -> set passed = False, provide a concise detected_weakness.

TASK DETAILS:
- Target Skill: {task.skill}
- Topic: {task.topic}
- Prompt / Question: {task.instructions}
- Expected Concepts: {task.expected_concepts}
- Evaluation Criteria: {task.evaluation_criteria}

STUDENT SUBMISSION:
---
{user_submission}
---

OUTPUT SPECIFICATION:
- score: float (0.0 to 100.0)
- passed: bool (True if score >= 70.0, else False)
- feedback: string (2-3 sentences explaining the grade)
- detected_weakness: string if score < 70.0, else null
- mastered_topics: list of strings
- recommended_action: string

Generate a complete structured JSON matching the EvaluationReport schema.
"""
        try:
            response, err = gemini_client._generate_with_fallback(prompt, EvaluationReport)
            if response:
                parsed_eval = None
                if hasattr(response, "parsed") and response.parsed is not None:
                    parsed_eval = response.parsed
                    if isinstance(parsed_eval, dict):
                        parsed_eval = EvaluationReport.model_validate(parsed_eval)
                elif response.text:
                    parsed_eval = EvaluationReport.model_validate_json(response.text)

                if parsed_eval:
                    parsed_eval.passed = (parsed_eval.score >= 70.0)
                    if not parsed_eval.passed and not parsed_eval.detected_weakness:
                        parsed_eval.detected_weakness = f"Application of {task.skill}"
                    elif parsed_eval.passed:
                        parsed_eval.detected_weakness = None
                    return parsed_eval
        except Exception as e:
            print(f"Gemini evaluator fallback triggered: {e}")

    return evaluate_submission_fallback(task, user_submission)
