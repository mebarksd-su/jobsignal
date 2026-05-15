def generate_rewrite_suggestions(missing_skills, semantic_score):

    suggestions = []

    missing_skills_lower = [
        skill.lower() for skill in missing_skills
    ]

    if semantic_score < 40:
        suggestions.append(
            "Rewrite one or two resume bullets using language from the job description."
        )

    if "communication" in missing_skills_lower:
        suggestions.append(
            "Add a bullet that shows communication, collaboration, presentations, documentation, or stakeholder work."
        )

    if "leadership" in missing_skills_lower:
        suggestions.append(
            "Add a bullet that shows ownership, initiative, team support, or project leadership."
        )

    if "cloud" in missing_skills_lower or "aws" in missing_skills_lower:
        suggestions.append(
            "Add a bullet showing AWS, deployment, cloud tools, or technical infrastructure experience."
        )

    if "automation" in missing_skills_lower:
        suggestions.append(
            "Add a bullet showing workflow automation, scripting, or process improvement."
        )

    if len(suggestions) == 0:
        suggestions.append(
            "Your resume is already showing strong alignment. Focus on making bullets more specific and measurable."
        )

    return suggestions