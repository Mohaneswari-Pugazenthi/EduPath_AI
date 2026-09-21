from typing import Dict, Any, Optional
from core.gemini_client import GeminiClient
from core.models import LearnerProfile, SkillGapReport, LearningRoadmap, PracticeTask, EvaluationReport
from tools.document_parser import extract_text_from_pdf
from tools.gap_analyzer import analyze_skill_gaps
from tools.roadmap_generator import generate_roadmap
from tools.practice_generator import generate_practice_task
from tools.evaluator import evaluate_practice_submission
from tools.adapter import adapt_roadmap

class EduPathAgent:
    """Main Agent Orchestrator for EduPath."""

    def __init__(self, gemini_client: GeminiClient = None):
        self.gemini_client = gemini_client or GeminiClient()

    def get_agent_status(self) -> dict:
        """Returns the current state and status of the EduPath Agent."""
        gemini_status = self.gemini_client.get_status()
        return {
            "agent_name": "EduPath Orchestrator",
            "ready": gemini_status["client_initialized"],
            "gemini_status": gemini_status
        }

    def analyze_resume_and_build_profile(self, pdf_file: Any, target_role: str) -> Dict[str, Any]:
        """
        Stage 2 Tool: Parse PDF resume text and invoke Gemini to generate a structured LearnerProfile.
        """
        parser_result = extract_text_from_pdf(pdf_file)
        if not parser_result["success"]:
            return {
                "success": False,
                "profile": None,
                "target_role": target_role,
                "raw_text": "",
                "error": parser_result["error"]
            }

        resume_text = parser_result["text"]
        gemini_result = self.gemini_client.extract_learner_profile(resume_text)
        if not gemini_result["success"]:
            return {
                "success": False,
                "profile": None,
                "target_role": target_role,
                "raw_text": resume_text,
                "error": gemini_result["error"]
            }

        return {
            "success": True,
            "profile": gemini_result["profile"],
            "target_role": target_role,
            "raw_text": resume_text,
            "error": None
        }

    def perform_skill_gap_analysis(self, learner_profile: LearnerProfile, target_role: str) -> Dict[str, Any]:
        """
        Stage 3 Tool: Compare learner profile against target role benchmark.
        """
        try:
            report = analyze_skill_gaps(
                learner_profile=learner_profile,
                target_role=target_role,
                gemini_client=self.gemini_client
            )
            return {
                "success": True,
                "report": report,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "report": None,
                "error": f"Skill gap analysis failed: {str(e)}"
            }

    def generate_personalized_roadmap(
        self,
        learner_profile: LearnerProfile,
        skill_gap_report: SkillGapReport,
        duration_weeks: int = 4
    ) -> Dict[str, Any]:
        """
        Stage 4 Tool: Generate a personalized weekly learning roadmap.
        """
        try:
            res = generate_roadmap(
                learner_profile=learner_profile,
                skill_gap_report=skill_gap_report,
                duration_weeks=duration_weeks,
                gemini_client=self.gemini_client
            )
            return res
        except Exception as e:
            return {
                "success": False,
                "roadmap": None,
                "error": f"Roadmap generation failed: {str(e)}"
            }

    def create_practice_task(
        self,
        roadmap: LearningRoadmap,
        learner_profile: LearnerProfile,
        week_index: int = 0,
        selected_skill: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Stage 5 Tool: Generate a practice challenge for the selected skill/topic from the active roadmap.
        """
        try:
            task = generate_practice_task(
                roadmap=roadmap,
                learner_profile=learner_profile,
                week_index=week_index,
                selected_skill=selected_skill,
                gemini_client=self.gemini_client
            )
            return {
                "success": True,
                "task": task,
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "task": None,
                "error": f"Practice task generation failed: {str(e)}"
            }

    def evaluate_and_adapt(
        self,
        task: PracticeTask,
        user_submission: str,
        current_roadmap: LearningRoadmap
    ) -> Dict[str, Any]:
        """
        Stage 5 Core Agentic Loop: Evaluate practice submission strictly against task.skill and adapt roadmap dynamically.
        """
        try:
            # Step 1: Evaluate practice submission strictly against task criteria
            evaluation = evaluate_practice_submission(
                task=task,
                user_submission=user_submission,
                gemini_client=self.gemini_client
            )

            # Step 2: Trigger dynamic roadmap adaptation based on evaluation score & weakness
            adaptation_res = adapt_roadmap(
                current_roadmap=current_roadmap,
                evaluation=evaluation
            )

            return {
                "success": True,
                "evaluation": evaluation,
                "adapted": adaptation_res["adapted"],
                "adapted_roadmap": adaptation_res["roadmap"],
                "weakness": adaptation_res["weakness"],
                "message": adaptation_res["message"],
                "error": None
            }
        except Exception as e:
            return {
                "success": False,
                "evaluation": None,
                "adapted": False,
                "adapted_roadmap": current_roadmap,
                "weakness": None,
                "message": "",
                "error": f"Evaluation and adaptation loop failed: {str(e)}"
            }
