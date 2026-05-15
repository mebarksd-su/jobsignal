import json
import os
from .skill_aliases import SKILL_ALIASES
from .skill_weights import SKILL_WEIGHTS
from .critical_skills import ROLE_CRITICAL_SKILLS


SKILLS_TAXONOMY_FILE = os.path.join(os.path.dirname(__file__), "skills_taxonomy.json")


# =========================
# SKILLS TAXONOMY LOADER
# Loads the shared analytics/AI skills taxonomy used across analyzers.
# =========================

def load_skills_taxonomy():

    if not os.path.exists(SKILLS_TAXONOMY_FILE):
        return {}

    with open(SKILLS_TAXONOMY_FILE, "r") as file:
        return json.load(file)



SKILLS_DB = load_skills_taxonomy()

# =========================
# CRITICAL SKILL FLATTENER
# Converts role-specific critical skills into one searchable set for base scoring.
# Role-specific critical gaps are still handled separately in app.py.
# =========================

CRITICAL_SKILLS = set()

for role_skills in ROLE_CRITICAL_SKILLS.values():
    for skill in role_skills:
        CRITICAL_SKILLS.add(skill.lower())

def iter_taxonomy_skills():

    for category, skill_group in SKILLS_DB.items():

        if isinstance(skill_group, list):
            for skill in skill_group:
                yield category, skill, [skill]

        elif isinstance(skill_group, dict):
            for canonical_skill, aliases in skill_group.items():
                yield category, canonical_skill, aliases


# =========================
# SKILL DISPLAY HELPERS
# Keeps common acronyms and tool names formatted cleanly.
# =========================

def format_skill_name(skill):

    skill_lower = skill.lower()

    if skill_lower in SKILL_ALIASES:
        return SKILL_ALIASES[skill_lower]

    display_names = {
        "sql": "SQL",
        "ai": "AI",
        "aws": "AWS",
        "gcp": "GCP",
        "nlp": "NLP",
        "llm": "LLM",
        "api": "API",
        "apis": "APIs",
        "html": "HTML",
        "css": "CSS",
        "c++": "C++",
        "power bi": "Power BI",
        "tableau": "Tableau",
        "python": "Python",
        "pandas": "Pandas",
        "numpy": "NumPy",
        "github": "GitHub",
        "streamlit": "Streamlit",
        "arcgis": "ArcGIS",
        "qgis": "QGIS"
    }

    return display_names.get(skill_lower, skill.title())

def get_skill_weight(skill):

    skill_lower = skill.lower()

    return SKILL_WEIGHTS.get(
        skill_lower,
        1
    )

def detect_skills(job_description):

    detected_skills = []

    detected_names = set()

    job_description_lower = job_description.lower()

    for category, canonical_skill, aliases in iter_taxonomy_skills():

        formatted_skill = format_skill_name(canonical_skill)

        for alias in aliases:

            if alias.lower() in job_description_lower:

                if formatted_skill not in detected_names:

                    detected_skills.append(formatted_skill)

                    detected_names.add(formatted_skill)

                break

    return detected_skills


def generate_resume_recommendations(detected_skills):

    resume_recommendations = []

    if "Python" in detected_skills:
        resume_recommendations.append(
            "Highlight Python projects involving automation, analytics, or AI workflows."
        )

    if "SQL" in detected_skills:
        resume_recommendations.append(
            "Emphasize experience working with databases, queries, and structured datasets."
        )

    if "Machine Learning" in detected_skills or "AI" in detected_skills:
        resume_recommendations.append(
            "Showcase AI-related projects, model experimentation, or data-driven research."
        )

    if "Tableau" in detected_skills or "Power BI" in detected_skills:
        resume_recommendations.append(
            "Include dashboard or visualization projects demonstrating business insights."
        )

    if len(resume_recommendations) == 0:
        resume_recommendations.append(
            "Focus on transferable technical and communication skills."
        )

    return resume_recommendations



