from dotenv import load_dotenv
import os 

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

import json
from google import genai
from google.genai import types

class AnalysisError(Exception):
    pass


# We define the exact JSON shape we want, and describe the rules
# for each field. Being explicit here = more reliable output.
ANALYSIS_PROMPT_TEMPLATE = """
You are an expert technical recruiter and career advisor.

Analyze the following resume text and respond with a JSON object matching
EXACTLY this structure (no extra keys, no missing keys):

{{
  "technical_skills": ["skill1", "skill2"],
  "soft_skills": ["skill1", "skill2"],
  "profile_summary": "2-3 sentence summary of the candidate",
  "recommended_job_role": "most suitable single job title",
  "missing_skills": ["skill1", "skill2"]
}}

Rules:
- technical_skills: hard/technical skills explicitly mentioned or clearly implied.
- soft_skills: interpersonal/behavioral skills implied by projects, leadership roles, etc.
- profile_summary: concise, professional tone, third person.
- recommended_job_role: ONE specific, realistic job title based on skills/education/experience.
- missing_skills: skills the candidate needs to learn to be a STRONG fit for
  recommended_job_role, that are NOT already present in the resume.

Resume text:
\"\"\"
{resume_text}
\"\"\"

"""

def analyze_resume(resume_text: str, api_key: str)-> dict:
    if not resume_text or not resume_text.strip():
        raise AnalysisError("No resume text porvided to analyze")

    client = genai.Client(api_key=api_key)
    prompt = ANALYSIS_PROMPT_TEMPLATE.format(resume_text = resume_text)

    try:
        response = client.models.generate_content(
            model = "gemini-3.5-flash", 
            contents = prompt,
            config = types.GenerateContentConfig(
                response_mime_type = 'application/json',
            ),
        )
    except Exception as e:
        raise AnalysisError(f"Gemini API call failed: {e}")

    raw_text = response.text

    cleaned = raw_text.strip()
    if(cleaned.startswith('```')):
        cleaned = cleaned.strip('`')
        if (cleaned.lower().startswith('json')):
            cleaned = cleaned[4:]
            cleaned = cleaned.strip()

    try:
        result = json.loads(cleaned)
    except json.JSONDecodeError:
        raise AnalysisError(f"Gemini didn't return valid JSON. Raw response: {raw_text[:300]}")
    
    required_keys = {
        "technical_skills",
        "soft_skills",
        "profile_summary",
        "recommended_job_role",
        "missing_skills"
    }

    missing_keys = required_keys - result.keys()
    if(missing_keys):
        raise AnalysisError(f"Gemini response is missing expected keys : {missing_keys}")

    return result

