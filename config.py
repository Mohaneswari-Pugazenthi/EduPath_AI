import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# App Configurations
APP_NAME = "EduPath"
APP_TAGLINE = "Personalized Learning & Skill Gap Agent"
APP_VERSION = "0.1.0"

# Gemini API Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

# Target Roles Supported (P0 Benchmarks)
TARGET_ROLES = [
    "AI Engineer",
    "Data Scientist",
    "Full Stack Developer",
    "Machine Learning Engineer"
]

