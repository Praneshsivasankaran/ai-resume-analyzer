import re


ACTION_VERBS = [
    "improved", "increased", "reduced", "optimized", "developed",
    "built", "designed", "led", "implemented", "launched", "shipped",
    "delivered", "architected", "automated", "scaled", "migrated",
    "refactored", "deployed", "created", "established", "managed",
    "mentored", "collaborated", "analyzed", "engineered", "accelerated",
    "streamlined", "achieved", "drove", "spearheaded", "pioneered",
]


def analyze_impact(resume_text):
    score = 0
    feedback = []
    text_lower = resume_text.lower()

    percentages = re.findall(r'\d+\s*%', resume_text)
    numbers = re.findall(r'\b\d{2,}\b', resume_text)
    money = re.findall(r'\$\s?\d+', resume_text)

    action_count = sum(1 for v in ACTION_VERBS if v in text_lower)

    metric_count = len(percentages) + len(money) + len(numbers)

    if metric_count >= 5:
        score += 50
    elif metric_count >= 2:
        score += 35
    else:
        feedback.append("Add more measurable achievements with numbers, percentages, or dollar amounts.")

    if action_count >= 5:
        score += 50
    elif action_count >= 2:
        score += 35
    else:
        feedback.append("Use stronger action verbs (e.g. 'improved', 'optimized', 'led', 'shipped').")

    return int(score), feedback