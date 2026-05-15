def generate_gap_analysis(matched_skills, missing_skills, semantic_score):

    gap_insights = []

    matched_skills_lower = [
        skill.lower() for skill in matched_skills
    ]

    missing_skills_lower = [
        skill.lower() for skill in missing_skills
    ]

    # -------------------------
    # Semantic Match Insight
    # -------------------------

    if semantic_score >= 70:
        gap_insights.append(
            "Your resume language strongly aligns with this job description."
        )

    elif semantic_score >= 40:
        gap_insights.append(
            "Your resume has moderate language alignment with this job description, but could be tailored more closely."
        )

    else:
        gap_insights.append(
            "Your resume may not closely match the wording and priorities of this job description yet."
        )

    # -------------------------
    # Technical Strength Insight
    # -------------------------

    if "python" in matched_skills_lower or "sql" in matched_skills_lower:
        gap_insights.append(
            "Your resume shows relevant technical experience for this role."
        )

    # -------------------------
    # Missing Communication Insight
    # -------------------------

    if "communication" in missing_skills_lower:
        gap_insights.append(
            "This role appears to value communication. Consider adding experience with teamwork, presentations, documentation, or stakeholder collaboration."
        )

    # -------------------------
    # Missing Cloud Insight
    # -------------------------

    if "aws" in missing_skills_lower or "cloud" in missing_skills_lower:
        gap_insights.append(
            "This role includes cloud-related skills. Consider adding AWS, deployment, or cloud project experience if you have it."
        )

    # -------------------------
    # Missing AI / Machine Learning Insight
    # -------------------------

    if "ai" in missing_skills_lower or "machine learning" in missing_skills_lower:
        gap_insights.append(
            "This role includes AI or machine learning language. Consider highlighting AI tools, model experimentation, or automation projects."
        )

    # -------------------------
    # Overall Skill Coverage Insight
    # -------------------------

    if len(missing_skills) == 0:
        gap_insights.append(
            "No major skill gaps were detected based on the current keyword and semantic analysis."
        )

    elif len(matched_skills) > len(missing_skills):
        gap_insights.append(
            "Your resume covers more required skills than it misses, which is a positive signal."
        )

    else:
        gap_insights.append(
            "Your resume may need stronger alignment with the role before applying."
        )

    return gap_insights