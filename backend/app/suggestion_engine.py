def generate_suggestions(
    breakdown,
    missing_keywords,
    missing_skills,
    ats_issues,
    impact_feedback,
    structure_feedback,
    grammar_feedback
):

    suggestions = []

    # --- Keyword Suggestions ---
    if breakdown["keyword"] < 40:
        suggestions.append(
            "Improve job alignment by incorporating more keywords from the job description."
        )

    if missing_keywords:
        suggestions.append(
            f"Consider adding experience with: {', '.join(missing_keywords)}."
        )

    # --- Skills Suggestions ---
    if missing_skills:
        suggestions.append(
            f"Strengthen technical stack by adding: {', '.join(missing_skills)}."
        )

    # --- ATS Suggestions ---
    if ats_issues:
        suggestions.extend(ats_issues)

    # --- Impact Suggestions ---
    if impact_feedback:
        suggestions.extend(impact_feedback)

    # --- Structure Suggestions ---
    if structure_feedback:
        suggestions.extend(structure_feedback)

    # --- Grammar Suggestions ---
    if grammar_feedback:
        suggestions.extend(grammar_feedback)

    # --- High Score Praise ---
    if breakdown["impact"] >= 90:
        suggestions.append(
            "Strong measurable achievements detected — good use of quantified impact."
        )

    if breakdown["structure"] >= 90:
        suggestions.append(
            "Resume structure is clean and ATS-friendly."
        )

    return suggestions