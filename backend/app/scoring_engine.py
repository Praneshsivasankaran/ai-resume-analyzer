def calculate_final_score(
    keyword_score,
    ats_score,
    impact_score,
    skills_score,
    structure_score,
    grammar_score
):

    final_score = (
        keyword_score * 0.35 +
        ats_score * 0.20 +
        impact_score * 0.15 +
        skills_score * 0.10 +
        structure_score * 0.10 +
        grammar_score * 0.10
    )

    return round(final_score, 2)