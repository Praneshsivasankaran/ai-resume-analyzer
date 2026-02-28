import language_tool_python
import re


def analyze_grammar(resume_text):

    tool = language_tool_python.LanguageTool('en-US')

    lines = resume_text.split("\n")

    meaningful_lines = []

    for line in lines:
        words = line.strip().split()

        # Ignore short bullet fragments
        if len(words) < 7:
            continue

        # Ignore tech-heavy lines
        tech_indicators = [
            "python", "java", "aws", "docker",
            "api", "ml", "fastapi", "tensorflow",
            "scikit", "huggingface"
        ]

        if any(word in line for word in tech_indicators):
            continue

        meaningful_lines.append(line.strip())

    error_count = 0

    for line in meaningful_lines:
        matches = tool.check(line)
        error_count += len(matches)

    feedback = []

    # Resume-calibrated scoring (soft penalty)
    if error_count <= 10:
        score = 95
    elif error_count <= 25:
        score = 85
    elif error_count <= 50:
        score = 75
    else:
        score = 70
        feedback.append("Minor grammar refinements recommended")

    return score, error_count, feedback