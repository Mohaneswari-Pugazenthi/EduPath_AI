import sys
import os
import io

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pypdf import PdfWriter
from tools.document_parser import extract_text_from_pdf
from core.models import LearnerProfile, Project, Education, Certification

def test_document_parser_invalid_pdf():
    result = extract_text_from_pdf(b"not a real pdf content")
    assert result["success"] is False
    assert "Failed to parse PDF file" in result["error"]
    print("[PASS] Invalid PDF test passed!")

def test_document_parser_valid_pdf():
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    
    buf = io.BytesIO()
    writer.write(buf)
    buf.seek(0)
    
    result = extract_text_from_pdf(buf)
    assert result["page_count"] == 1
    assert result["success"] is False
    assert "No readable text found" in result["error"]
    print("[PASS] Blank PDF test passed!")

def test_learner_profile_schema():
    profile = LearnerProfile(
        name="John Doe",
        current_roles=["Junior Python Developer"],
        years_of_experience=2.0,
        technical_skills=["Python", "SQL", "Git"],
        tools_and_technologies=["VS Code", "PostgreSQL", "Docker"],
        projects=[
            Project(title="Web Scraper", description="Built with BeautifulSoup", technologies=["Python"])
        ],
        education=[
            Education(degree="B.S. Computer Science", institution="State University", year="2022")
        ],
        certifications=[
            Certification(title="AWS Certified Developer", issuer="Amazon Web Services")
        ]
    )
    assert profile.name == "John Doe"
    assert "Python" in profile.technical_skills
    assert len(profile.projects) == 1
    print("[PASS] LearnerProfile schema test passed!")

if __name__ == "__main__":
    test_document_parser_invalid_pdf()
    test_document_parser_valid_pdf()
    test_learner_profile_schema()
    print("ALL STAGE 2 UNIT TESTS PASSED!")
