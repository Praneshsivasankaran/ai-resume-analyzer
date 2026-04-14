def generate_suggestions(
    breakdown,
    missing_keywords,
    missing_skills,
    ats_issues,
    impact_feedback,
    structure_feedback,
):
    suggestions = []

    # Skills take priority — show those first
    if missing_skills:
        suggestions.append(
            f"Strengthen your technical stack by adding experience with: {', '.join(missing_skills[:8])}."
        )

    # Filter missing_keywords: drop any that are already in missing_skills (case-insensitive)
    skill_names_lower = {s.lower() for s in missing_skills}
    filtered_keywords = [
        kw for kw in missing_keywords if kw.lower() not in skill_names_lower
    ]

    if filtered_keywords:
        suggestions.append(
            f"Other terms from the job description worth mentioning: {', '.join(filtered_keywords[:6])}."
        )

    if breakdown["keyword"] < 55:
        suggestions.append(
            "Improve overall job alignment by weaving more of the job description's language into your resume."
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