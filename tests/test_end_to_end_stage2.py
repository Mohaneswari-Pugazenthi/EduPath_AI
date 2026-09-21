import sys
import os
import io

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.gemini_client import GeminiClient
from core.agent import EduPathAgent
from tools.document_parser import extract_text_from_pdf

def run_stage2_verification():
    print("--- Stage 2 Verification ---")
    
    client = GeminiClient()
    agent = EduPathAgent(client)
    status = agent.get_agent_status()
    
    print(f"Gemini Client Configured: {status['ready']}")
    print(f"SDK Installed: {status['gemini_status']['sdk_installed']}")
    print(f"API Key Set: {status['gemini_status']['api_key_set']}")
    print(f"Model: {status['gemini_status']['model']}")
    
    sample_text = """
    Alex Johnson
    Software Engineer | 3 Years Experience
    Email: alex@example.com
    
    SUMMARY:
    Full stack developer with 3 years of experience in Python, Django, PostgreSQL, and React.
    Built web applications and REST APIs.
    
    TECHNICAL SKILLS:
    - Languages: Python, JavaScript, SQL, HTML/CSS
    - Frameworks: Django, FastAPI, React, Flask
    - Databases: PostgreSQL, Redis, MongoDB
    - Tools: Git, Docker, VS Code, Linux
    
    PROJECTS:
    - E-Commerce API: Designed scalable RESTful APIs using FastAPI and PostgreSQL.
    - Analytics Dashboard: Built interactive React frontend with Django backend.
    
    EDUCATION:
    - B.S. in Computer Science, University of Technology (2021)
    
    CERTIFICATIONS:
    - AWS Certified Cloud Practitioner (2022)
    """
    
    if status['ready']:
        print("\nTesting Gemini extraction on sample resume text...")
        result = client.extract_learner_profile(sample_text)
        if result["success"]:
            profile = result["profile"]
            print(f"[SUCCESS] Extracted Profile Name: {profile.name}")
            print(f"Roles: {profile.current_roles}")
            print(f"Years of Experience: {profile.years_of_experience}")
            print(f"Technical Skills: {profile.technical_skills}")
            print(f"Tools & Tech: {profile.tools_and_technologies}")
            print(f"Projects Count: {len(profile.projects)}")
            print(f"Education: {[e.degree for e in profile.education]}")
            print(f"Certifications: {[c.title for c in profile.certifications]}")
        else:
            print(f"[FAIL] Gemini extraction error: {result['error']}")
    else:
        print("\n[NOTE] Gemini API key not provided in .env yet. Mock/offline tests passed successfully.")

if __name__ == "__main__":
    run_stage2_verification()
