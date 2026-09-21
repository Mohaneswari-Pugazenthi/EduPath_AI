import re
from typing import List
from core.models import LearnerProfile, Project, Education, Certification

# Comprehensive technical keywords database for fallback extraction
TECH_KEYWORDS = [
    "Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "SQL", "HTML", "CSS",
    "React", "Node.js", "Express", "Django", "FastAPI", "Flask", "PyTorch", "TensorFlow",
    "Scikit-Learn", "Pandas", "NumPy", "Matplotlib", "Seaborn", "PostgreSQL", "MySQL",
    "MongoDB", "Redis", "Docker", "Kubernetes", "Git", "GitHub", "AWS", "Azure", "GCP",
    "Machine Learning", "Deep Learning", "Artificial Intelligence", "Data Science",
    "Natural Language Processing", "NLP", "Computer Vision", "REST API", "GraphQL",
    "Vector Databases", "LangChain", "LlamaIndex", "ChromaDB", "Pinecone", "FAISS",
    "RAG", "Retrieval-Augmented Generation", "Prompt Engineering", "Embeddings"
]

EDUCATION_KEYWORDS = ["Bachelor", "Master", "B.Tech", "B.E.", "B.S.", "M.S.", "M.Tech", "Degree", "University", "College", "Institute"]

def extract_profile_from_raw_text(resume_text: str) -> LearnerProfile:
    """
    Deterministically extract a structured LearnerProfile directly from raw resume text
    when Gemini API quota is exhausted or unavailable.
    """
    lines = [line.strip() for line in resume_text.split("\n") if line.strip()]
    
    # 1. Extract Name (from first non-empty line or file header)
    candidate_name = "Candidate"
    if lines:
        first_line = lines[0]
        # Clean up common resume title headers
        clean_name = re.sub(r'^(resume|curriculum vitae|cv|profile)\s*[:\-]*\s*', '', first_line, flags=re.IGNORECASE).strip()
        if len(clean_name) > 2 and len(clean_name) < 40 and not any(char.isdigit() for char in clean_name):
            candidate_name = clean_name.title()

    # 2. Extract Technical Skills & Tools via keyword scanning
    detected_skills: List[str] = []
    text_lower = resume_text.lower()
    
    for kw in TECH_KEYWORDS:
        # Check boundary match or substring match
        pattern = r'\b' + re.escape(kw.lower()) + r'\b'
        if re.search(pattern, text_lower):
            detected_skills.append(kw)

    # Separate into skills and tools
    languages_and_concepts = ["Python", "Java", "C++", "C#", "JavaScript", "TypeScript", "SQL", "HTML", "CSS", "Machine Learning", "Deep Learning", "Artificial Intelligence", "Data Science", "NLP", "REST API", "RAG", "Prompt Engineering"]
    
    technical_skills = [s for s in detected_skills if s in languages_and_concepts]
    tools_and_tech = [s for s in detected_skills if s not in languages_and_concepts]
    
    if not technical_skills and detected_skills:
        technical_skills = detected_skills[:4]
    if not tools_and_tech and len(detected_skills) > 4:
        tools_and_tech = detected_skills[4:]

    # 3. Estimate Years of Experience
    exp_years = 1.0
    exp_matches = re.findall(r'(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)', text_lower)
    if exp_matches:
        try:
            exp_years = float(exp_matches[0])
        except ValueError:
            pass

    # 4. Extract Projects
    projects = []
    project_sections = re.findall(r'(?:projects?|key projects?)\s*[:\-]*\n+(.*?)(?=\n\s*(?:education|experience|skills|certifications)|$)', resume_text, re.IGNORECASE | re.DOTALL)
    if project_sections:
        proj_text = project_sections[0]
        proj_lines = [l.strip() for l in proj_text.split('\n') if l.strip()]
        for l in proj_lines[:3]:
            if len(l) > 5:
                proj_tech = [s for s in detected_skills if s.lower() in l.lower()]
                projects.append(Project(title=l[:50], description=l, technologies=proj_tech))
                
    if not projects:
        projects.append(Project(title="Technical Project", description="Relevant hands-on software development project", technologies=detected_skills[:3]))

    # 5. Extract Education
    education = []
    for line in lines:
        if any(edu_kw.lower() in line.lower() for edu_kw in EDUCATION_KEYWORDS):
            education.append(Education(degree=line[:60], institution="", year=""))
            break
            
    if not education:
        education.append(Education(degree="Bachelor of Technology / Science", institution="University", year=""))

    return LearnerProfile(
        name=candidate_name,
        current_roles=["Software Developer"],
        years_of_experience=exp_years,
        technical_skills=technical_skills if technical_skills else ["Python", "SQL"],
        tools_and_technologies=tools_and_tech if tools_and_tech else ["Git", "VS Code"],
        projects=projects,
        education=education,
        certifications=[Certification(title="Technical Certification", issuer="Online Platform")] if "certif" in text_lower else [],
        other_capabilities=["Problem Solving", "Team Collaboration"]
    )
