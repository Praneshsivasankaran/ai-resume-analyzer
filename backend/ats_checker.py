import re


def check_ats_rules(resume_text):

    score = 0
    issues = []

    # 1️⃣ Email Check
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
    if re.search(email_pattern, resume_text):
        score += 20
    else:
        issues.append("Email not found")

    # 2️⃣ Phone Number Check (basic 10 digit)
    phone_pattern = r'\b\d{10}\b'
    if re.search(phone_pattern, resume_text):
        score += 20
    else:
        issues.append("Phone number not found")

    # 3️⃣ Experience Section (flexible detection)
    experience_keywords = [
    "experience",
    "work history",
    "professional experience",
    "project",
    "projects"
]

    if any(word in resume_text for word in experience_keywords):
        score += 20
    else:
        issues.append("Experience section missing")

    # 4️⃣ Skills Section (flexible detection)
    skills_keywords = [
        "skills",
        "technical skills",
        "core competencies"
    ]

    if any(word in resume_text for word in skills_keywords):
        score += 20
    else:
        issues.append("Skills section missing")

    # 5️⃣ Education Section (flexible detection)
    education_keywords = [
        "education",
        "academic background",
        "qualifications"
    ]

    if any(word in resume_text for word in education_keywords):
        score += 20
    else:
        issues.append("Education section missing")

    return score, issues