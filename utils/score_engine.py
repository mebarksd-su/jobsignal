# =========================
# RADARSCORE ENGINE
# Combines keyword skill matching and semantic alignment
# into one overall role-fit score for RoleRadar.
# =========================
def calculate_final_fit_score(match_score, semantic_score):

    # RadarScore prioritizes direct skill overlap slightly more
    # than semantic resume alignment.
    keyword_weight = 0.6
    semantic_weight = 0.4

    # Weighted scoring calculation
    final_score = (
        match_score * keyword_weight
    ) + (
        semantic_score * semantic_weight
    )

    # Rounded for cleaner dashboard display
    return round(final_score, 1)