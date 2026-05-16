import os
from openai import OpenAI, APIConnectionError, APITimeoutError, AuthenticationError, RateLimitError
from dotenv import load_dotenv



# Helper for formatting OpenAI errors
def format_openai_error(error):
    error_text = str(error).lower()

    if isinstance(error, AuthenticationError) or "invalid_api_key" in error_text:
        return (
            "RoleRadar could not authenticate with OpenAI. "
            "Check that your API key is correct and saved in your .env file."
        )

    if isinstance(error, RateLimitError) or "insufficient_quota" in error_text:
        return (
            "RoleRadar reached the current OpenAI usage limit. "
            "Check billing, credits, or usage limits before trying again."
        )

    if isinstance(error, APITimeoutError):
        return (
            "The AI request took too long. Try again in a moment or shorten the job description."
        )

    if isinstance(error, APIConnectionError):
        return (
            "RoleRadar could not connect to OpenAI. Check your internet connection and try again."
        )

    return (
        "RoleRadar could not complete the AI rewrite right now. "
        "Try again in a moment."
    )




def get_openai_client():
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return None

    return OpenAI(
        api_key=api_key,
        timeout=20.0
    )


def rewrite_resume_bullet_with_ai(original_bullet, job_description):
    client = get_openai_client()

    if client is None:
        return {
            "success": False,
            "result": "",
            "error": "OpenAI API key was not found. Add OPENAI_API_KEY to your environment or .env file."
        }

    if original_bullet.strip() == "":
        return {
            "success": False,
            "result": "",
            "error": "Paste a resume bullet before running the AI rewrite."
        }

    if job_description.strip() == "":
        return {
            "success": False,
            "result": "",
            "error": "Paste a target job description before running the AI rewrite."
        }

    prompt = f"""
Rewrite this resume bullet to better match the target job description.

Rules:
- Keep it truthful.
- Do not invent tools, companies, metrics, or experience.
- Make it stronger, clearer, and more professional.
- Keep it as one resume bullet.
- Use action-oriented language.
- Make it sound natural for a college student or early-career applicant.

Original resume bullet:
{original_bullet}

Target job description:
{job_description}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are a resume improvement assistant for college students and early-career applicants. "
                "You improve wording without inventing experience."
            ),
            input=prompt
        )

        return {
            "success": True,
            "result": response.output_text.strip(),
            "error": ""
        }

    except Exception as error:
        return {
            "success": False,
            "result": "",
            "error": format_openai_error(error)
        }


def summarize_job_description_with_ai(job_description):
    client = get_openai_client()

    if client is None:
        return {
            "success": False,
            "result": "",
            "error": "OpenAI API key was not found. Add OPENAI_API_KEY to your environment or .env file."
        }

    if job_description.strip() == "":
        return {
            "success": False,
            "result": "",
            "error": "Paste a job description before running the AI summary."
        }

    prompt = f"""
Summarize this job description for a college student or early-career applicant.

Rules:
- Keep it truthful.
- Do not invent details.
- Use clear, professional language.
- Keep it concise.
- Focus on what the role is really asking for.
- Mention the most important skills, responsibilities, and applicant profile.
- Write in 4 to 6 short bullet points.

Job description:
{job_description}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are a career intelligence assistant for college students and early-career applicants. "
                "You explain job descriptions clearly without exaggerating or inventing details."
            ),
            input=prompt
        )

        return {
            "success": True,
            "result": response.output_text.strip(),
            "error": ""
        }

    except Exception as error:
        return {
            "success": False,
            "result": "",
            "error": format_openai_error(error)
        }


def explain_resume_gaps_with_ai(missing_skills, matched_skills, job_description):
    client = get_openai_client()

    if client is None:
        return {
            "success": False,
            "result": "",
            "error": "OpenAI API key was not found. Add OPENAI_API_KEY to your environment or .env file."
        }

    if not missing_skills:
        return {
            "success": False,
            "result": "",
            "error": "No resume gaps were found for this analysis."
        }

    if job_description.strip() == "":
        return {
            "success": False,
            "result": "",
            "error": "Paste a job description before running the AI gap explanation."
        }

    prompt = f"""
Explain the resume gaps for this job application.

Rules:
- Keep the feedback truthful and practical.
- Do not invent experience, tools, projects, metrics, or qualifications.
- Explain why the missing skills matter for this role.
- Mention where the applicant already has overlap.
- Give clear improvement advice for a college student or early-career applicant.
- Keep it concise and human.
- Write 3 to 5 short bullet points.

Matched skills:
{matched_skills}

Missing skills:
{missing_skills}

Target job description:
{job_description}
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            instructions=(
                "You are a career intelligence assistant for college students and early-career applicants. "
                "You explain resume gaps clearly, honestly, and without making the applicant feel discouraged."
            ),
            input=prompt
        )

        return {
            "success": True,
            "result": response.output_text.strip(),
            "error": ""
        }

    except Exception as error:
        return {
            "success": False,
            "result": "",
            "error": format_openai_error(error)
        }