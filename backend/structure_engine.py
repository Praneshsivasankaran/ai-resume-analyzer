def analyze_structure(resume_text):
    score = 0
    feedback = []
    text_lower = resume_text.lower()

    sections = {
        "summary": ["summary", "professional summary", "profile", "about"],
        "experience": ["experience", "work history", "professional experience", "project", "projects", "employment"],
        "skills": ["skills", "technical skills", "core competencies", "technologies"],
        "education": ["education", "academic background", "university", "college"],
    }

    present = 0
    for section, keywords in sections.items():
        if any(k in text_lower for k in keywords):
            present += 1
        else:
            feedback.append(f"{section.capitalize()} section missing")

    score += (present / len(sections)) * 60

    bullet_symbols = ["•", "●", "·", "▪", "◦"]
    bullet_count = sum(resume_text.count(s) for s in bullet_symbols)
    # Also count lines starting with - or *
    lines = resume_text.splitlines()
    dash_bullets = sum(1 for line in lines if line.strip().startswith(("-", "*")))
    bullet_count += dash_bullets

    if bullet_count >= 8:
        score += 40
    elif bullet_count >= 3:
        score += 25
    else:
        feedback.append("Use bullet points for better readability.")

    return int(round(score)), feedback