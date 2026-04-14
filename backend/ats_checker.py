import re


def check_ats_rules(resume_text):
    score = 0
    issues = []
    text_lower = resume_text.lower()

    # Email
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', resume_text):
        score += 20
    else:
        issues.append("Email not found")

    # Phone — accept 10+ digits with common separators
    phone_pattern = r'(\+?\d{1,3}[\s.-]?)?(\(?\d{3,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}'
    phones = re.findall(phone_pattern, resume_text)
    # Filter out junk by requiring the raw text to have >=10 consecutive digit-ish chars somewhere
    digit_runs = re.findall(r'[\d\s\-().+]{10,}', resume_text)
    if digit_runs and any(sum(c.isdigit() for c in run) >= 10 for run in digit_runs):
        score += 20
    else:
        issues.append("Phone number not found")

    experience_keywords = ["experience", "work history", "professional experience", "project", "projects", "employment"]
    if any(k in text_lower for k in experience_keywords):
        score += 20
    else:
        issues.append("Experience section missing")

    skills_keywords = ["skills", "technical skills", "core competencies", "technologies"]
    if any(k in text_lower for k in skills_keywords):
        score += 20
    else:
        issues.append("Skills section missing")

    education_keywords = ["education", "academic", "qualifications", "university", "college", "degree"]
    if any(k in text_lower for k in education_keywords):
        score += 20
    else:
        issues.append("Education section missing")

    return score, issues