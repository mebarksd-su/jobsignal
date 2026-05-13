def detect_skills(job_description):

    skill_keywords = [
        "Python",
        "SQL",
        "Excel",
        "Machine Learning",
        "AI",
        "Data Visualization",
        "Tableau",
        "Communication",
        "Leadership",
        "Cloud",
        "AWS",
        "Power BI"
    ]

    detected_skills = []

    for skill in skill_keywords:
        if skill.lower() in job_description.lower():
            detected_skills.append(skill)

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

    match_skills = [
        "Python",
        "SQL",
        "Excel",
        "Machine Learning",
        "AI",
        "Data Visualization",
        "Tableau",
        "Communication",
        "Leadership",
        "Cloud",
        "AWS",
        "Power BI",
        "Streamlit",
        "Pandas",
        "GitHub",
        "Automation",
        "Data Analysis",
        "APIs"
    ]

    required_skills = []
    matched_skills = []
    missing_skills = []

    for skill in match_skills:
        if skill.lower() in job_description.lower():
            required_skills.append(skill)

    for skill in required_skills:
        if skill.lower() in resume_text.lower():
            matched_skills.append(skill)
        else:
            missing_skills.append(skill)

    if len(required_skills) > 0:
        match_score = round((len(matched_skills) / len(required_skills)) * 100, 1)
    else:
        match_score = 0

    return match_score, matched_skills, missing_skills


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