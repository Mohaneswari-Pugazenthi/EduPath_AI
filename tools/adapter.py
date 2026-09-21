import copy
from typing import Dict, Any
from core.models import LearningRoadmap, WeeklyPlan, EvaluationReport

def adapt_roadmap(
    current_roadmap: LearningRoadmap,
    evaluation: EvaluationReport
) -> Dict[str, Any]:
    """
    Dynamically adapt the learning roadmap based on practice evaluation feedback.
    
    If evaluation.passed is True (score >= 70):
        Roadmap remains unchanged.
        
    If evaluation.passed is False (score < 70):
        Inserts exactly ONE targeted remedial module for the detected weakness.
        Caps at maximum 1 remedial module per skill to prevent infinite loops.
    """
    if not current_roadmap:
        return {
            "adapted": False,
            "roadmap": None,
            "weakness": None,
            "message": "No active roadmap to adapt."
        }

    # Case 1: Learner passed evaluation (score >= 70)
    if evaluation.passed:
        return {
            "adapted": False,
            "roadmap": current_roadmap,
            "weakness": None,
            "message": f"Great job! Score ({evaluation.score}%) passed threshold. Roadmap continues as planned."
        }

    # Case 2: Learner failed evaluation (score < 70) -> Trigger Adaptation
    weakness = evaluation.detected_weakness or "Core Concept Mechanics"

    # Clone roadmap to preserve state immutability
    adapted_roadmap = copy.deepcopy(current_roadmap)

    # Check for existing remedial module for this weakness to prevent infinite duplicates
    existing_remedial = [
        w for w in adapted_roadmap.weeks
        if f"remedial" in w.title.lower() or weakness.lower() in w.title.lower()
    ]
    if len(existing_remedial) >= 1:
        return {
            "adapted": False,
            "roadmap": current_roadmap,
            "weakness": weakness,
            "message": f"Remedial module for '{weakness}' is already present in your roadmap. Maximum 1 remedial module cap reached."
        }

    # Identify matching predefined skill from roadmap
    target_skill = None
    if hasattr(current_roadmap, "generated_from_gaps") and current_roadmap.generated_from_gaps:
        for s in current_roadmap.generated_from_gaps:
            if s.lower() in weakness.lower() or weakness.lower() in s.lower():
                target_skill = s
                break
    if not target_skill:
        for w in current_roadmap.weeks:
            if "remedial" not in w.title.lower():
                for s in w.skills_targeted:
                    if s.lower() in weakness.lower() or weakness.lower() in s.lower():
                        target_skill = s
                        break
            if target_skill:
                break
    if not target_skill:
        if hasattr(current_roadmap, "generated_from_gaps") and current_roadmap.generated_from_gaps:
            target_skill = current_roadmap.generated_from_gaps[0]
        else:
            target_skill = "Vector Databases"

    # Construct the targeted remedial module
    remedial_week = WeeklyPlan(
        week_number=1,  # Temporary marker, re-indexed below
        title=f"Remedial Focus: {weakness}",
        learning_objectives=[
            f"Strengthen foundational understanding of {weakness}",
            "Bridge diagnostic gaps identified during practice evaluation"
        ],
        skills_targeted=[target_skill],
        topics=[
            f"{target_skill} core mechanics & representation",
            "Step-by-step diagnostic breakdown & intuition",
            "Guided remedial practice exercise"
        ],
        estimated_hours=4,
        practice_task=f"Complete targeted diagnostic exercise on {weakness} principles.",
        resource_recommendations=[
            f"Refresher guide: {target_skill} fundamentals",
            f"Interactive breakdown: Understanding {target_skill}"
        ],
        expected_outcome=f"Solidified mastery of {target_skill} before advancing to complex topics."
    )

    # Insert remedial module right after Week 1 (or index 1)
    insert_pos = 1 if len(adapted_roadmap.weeks) >= 1 else 0
    adapted_roadmap.weeks.insert(insert_pos, remedial_week)

    # Re-index week numbers cleanly (e.g. 1, 2, 3, 4, 5 or 1, 1.5, 2...)
    # Using decimal or clear labeling
    for idx, w in enumerate(adapted_roadmap.weeks):
        if "remedial" in w.title.lower():
            w.week_number = idx + 1
        else:
            w.week_number = idx + 1

    adapted_roadmap.duration_weeks = len(adapted_roadmap.weeks)
    adapted_roadmap.summary = f"⚠️ ROADMAP ADAPTED: Added targeted remedial module for '{weakness}'. {current_roadmap.summary}"

    return {
        "adapted": True,
        "roadmap": adapted_roadmap,
        "weakness": weakness,
        "message": f"EduPath Agent dynamically adapted your roadmap by inserting a remedial module for '{weakness}'!"
    }
