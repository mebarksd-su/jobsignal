from collections import Counter


def analyze_skill_trends(analysis_history):

    all_missing_skills = []
    all_matched_skills = []

    for record in analysis_history:

        analysis = record["analysis"]

        all_missing_skills.extend(
            analysis["missing_skills"]
        )

        all_matched_skills.extend(
            analysis["matched_skills"]
        )

    missing_counter = Counter(all_missing_skills)
    matched_counter = Counter(all_matched_skills)

    trending_missing = missing_counter.most_common(5)
    trending_strengths = matched_counter.most_common(5)

    return {
        "trending_missing": trending_missing,
        "trending_strengths": trending_strengths
    }