def calculate_skills_score(resume_text, jd_text):

    # Basic skill list (expand later)
    skill_keywords = [
        "python", "java", "c++", "sql",
        "fastapi", "django", "flask",
        "docker", "kubernetes", "aws",
        "machine learning", "tensorflow",
        "pandas", "numpy", "scikit-learn"
    ]

    required_skills = []
    matched_skills = []

    for skill in skill_keywords:
        if skill in jd_text.lower():
            required_skills.append(skill)

    for skill in required_skills:
        if skill in resume_text:
            matched_skills.append(skill)

    if not required_skills:
        return 50, []  # neutral if no skills detected

    match_ratio = len(matched_skills) / len(required_skills)

    score = round(match_ratio * 100, 2)

    missing_skills = list(set(required_skills) - set(matched_skills))

    return score, missing_skills