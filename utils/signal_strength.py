def calculate_signal_strength(
    matched_skills,
    missing_skills,
    skills_section_found,
    semantic_score
):

    matched_count = len(matched_skills)
    missing_count = len(missing_skills)

    # Radar Strength measures how reliable the analysis is,
    # not whether the resume is already a strong match.

    score = 35

    if skills_section_found:
        score += 30
    else:
        score += 10

    score += min(matched_count * 5, 25)

    if semantic_score >= 40:
        score += 10
    elif semantic_score >= 20:
        score += 5

    if matched_count == 0:
        score -= 25

    if missing_count > matched_count * 2 and matched_count > 0:
        score -= 5

    score = max(0, min(score, 100))

    if score >= 80:
        return {
            "label": "High",
            "score": score,
            "summary": (
                "RoleRadar found a clear resume structure and enough skill evidence to support a reliable analysis."
            )
        }

    if score >= 60:
        return {
            "label": "Moderate",
            "score": score,
            "summary": (
                "RoleRadar found useful resume evidence, but the analysis may improve with clearer skill wording or stronger role-specific details."
            )
        }

    return {
        "label": "Low",
        "score": score,
        "summary": (
            "RoleRadar could not find enough clear evidence to fully trust this analysis. A clearer skills section or more specific resume details may help."
        )
    }