def calculate_match_score(resume_text, job_description):

    required_skills = []
    matched_skills = []
    missing_skills = []

    critical_matched = []
    critical_missing = []

    total_possible_weight = 0
    matched_weight = 0

    resume_text_lower = resume_text.lower()
    job_description_lower = job_description.lower()

    for category, canonical_skill, aliases in iter_taxonomy_skills():

        formatted_skill = format_skill_name(canonical_skill)

        appears_in_job = False
        appears_in_resume = False

        for alias in aliases:
            alias_lower = alias.lower()

            if alias_lower in job_description_lower:
                appears_in_job = True

            if alias_lower in resume_text_lower:
                appears_in_resume = True

        if appears_in_job:

            if formatted_skill not in required_skills:
                required_skills.append(formatted_skill)

                skill_weight = get_skill_weight(formatted_skill)
                total_possible_weight += skill_weight

                if appears_in_resume:

                    matched_skills.append(formatted_skill)
                    matched_weight += skill_weight

                    if canonical_skill.lower() in CRITICAL_SKILLS:
                        critical_matched.append(formatted_skill)

                else:

                    missing_skills.append(formatted_skill)

                    if canonical_skill.lower() in CRITICAL_SKILLS:
                        critical_missing.append(formatted_skill)


    if total_possible_weight > 0:
        match_score = round(
            (matched_weight / total_possible_weight) * 100,
            1
        )
    else:
        match_score = 0

    return (
        match_score,
        matched_skills,
        missing_skills,
        critical_matched,
        critical_missing
    )


def get_skill_advice(skill):

    skill_advice = {
        "Python": "Build more Python automation or analytics projects.",
        "SQL": "Practice SQL queries and database projects.",
        "AWS": "Learn cloud deployment and AWS fundamentals.",
        "Machine Learning": "Create ML prediction or classification projects.",
        "AI": "Develop AI-focused portfolio projects and workflows.",
        "Tableau": "Build interactive dashboards using Tableau.",
        "Power BI": "Create business intelligence dashboards.",
        "Communication": "Highlight teamwork, leadership, and presentation experience.",
        "Leadership": "Show initiative through leadership roles or projects.",
        "Excel": "Improve spreadsheet modeling and analysis skills.",
        "GitHub": "Upload and document more coding projects publicly.",
        "APIs": "Practice working with API integrations and external data.",
        "Streamlit": "Deploy more interactive data applications.",
        "Pandas": "Work more with real-world datasets and data cleaning."
    }

    return skill_advice.get(skill, f"Develop stronger experience with {skill}.")


def enhance_resume_bullet(original_bullet):

    bullet = original_bullet.strip()
    bullet_lower = bullet.lower()

    if bullet == "":
        return "Please enter a resume bullet to enhance."

    detected_skills = []

    if "python" in bullet_lower:
        detected_skills.append("Python")

    if "sql" in bullet_lower:
        detected_skills.append("SQL")

    if "excel" in bullet_lower:
        detected_skills.append("Excel")

    if "dashboard" in bullet_lower or "visualization" in bullet_lower:
        detected_skills.append("data visualization")

    if "ai" in bullet_lower or "machine learning" in bullet_lower:
        detected_skills.append("AI")

    if len(detected_skills) > 0:
        skills_text = ", ".join(detected_skills)

        return (
            f"Applied {skills_text} to support data analysis, workflow automation, "
            "technical problem-solving, and business-focused reporting."
        )

    improved_bullet = bullet

    action_verbs = {
        "worked on": "Developed",
        "helped": "Collaborated on",
        "made": "Engineered",
        "did": "Executed",
        "used": "Leveraged",
        "created": "Built",
        "looked at": "Analyzed"
    }

    for weak, strong in action_verbs.items():
        improved_bullet = improved_bullet.replace(weak, strong)

    if improved_bullet == bullet:
        improved_bullet = (
            f"Strengthened experience in {bullet} through applied technical work, "
            "problem-solving, and project-based execution."
        )

    return improved_bullet


def detect_enhancement_keywords(job_description):

    enhancement_keywords = [
        "Python",
        "SQL",
        "Machine Learning",
        "AI",
        "AWS",
        "Tableau",
        "Leadership",
        "Automation",
        "Analytics",
        "Data"
    ]

    keyword_matches = []

    for keyword in enhancement_keywords:
        if keyword.lower() in job_description.lower():
            keyword_matches.append(keyword)

    return keyword_matches