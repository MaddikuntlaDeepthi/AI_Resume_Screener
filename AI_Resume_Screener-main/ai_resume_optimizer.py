import os
import textwrap
from groq import Groq
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file")

client = Groq(api_key=api_key)

def optimize_resume(resume_text: str, job_description: str) -> str:
    """
    Optimize a resume text to match a job description and improve ATS score.
    Returns the optimized resume as a string.
    """
    prompt = textwrap.dedent(f"""
        You are a professional ATS resume writer.

        Rewrite the following resume so it matches the job description
        and improves ATS score.

        IMPORTANT RULES:
        - Return ONLY the resume.
        - Do NOT include explanations.
        - Do NOT include comments.
        - Use clear sections:
          Name
          Contact Information
          Professional Summary
          Skills
          Education
          Projects
          Experience
          Certifications
        - Use bullet points for skills and projects.

        Job Description:
        {job_description}

        Resume:
        {resume_text}
    """)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    content = getattr(response.choices[0].message, "content", None)
    if content is None:
        raise ValueError("Groq API returned no content")
    return content