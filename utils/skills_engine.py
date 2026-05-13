import re


TECHNICAL_SKILLS = {
    "Programming": [
        "python",
        "sql",
        "r",
        "java",
        "javascript",
        "c++",
        "typescript"
    ],

    "Data": [
        "excel",
        "tableau",
        "power bi",
        "pandas",
        "numpy",
        "machine learning",
        "data visualization",
        "analytics"
    ],

    "Cloud": [
        "aws",
        "azure",
        "gcp",
        "cloud",
        "docker",
        "kubernetes"
    ],

    "AI": [
        "ai",
        "artificial intelligence",
        "nlp",
        "deep learning",
        "neural networks",
        "llm",
        "generative ai"
    ],

    "Business": [
        "communication",
        "leadership",
        "project management",
        "stakeholder management",
        "strategy"
    ]
}

DISPLAY_NAMES = {
    "sql": "SQL",
    "ai": "AI",
    "aws": "AWS",
    "gcp": "GCP",
    "nlp": "NLP",
    "llm": "LLM",
    "c++": "C++",
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "power bi": "Power BI"
}

def extract_skills(text):

    detected_skills = []

    text = text.lower()

    for category, skills in TECHNICAL_SKILLS.items():

        for skill in skills:

            pattern = r"\b" + re.escape(skill) + r"\b"

            if re.search(pattern, text):
                detected_skills.append({
                    "display_skill": DISPLAY_NAMES.get(
                        skill,
                        skill.title()
                    ),
                    "category": category
                })

    return detected_skills


def calculate_skill_frequency(skills):

    frequency_map = {}

    for item in skills:

        skill_name = item["display_skill"]

        if skill_name not in frequency_map:
            frequency_map[skill_name] = 1
        else:
            frequency_map[skill_name] += 1

    return frequency_map