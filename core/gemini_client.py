import os
import json
import time
from typing import Optional, Dict, Any
import config
from core.models import LearnerProfile
from tools.profile_extractor_fallback import extract_profile_from_raw_text

try:
    from google import genai
    from google.genai import types
    GENAI_AVAILABLE = True
except ImportError:
    GENAI_AVAILABLE = False


class GeminiClient:
    """Wrapper around official Google GenAI Python SDK with automatic retry & fallback parsing."""

    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or config.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")
        self.model_name = model_name or config.GEMINI_MODEL or "gemini-3.5-flash"
        self.fallback_models = [
            "gemini-3.5-flash",
            "gemini-3.1-flash-lite",
            "gemini-2.5-flash",
            "gemini-flash-latest",
            "gemini-flash-lite-latest"
        ]
        self.client = None

        if GENAI_AVAILABLE and self.api_key:
            try:
                self.client = genai.Client(api_key=self.api_key)
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini Client: {e}")

    def is_configured(self) -> bool:
        """Check if Gemini client is properly initialized."""
        return self.client is not None

    def get_status(self) -> dict:
        """Return diagnostic status of the Gemini connection."""
        return {
            "sdk_installed": GENAI_AVAILABLE,
            "api_key_set": bool(self.api_key),
            "client_initialized": self.is_configured(),
            "model": self.model_name
        }

    def _generate_with_fallback(self, prompt: str, schema_cls: Any) -> Any:
        """Execute generate_content with automatic retry across fallback models."""
        if not self.is_configured():
            return None, "Gemini API key is not configured."

        models_to_try = [self.model_name] + [m for m in self.fallback_models if m != self.model_name]
        last_error = None

        for model in models_to_try:
            for attempt in range(2):  # 2 attempts per model
                try:
                    config_params = types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema_cls,
                        temperature=0.1,
                    )

                    response = self.client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=config_params,
                    )
                    return response, None
                except Exception as e:
                    last_error = str(e)
                    if "503" in last_error or "RESOURCE_EXHAUSTED" in last_error or "429" in last_error or "UNAVAILABLE" in last_error:
                        time.sleep(1)  # brief pause before trying next model
                    else:
                        break  # move to next model if model not found or non-transient error

        return None, last_error

    def extract_learner_profile(self, resume_text: str) -> Dict[str, Any]:
        """
        Analyze raw resume text using Gemini and extract a structured LearnerProfile.
        Falls back to smart offline text extraction if API rate limits (429) or quota limits are hit.
        """
        if not resume_text or not resume_text.strip():
            return {
                "success": False,
                "profile": None,
                "error": "Resume text is empty or missing."
            }

        prompt = f"""
You are an expert technical recruiter and resume analyzer.
Analyze the following resume text and extract the candidate's structured profile.

STRICT INSTRUCTIONS:
- Extract ONLY information directly supported by the resume text.
- Do NOT infer unsupported skills, tools, or roles.
- Do NOT fabricate experience or dates.
- Preserve exact programming languages, frameworks, libraries, and project names as stated.
- If any requested field or section is not mentioned in the resume, return an empty list or null.

RESUME TEXT:
---
{resume_text}
---
"""

        response, err = self._generate_with_fallback(prompt, LearnerProfile)
        
        # If API is rate-limited (429/quota), unconfigured, or fails, use Smart Offline Extractor Fallback!
        if not response:
            print(f"Gemini API rate-limit/quota notice ({err}). Engaging Smart Offline Resume Parser...")
            fallback_profile = extract_profile_from_raw_text(resume_text)
            return {
                "success": True,
                "profile": fallback_profile,
                "error": None,
                "is_fallback": True,
                "note": "Extracted via Smart Offline Engine (Gemini API Quota Exceeded)"
            }

        try:
            parsed_profile = None
            if hasattr(response, "parsed") and response.parsed is not None:
                parsed_profile = response.parsed
                if isinstance(parsed_profile, dict):
                    parsed_profile = LearnerProfile.model_validate(parsed_profile)
            elif response.text:
                parsed_profile = LearnerProfile.model_validate_json(response.text)

            if not parsed_profile:
                fallback_profile = extract_profile_from_raw_text(resume_text)
                return {
                    "success": True,
                    "profile": fallback_profile,
                    "error": None,
                    "is_fallback": True
                }

            return {
                "success": True,
                "profile": parsed_profile,
                "error": None
            }

        except Exception as e:
            fallback_profile = extract_profile_from_raw_text(resume_text)
            return {
                "success": True,
                "profile": fallback_profile,
                "error": None,
                "is_fallback": True
            }
