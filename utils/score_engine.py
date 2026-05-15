def calculate_final_fit_score(match_score, semantic_score):

    keyword_weight = 0.6
    semantic_weight = 0.4

    final_score = (
        match_score * keyword_weight
    ) + (
        semantic_score * semantic_weight
    )

    return round(final_score, 1)