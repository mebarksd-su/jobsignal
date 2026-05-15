def classify_job_fit(match_score, semantic_score, matched_skills, missing_skills):

    fit_result = {
        "label": "",
        "summary": "",
        "tailoring_level": "",
        "next_action": ""
    }

    matched_count = len(matched_skills)
    missing_count = len(missing_skills)

    # -------------------------
    # Strong Overall Fit
    # -------------------------

    if match_score >= 75 and semantic_score >= 40 and matched_count >= missing_count:
        fit_result["label"] = "Strong Fit"
        fit_result["summary"] = (
            "Your resume shows strong skill coverage and solid language alignment with this role."
        )
        fit_result["tailoring_level"] = "Light Tailoring"
        fit_result["next_action"] = (
            "Apply with a lightly tailored resume and emphasize your strongest matching skills."
        )

    # -------------------------
    # Keyword Strong, Semantic Weak
    # -------------------------

    elif match_score >= 70 and semantic_score < 40:
        fit_result["label"] = "Good Skill Match, Needs Better Wording"
        fit_result["summary"] = (
            "Your resume contains several required skills, but the overall wording does not closely match the job description."
        )
        fit_result["tailoring_level"] = "Moderate Tailoring"
        fit_result["next_action"] = (
            "Rewrite bullets to mirror the job description more closely and include role-specific language."
        )

    # -------------------------
    # Semantic Strong, Skill Gaps Present
    # -------------------------

    elif semantic_score >= 40 and missing_count > matched_count:
        fit_result["label"] = "Language Fit Strong, Skill Coverage Weak"
        fit_result["summary"] = (
            "Your resume language aligns with the role, but several required skills are missing."
        )
        fit_result["tailoring_level"] = "Moderate Tailoring"
        fit_result["next_action"] = (
            "Add missing technical skills only if you genuinely have experience with them."
        )

    # -------------------------
    # Moderate Fit
    # -------------------------

    elif match_score >= 50:
        fit_result["label"] = "Moderate Fit"
        fit_result["summary"] = (
            "Your resume has some alignment with the role, but it needs stronger targeting before applying."
        )
        fit_result["tailoring_level"] = "Moderate Tailoring"
        fit_result["next_action"] = (
            "Tailor your resume bullets toward the missing skills and the role's main responsibilities."
        )

    # -------------------------
    # Weak Fit
    # -------------------------

    else:
        fit_result["label"] = "Weak Fit"
        fit_result["summary"] = (
            "Your resume does not currently show enough alignment with this job description."
        )
        fit_result["tailoring_level"] = "Heavy Tailoring"
        fit_result["next_action"] = (
            "Only apply if this role is important to you, and heavily tailor the resume first."
        )

    return fit_result