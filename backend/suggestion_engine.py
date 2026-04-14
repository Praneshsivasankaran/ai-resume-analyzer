def generate_suggestions(
    breakdown,
    missing_keywords,
    missing_skills,
    ats_issues,
    impact_feedback,
    structure_feedback,
):
    suggestions = []

    if breakdown["keyword"] < 55:
        suggestions.append(
            "Improve job alignment by incorporating more keywords from the job description."
        )

    if missing_keywords:
        top = missing_keywords[:6]
        suggestions.append(
            f"Consider incorporating these terms from the job description: {', '.join(top)}."
        )

    if missing_skills:
        suggestions.append(
            f"Strengthen your technical stack by adding experience with: {', '.join(missing_skills[:8])}."
        )

    if ats_issues:
        suggestions.extend(ats_issues)

    if impact_feedback:
        suggestions.extend(impact_feedback)

    if structure_feedback:
        suggestions.extend(structure_feedback)

    if breakdown["impact"] >= 85:
        suggestions.append("Strong measurable achievements detected — great use of quantified impact.")

    if breakdown["structure"] >= 85:
        suggestions.append("Resume structure is clean and ATS-friendly.")

    return suggestions