def calculate_final_score(
    keyword_score,
    ats_score,
    impact_score,
    skills_score,
    structure_score,
):
    final_score = (
        keyword_score * 0.35
        + skills_score * 0.25
        + ats_score * 0.20
        + impact_score * 0.10
        + structure_score * 0.10
    )
    return int(round(final_score))