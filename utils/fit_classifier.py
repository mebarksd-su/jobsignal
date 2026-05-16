def classify_job_fit(match_score, semantic_score, matched_skills, missing_skills):

    fit_result = {
        "label": "",
        "summary": "",
        "effort_level": "",
        "next_action": ""
    }

    matched_count = len(matched_skills)
    missing_count = len(missing_skills)

    # -------------------------
    # Strong Overall Alignment
    # -------------------------

    if match_score >= 75 and semantic_score >= 40 and matched_count >= missing_count:
        fit_result["label"] = "Ready to Apply"
        fit_result["summary"] = (
            "Your resume already lines up well with this role and shows a strong mix of relevant skills and experience."
        )
        fit_result["effort_level"] = "Small Edits"
        fit_result["next_action"] = (
            "You’re in a strong spot. Make a few small edits so your best experience stands out right away."
        )

    # -------------------------
    # Strong Skills, Weak Wording
    # -------------------------

    elif match_score >= 70 and semantic_score < 40:
        fit_result["label"] = "Strong Skills, Needs Clearer Wording"
        fit_result["summary"] = (
            "You already have many of the right skills for this role, but your resume could do a better job communicating them in the same language used in the job description."
        )
        fit_result["effort_level"] = "Moderate Edits"
        fit_result["next_action"] = (
            "Try rewriting a few resume bullets using keywords and responsibilities from the posting while still keeping everything truthful to your experience."
        )

    # -------------------------
    # Strong Wording, Skill Gaps Present
    # -------------------------

    elif semantic_score >= 40 and missing_count > matched_count:
        fit_result["label"] = "Good Wording, Missing Key Skills"
        fit_result["summary"] = (
            "Your resume sounds aligned with the role overall, but there are still a few important skills or tools that are not clearly represented yet."
        )
        fit_result["effort_level"] = "Moderate Edits"
        fit_result["next_action"] = (
            "If you genuinely have experience with the missing skills, make them easier to spot. Otherwise, consider building a small project to strengthen that area."
        )

    # -------------------------
    # Moderate Alignment
    # -------------------------

    elif match_score >= 50:
        fit_result["label"] = "Some Match, Needs Focus"
        fit_result["summary"] = (
            "Your background connects with parts of this role, but the resume still feels too general for this specific position."
        )
        fit_result["effort_level"] = "Moderate Edits"
        fit_result["next_action"] = (
            "Focus your strongest experiences around the responsibilities and skills emphasized in the posting."
        )

    # -------------------------
    # Low Alignment
    # -------------------------

    else:
        fit_result["label"] = "Needs More Role Evidence"
        fit_result["summary"] = (
            "Right now, the resume does not show enough clear evidence for what this role is asking for."
        )
        fit_result["effort_level"] = "Major Updates"
        fit_result["next_action"] = (
            "This may be a stretch role for now. Strengthen the resume with more relevant skills, projects, or experience before relying on it for this kind of application."
        )

    return fit_result