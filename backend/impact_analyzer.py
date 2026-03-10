import re


def analyze_impact(resume_text):

    score = 0
    feedback = []

    # 1️⃣ Percentage detection
    percentage_pattern = r'\d+%'
    percentages = re.findall(percentage_pattern, resume_text)

    # 2️⃣ Number detection (basic metrics)
    number_pattern = r'\b\d{2,}\b'
    numbers = re.findall(number_pattern, resume_text)

    # 3️⃣ Action verbs detection
    action_verbs = [
        "improved", "increased", "reduced",
        "optimized", "developed", "built",
        "designed", "led", "implemented"
    ]

    action_count = sum(word in resume_text for word in action_verbs)

    # Scoring logic
    metric_count = len(percentages) + len(numbers)

    if metric_count >= 5:
        score += 50
    elif metric_count >= 2:
        score += 30
    else:
        feedback.append("Add more measurable achievements with numbers or percentages")

    if action_count >= 3:
        score += 50
    elif action_count >= 1:
        score += 30
    else:
        feedback.append("Use strong action verbs like 'improved', 'optimized', 'built'")

    return score, feedback