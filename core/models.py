from typing import List, Optional
from pydantic import BaseModel, Field

class Project(BaseModel):
    title: str = Field(description="Name or title of the project")
    description: Optional[str] = Field(default="", description="Brief summary of the project and tech stack used")
    technologies: List[str] = Field(default_factory=list, description="Technologies/tools used in this project")

class Education(BaseModel):
    degree: str = Field(description="Degree name or educational qualification")
    institution: Optional[str] = Field(default="", description="School, college, or university name")
    year: Optional[str] = Field(default="", description="Graduation year or completion timeline")

class Certification(BaseModel):
    title: str = Field(description="Certification title")
    issuer: Optional[str] = Field(default="", description="Issuing body or organization")

class LearnerProfile(BaseModel):
    name: Optional[str] = Field(default="Learner", description="Full name of the candidate")
    current_roles: List[str] = Field(default_factory=list, description="Current or recent job titles/roles")
    years_of_experience: Optional[float] = Field(default=None, description="Total estimated years of relevant work experience")
    technical_skills: List[str] = Field(default_factory=list, description="Core programming languages, frameworks, and technical domains")
    tools_and_technologies: List[str] = Field(default_factory=list, description="Software tools, platforms, databases, and libraries")
    projects: List[Project] = Field(default_factory=list, description="Key projects completed")
    education: List[Education] = Field(default_factory=list, description="Academic background")
    certifications: List[Certification] = Field(default_factory=list, description="Professional certifications or licenses")
    other_capabilities: List[str] = Field(default_factory=list, description="Other notable skills or non-technical capabilities")

class PrioritizedGap(BaseModel):
    skill: str = Field(description="Name of the missing skill or technology")
    priority: str = Field(description="Priority rating: Critical, Important, or Nice to Have")
    category: str = Field(description="Category: Core Skill, Supporting Skill, or Technology")

class SkillGapReport(BaseModel):
    target_role: str = Field(description="Selected target role benchmark")
    acquired_core_skills: List[str] = Field(default_factory=list, description="Core skills the learner possesses")
    missing_core_skills: List[str] = Field(default_factory=list, description="Core skills the learner lacks")
    acquired_supporting_skills: List[str] = Field(default_factory=list, description="Supporting skills the learner possesses")
    missing_supporting_skills: List[str] = Field(default_factory=list, description="Supporting skills the learner lacks")
    technology_gaps: List[str] = Field(default_factory=list, description="Tools or technologies missing from benchmark")
    prioritized_gaps: List[PrioritizedGap] = Field(default_factory=list, description="Ordered list of missing gaps with priority levels")
    readiness_percentage: float = Field(description="Deterministically computed readiness percentage (0 to 100)")
    gap_summary: str = Field(description="Natural-language summary of the learner's skill gap and next priorities")

class WeeklyPlan(BaseModel):
    week_number: int = Field(description="Sequential week number (e.g. 1, 2, 3, 4)")
    title: str = Field(description="Title of the week focus area (e.g. Foundation for Vector Embeddings)")
    learning_objectives: List[str] = Field(default_factory=list, description="Targeted learning goals for this week")
    skills_targeted: List[str] = Field(default_factory=list, description="Specific missing skills addressed this week")
    topics: List[str] = Field(default_factory=list, description="Core concepts and sub-topics to cover")
    estimated_hours: int = Field(default=8, description="Estimated study time in hours (typically 8-10 hrs)")
    practice_task: str = Field(description="Hands-on practice task or project prompt for the week")
    resource_recommendations: List[str] = Field(default_factory=list, description="Search queries or official documentation titles")
    expected_outcome: str = Field(description="Concrete deliverable or capability acquired by end of week")

class LearningRoadmap(BaseModel):
    target_role: str = Field(description="Target role for this learning roadmap")
    duration_weeks: int = Field(default=4, description="Total duration of the roadmap in weeks")
    readiness_score_before: float = Field(description="Baseline readiness score before starting the plan")
    weeks: List[WeeklyPlan] = Field(default_factory=list, description="List of 4 weekly learning plans")
    generated_from_gaps: List[str] = Field(default_factory=list, description="List of primary gap skills targeted in this plan")
    summary: str = Field(description="Brief summary of the 4-week learning journey")

class PracticeTask(BaseModel):
    task_id: str = Field(description="Unique task identifier, e.g. TASK_W1_01")
    skill: str = Field(description="Targeted skill or concept being tested from the roadmap")
    topic: str = Field(default="Core Concepts", description="Specific sub-topic or focus area within the skill")
    title: str = Field(description="Short title for the practice exercise")
    difficulty: str = Field(default="Intermediate", description="Difficulty level: Beginner, Intermediate, or Advanced")
    instructions: str = Field(description="Detailed instructions and question prompt for the learner")
    expected_concepts: List[str] = Field(default_factory=list, description="Key technical concepts expected in a complete response")
    evaluation_criteria: List[str] = Field(default_factory=list, description="Criteria used by AI evaluator to grade the answer")

class EvaluationReport(BaseModel):
    task_id: str = Field(description="Identifier of the evaluated task")
    score: float = Field(description="Evaluation score from 0.0 to 100.0")
    passed: bool = Field(description="True if score >= 70.0, else False")
    feedback: str = Field(description="Constructive AI feedback explaining the evaluation score")
    detected_weakness: Optional[str] = Field(default=None, description="Specific concept or weakness detected if score < 70")
    mastered_topics: List[str] = Field(default_factory=list, description="Concepts correctly understood and demonstrated")
    recommended_action: str = Field(description="Next recommended step for the learner")
