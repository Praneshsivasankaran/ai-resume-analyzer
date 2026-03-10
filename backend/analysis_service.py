from concurrent.futures import ThreadPoolExecutor

from resume_parser import extract_text
from keyword_engine import keyword_match_score
from ats_checker import check_ats_rules
from impact_analyzer import analyze_impact
from skills_engine import calculate_skills_score
from structure_engine import analyze_structure
from scoring_engine import calculate_final_score
from suggestion_engine import generate_suggestions


def analyze_resume(file_path, jd_text):

    # ---- Extract Resume Text ----
    resume_text = extract_text(file_path)

    # ---- Limit text size (prevents slow processing) ----
    resume_text = resume_text[:8000]
    jd_text = jd_text[:4000]

    # ---- Run Analysis Engines in Parallel ----
    with ThreadPoolExecutor() as executor:

        keyword_future = executor.submit(keyword_match_score, resume_text, jd_text)
        ats_future = executor.submit(check_ats_rules, resume_text)
        impact_future = executor.submit(analyze_impact, resume_text)
        skills_future = executor.submit(calculate_skills_score, resume_text, jd_text)
        structure_future = executor.submit(analyze_structure, resume_text)

        keyword_score, similarity, missing_keywords = keyword_future.result()
        ats_score, ats_issues = ats_future.result()
        impact_score, impact_feedback = impact_future.result()
        skills_score, missing_skills = skills_future.result()
        structure_score, structure_feedback = structure_future.result()

    # ---- Grammar Engine Disabled (Too Slow) ----
    grammar_score = 10
    grammar_errors = []
    grammar_feedback = []

    # ---- Final Score ----
    final_score = calculate_final_score(
        keyword_score=keyword_score,
        ats_score=ats_score,
        impact_score=impact_score,
        skills_score=skills_score,
        structure_score=structure_score,
        grammar_score=grammar_score
    )

    # ---- Breakdown Dictionary ----
    breakdown = {
        "keyword": keyword_score,
        "ats": ats_score,
        "impact": impact_score,
        "skills": skills_score,
        "structure": structure_score,
        "grammar": grammar_score
    }

    # ---- Generate Suggestions ----
    suggestions = generate_suggestions(
        breakdown=breakdown,
        missing_keywords=missing_keywords,
        missing_skills=missing_skills,
        ats_issues=ats_issues,
        impact_feedback=impact_feedback,
        structure_feedback=structure_feedback,
        grammar_feedback=grammar_feedback
    )

    # ---- Final Response ----
    return {
        "total_score": final_score,
        "breakdown": breakdown,
        "missing_keywords": missing_keywords,
        "missing_skills": missing_skills,
        "ats_issues": ats_issues,
        "impact_feedback": impact_feedback,
        "structure_feedback": structure_feedback,
        "grammar_feedback": grammar_feedback,
        "suggestions": suggestions
    }