import json
import os
import re
from collections import Counter
from .skill_aliases import SKILL_ALIASES


SKILLS_TAXONOMY_FILE = os.path.join(
    os.path.dirname(__file__),
    "skills_taxonomy.json"
)


DISPLAY_NAMES = {
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





def load_skills_taxonomy():

    if not os.path.exists(SKILLS_TAXONOMY_FILE):
        return {}

    with open(SKILLS_TAXONOMY_FILE, "r") as file:
        return json.load(file)


SKILLS_DB = load_skills_taxonomy()


def format_skill_name(skill):

    skill_lower = skill.lower()

    if skill_lower in SKILL_ALIASES:
        return SKILL_ALIASES[skill_lower]

    return DISPLAY_NAMES.get(
        skill_lower,
        skill.title()
    )


def iter_taxonomy_skills():

    for category, skill_group in SKILLS_DB.items():

        if isinstance(skill_group, list):
            for skill in skill_group:
                yield category, skill, [skill]

        elif isinstance(skill_group, dict):
            for canonical_skill, aliases in skill_group.items():
                yield category, canonical_skill, aliases


def extract_skills(text):

    detected_skills = []
    detected_names = set()
    text_lower = text.lower()

    for category, canonical_skill, aliases in iter_taxonomy_skills():

        display_skill = format_skill_name(canonical_skill)

        for alias in aliases:
            pattern = r"\b" + re.escape(alias.lower()) + r"\b"

            if re.search(pattern, text_lower):
                if display_skill not in detected_names:
                    detected_skills.append({
                        "display_skill": display_skill,
                        "category": category
                    })
                    detected_names.add(display_skill)
                break

    return detected_skills


def calculate_skill_frequency(detected_skills):

    skill_names = [
        item["display_skill"]
        for item in detected_skills
    ]

    return Counter(skill_names)
