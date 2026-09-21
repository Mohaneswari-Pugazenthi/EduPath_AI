import json
import os
import re
from typing import Dict, Any, List, Set, Optional
from core.models import LearnerProfile, SkillGapReport, PrioritizedGap

BENCHMARK_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "target_roles.json")

# Normalization mapping for common variations
ALIAS_MAP = {
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "py": "python",
    "js": "javascript",
    "ts": "typescript",
    "postgres": "postgresql",
    "mongo": "mongodb",
    "py-torch": "pytorch",
    "tf": "tensorflow",
    "react.js": "react",
    "reactjs": "react",
    "node": "node.js",
    "nodejs": "node.js",
    "expressjs": "express",
    "rag": "retrieval-augmented generation (rag)",
    "vector dbs": "vector databases",
    "vector db": "vector databases"
}

def load_target_role_benchmarks() -> Dict[str, Any]:
    """Load benchmark definitions from target_roles.json."""
    if not os.path.exists(BENCHMARK_PATH):
        raise FileNotFoundError(f"Target roles benchmark file not found at {BENCHMARK_PATH}")
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_skill(skill_name: str) -> str:
    """Normalize a skill name string for comparisons."""
    clean = skill_name.strip().lower()
    clean = re.sub(r'[^\w\s\-\.\/]', '', clean)
    return ALIAS_MAP.get(clean, clean)

def is_skill_matched(learner_skill_normalized: str, benchmark_skill_normalized: str) -> bool:
    """Check if a learner's skill matches a benchmark skill safely without false positives."""
    if learner_skill_normalized == benchmark_skill_normalized:
        return True
    
    # Substring match for compound phrases if reasonable
    if len(learner_skill_normalized) > 3 and len(benchmark_skill_normalized) > 3:
        if learner_skill_normalized in benchmark_skill_normalized or benchmark_skill_normalized in learner_skill_normalized:
            # Prevent 'sql' from matching 'postgresql' directly unless explicit
            if learner_skill_normalized == "sql" and "postgresql" in benchmark_skill_normalized:
                return False
            return True
            
    return False

def analyze_skill_gaps(
    learner_profile: LearnerProfile,
    target_role: str,
    gemini_client: Optional[Any] = None
) -> SkillGapReport:
    """
    Compare learner profile against target role benchmark and generate structured SkillGapReport.
    
    Deterministically computes readiness percentage and matches skills.
    """
    benchmarks = load_target_role_benchmarks()
    
    if target_role not in benchmarks:
        raise ValueError(f"Target role '{target_role}' is not supported in benchmarks. Choose from: {list(benchmarks.keys())}")
        
    role_benchmark = benchmarks[target_role]
    benchmark_core = role_benchmark.get("core_skills", [])
    benchmark_supp = role_benchmark.get("supporting_skills", [])
    benchmark_tools = role_benchmark.get("tools_and_technologies", [])

    # Collect all learner skills into a normalized set
    learner_raw_skills = set(learner_profile.technical_skills + learner_profile.tools_and_technologies + learner_profile.other_capabilities)
    for proj in learner_profile.projects:
        learner_raw_skills.update(proj.technologies)
        
    learner_normalized = {normalize_skill(s): s for s in learner_raw_skills if s and s.strip()}

    # Match Core Skills
    acquired_core = []
    missing_core = []
    for core_item in benchmark_core:
        c_norm = normalize_skill(core_item)
        matched = any(is_skill_matched(l_norm, c_norm) for l_norm in learner_normalized.keys())
        if matched:
            acquired_core.append(core_item)
        else:
            missing_core.append(core_item)

    # Match Supporting Skills
    acquired_supp = []
    missing_supp = []
    for supp_item in benchmark_supp:
        s_norm = normalize_skill(supp_item)
        matched = any(is_skill_matched(l_norm, s_norm) for l_norm in learner_normalized.keys())
        if matched:
            acquired_supp.append(supp_item)
        else:
            missing_supp.append(supp_item)

    # Match Tools & Technologies
    acquired_tools = []
    missing_tools = []
    for tool_item in benchmark_tools:
        t_norm = normalize_skill(tool_item)
        matched = any(is_skill_matched(l_norm, t_norm) for l_norm in learner_normalized.keys())
        if matched:
            acquired_tools.append(tool_item)
        else:
            missing_tools.append(tool_item)

    # Deterministic Readiness Score Calculation (Core: 60%, Supporting: 25%, Tools: 15%)
    core_ratio = len(acquired_core) / max(len(benchmark_core), 1)
    supp_ratio = len(acquired_supp) / max(len(benchmark_supp), 1)
    tool_ratio = len(acquired_tools) / max(len(benchmark_tools), 1)
    
    raw_score = (core_ratio * 60.0) + (supp_ratio * 25.0) + (tool_ratio * 15.0)
    readiness_percentage = round(min(100.0, max(0.0, raw_score)), 1)

    # Build Prioritized Gaps List
    prioritized_gaps = []
    for skill in missing_core:
        prioritized_gaps.append(PrioritizedGap(skill=skill, priority="Critical", category="Core Skill"))
    for skill in missing_supp:
        prioritized_gaps.append(PrioritizedGap(skill=skill, priority="Important", category="Supporting Skill"))
    for tool in missing_tools:
        prioritized_gaps.append(PrioritizedGap(skill=tool, priority="Nice to Have", category="Technology"))

    # Generate Gap Summary (Deterministic fallback first)
    top_missing_str = ", ".join(missing_core[:3]) if missing_core else "None! You possess all core skills."
    fallback_summary = (
        f"You have a {readiness_percentage}% readiness match for {target_role}. "
        f"You possess {len(acquired_core)} of {len(benchmark_core)} core skills. "
        f"Top critical focus areas: {top_missing_str}."
    )
    
    gap_summary = fallback_summary

    # Attempt AI summary if Gemini client is available
    if gemini_client and gemini_client.is_configured():
        try:
            prompt = f"""
Summarize the following skill gap analysis for a learner targeting the role of '{target_role}'.
Keep the summary encouraging, concise (2-3 sentences), and highlight the top priority skills to learn next.

Data:
- Target Role: {target_role}
- Readiness Score: {readiness_percentage}%
- Acquired Core Skills: {acquired_core}
- Missing Core Skills (Critical): {missing_core}
- Missing Supporting Skills: {missing_supp}
- Missing Tools: {missing_tools}

Provide ONLY the summary text (no bullet points, no markdown formatting).
"""
            # Direct generation without JSON schema requirement
            response = gemini_client.client.models.generate_content(
                model=gemini_client.model_name,
                contents=prompt
            )
            if response and response.text and response.text.strip():
                gap_summary = response.text.strip()
        except Exception:
            # Maintain deterministic summary if Gemini call fails
            pass

    return SkillGapReport(
        target_role=target_role,
        acquired_core_skills=acquired_core,
        missing_core_skills=missing_core,
        acquired_supporting_skills=acquired_supp,
        missing_supporting_skills=missing_supp,
        technology_gaps=missing_tools,
        prioritized_gaps=prioritized_gaps,
        readiness_percentage=readiness_percentage,
        gap_summary=gap_summary
    )
