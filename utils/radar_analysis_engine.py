from utils.ai_tools import calculate_match_score

from utils.semantic_matcher import calculate_semantic_match
from utils.smart_gap_analyzer import generate_gap_analysis
from utils.fit_classifier import classify_job_fit
from utils.action_plan_engine import generate_action_plan
from utils.score_engine import calculate_final_fit_score
from utils.role_classifier import classify_role_type
from utils.critical_skills import ROLE_CRITICAL_SKILLS
from utils.signal_strength import calculate_signal_strength
from utils.openai_client import explain_resume_gaps_with_ai


def run_radar_analysis(resume_text, target_job_description):

    semantic_score = calculate_semantic_match(
        resume_text,
        target_job_description
    )

    (
        match_score,
        matched_skills,
        missing_skills,
        critical_matched,
        critical_missing
    ) = calculate_match_score(
        resume_text,
        target_job_description
    )

    if isinstance(match_score, dict):
        match_score = match_score.get("score", 0)

    role_type = classify_role_type(
        target_job_description
    )

    critical_skills = ROLE_CRITICAL_SKILLS.get(
        role_type,
        []
    )

    final_fit_score = calculate_final_fit_score(
        match_score,
        semantic_score
    )

    signal_strength = calculate_signal_strength(
        matched_skills,
        missing_skills,
        True,
        semantic_score
    )

    smart_analysis = generate_gap_analysis(
        matched_skills,
        missing_skills,
        semantic_score
    )

    fit_analysis = classify_job_fit(
        match_score,
        semantic_score,
        matched_skills,
        missing_skills
    )

    action_plan = generate_action_plan(
        fit_analysis,
        missing_skills,
        semantic_score
    )

    ai_gap_explanation = {
        "success": False,
        "result": "",
        "error": "No AI gap explanation generated."
    }

    if missing_skills:
        ai_gap_explanation = explain_resume_gaps_with_ai(
            missing_skills,
            matched_skills,
            target_job_description
        )

    return {
        "match_score": match_score,
        "semantic_score": semantic_score,
        "signal_strength_score": signal_strength,
        "final_fit_score": final_fit_score,
        "detected_role_type": role_type,
        "critical_skills": critical_skills,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "critical_matched": critical_matched,
        "critical_missing": critical_missing,
        "smart_analysis": smart_analysis,
        "fit_analysis": fit_analysis,
        "action_plan": action_plan,
        "ai_gap_explanation": ai_gap_explanation
    }