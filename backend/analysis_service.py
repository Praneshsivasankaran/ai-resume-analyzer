from resume_parser import extract_text
from keyword_engine import keyword_match_score
from ats_checker import check_ats_rules
from impact_analyzer import analyze_impact
from skills_engine import calculate_skills_score
from structure_engine import analyze_structure
from grammar_engine import analyze_grammar
from scoring_engine import calculate_final_score
from suggestion_engine import generate_suggestions


def analyze_resume(file_path, jd_text):

    resume_text = extract_text(file_path)

    # ---- Engines ----
    keyword_score, similarity, missing_keywords = keyword_match_score(
        resume_text, jd_text
    )

    ats_score, ats_issues = check_ats_rules(resume_text)

    impact_score, impact_feedback = analyze_impact(resume_text)

    skills_score, missing_skills = calculate_skills_score(
        resume_text, jd_text
    )

    structure_score, structure_feedback = analyze_structure(resume_text)

    grammar_score, grammar_errors, grammar_feedback = analyze_grammar(
        resume_text
    )

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