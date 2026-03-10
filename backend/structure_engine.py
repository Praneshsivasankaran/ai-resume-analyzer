def analyze_structure(resume_text):

    score = 0
    feedback = []

    # Section checks
    sections = {
        "summary": ["summary", "professional summary", "profile"],
       "experience": ["experience", "work history", "professional experience", "project", "projects"],
        "skills": ["skills", "technical skills", "core competencies"],
        "education": ["education", "academic background"]
    }

    section_count = 0

    for section, keywords in sections.items():
        if any(keyword in resume_text for keyword in keywords):
            section_count += 1
        else:
            feedback.append(f"{section.capitalize()} section missing")

    # Section completeness scoring
    score += (section_count / len(sections)) * 60

    # Bullet point detection
    bullet_symbols = ["•", "-", "*"]
    bullet_count = sum(resume_text.count(symbol) for symbol in bullet_symbols)

    if bullet_count >= 5:
        score += 40
    elif bullet_count >= 2:
        score += 25
    else:
        feedback.append("Use bullet points for better readability")

    return round(score, 2), feedback