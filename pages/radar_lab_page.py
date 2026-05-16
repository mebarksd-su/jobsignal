import streamlit as st
import pandas as pd

from utils.ai_tools import (
    generate_resume_recommendations,
    calculate_match_score,
    detect_enhancement_keywords
)
from utils.skills_engine import (
    extract_skills,
    calculate_skill_frequency
)
from utils.semantic_matcher import calculate_semantic_match
from utils.smart_gap_analyzer import generate_gap_analysis
from utils.fit_classifier import classify_job_fit
from utils.action_plan_engine import generate_action_plan
from utils.analysis_storage import (
    save_latest_analysis,
    load_latest_analysis,
    save_analysis_to_history,
    load_analysis_history
)
from utils.skill_trend_engine import analyze_skill_trends
from utils.score_engine import calculate_final_fit_score
from utils.role_classifier import classify_role_type
from utils.critical_skills import ROLE_CRITICAL_SKILLS
from utils.rewrite_templates import generate_resume_bullet
from utils.resume_parser import extract_resume_text
from utils.section_parser import extract_skills_section
from utils.signal_strength import calculate_signal_strength
from utils.openai_client import (
    rewrite_resume_bullet_with_ai,
    summarize_job_description_with_ai,
    explain_resume_gaps_with_ai
)


def render_radar_lab_page():
    st.caption("Upload a resume, paste a job description, and let RoleRadar evaluate skill match, alignment, priority gaps, and improvement steps.")

    # -------------------------
    # RESUME MATCH SCORING
    # Compares resume content against the target job description.
    # -------------------------

    st.header("Role Match Scanner")

    resume_text = ""
    skills_section_found = False

    uploaded_resume = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
    )

    if uploaded_resume is not None:

        resume_parse_result = extract_resume_text(
            uploaded_resume
        )

        if not resume_parse_result["success"]:
            st.error(resume_parse_result["error"])
        else:
            extracted_resume = resume_parse_result["text"]

            skills_section = extract_skills_section(
                extracted_resume
            )

            if skills_section.strip() != "":
                resume_text = skills_section
                skills_section_found = True
                st.info("RoleRadar found and prioritized your resume skills section.")
            else:
                resume_text = extracted_resume
                skills_section_found = False
                st.warning(
                    "RoleRadar could not find a clear skills section, so it analyzed the full resume instead."
                )

            st.success("Resume uploaded successfully.")

            with st.expander("Preview Extracted Resume Text"):

                st.text_area(
                    "Full Extracted Resume Text",
                    extracted_resume,
                    height=300
                )


    match_job_description = st.text_area(
        "Paste Job Description for Match Score",
        height=200
    )

    match_button = st.button("Calculate Match Score")

    saved_analysis = load_latest_analysis()

    if match_button:
        if resume_text.strip() == "":
            st.error("Please upload a resume PDF before calculating a match score.")
            st.stop()

        if match_job_description.strip() == "":
            st.error("Please paste a job description before calculating a match score.")
            st.stop()

        (
            match_score,
            matched_skills,
            missing_skills,
            critical_matched,
            critical_missing
        ) = calculate_match_score(
            resume_text,
            match_job_description
        )
        semantic_score = calculate_semantic_match(
            resume_text,
            match_job_description
        )

        role_type = classify_role_type(match_job_description)
        critical_skills = ROLE_CRITICAL_SKILLS.get(role_type, [])

        missing_critical_skills = []

        for skill in critical_skills:
            if skill.lower() not in [
                s.lower() for s in matched_skills
            ]:
                missing_critical_skills.append(skill)

        final_fit_score = calculate_final_fit_score(
            match_score,
            semantic_score
        )
        signal_strength = calculate_signal_strength(
            matched_skills,
            missing_skills,
            skills_section_found,
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
            with st.spinner("RoleRadar is explaining your resume gaps..."):
                ai_gap_explanation = explain_resume_gaps_with_ai(
                    missing_skills,
                    matched_skills,
                    match_job_description
                )

        latest_analysis = {
            "match_score": match_score,
            "semantic_score": semantic_score,
            "role_type": role_type,
            "final_fit_score": final_fit_score,
            "signal_strength": signal_strength,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "smart_analysis": smart_analysis,
            "fit_analysis": fit_analysis,
            "action_plan": action_plan,
            "ai_gap_explanation": ai_gap_explanation
        }
        save_latest_analysis(latest_analysis)
        save_analysis_to_history(latest_analysis)

        st.session_state["latest_match_results"] = {
            "match_score": match_score,
            "semantic_score": semantic_score,
            "role_type": role_type,
            "final_fit_score": final_fit_score,
            "signal_strength": signal_strength,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "smart_analysis": smart_analysis,
            "fit_analysis": fit_analysis,
            "action_plan": action_plan,
            "ai_gap_explanation": ai_gap_explanation
        }

        st.subheader("Match Results")

        col1, col2, col3, col4, col5, col6 = st.columns(6)
        col1.metric("Skill Match", f"{match_score}%")
        col2.metric("Resume Alignment", f"{semantic_score}%")
        col3.metric("RadarScore", f"{final_fit_score}%")
        col4.metric("Radar Strength", f"{signal_strength['score']}%")
        col5.metric("Matched Skills", len(matched_skills))
        col6.metric("Missing Skills", len(missing_skills))

        st.info(f"Detected Role Type: {role_type}")
        st.info(
            f"Radar Strength: {signal_strength['label']} — {signal_strength['summary']}"
        )

        st.subheader("Priority Skill Analysis")

        col6, col7 = st.columns(2)
        col6.metric(
            "Priority Skills Matched",
            len(critical_matched)
        )
        col7.metric(
            "Priority Skills Missing",
            len(critical_missing)
        )

        st.subheader("Matched Skills")
        if matched_skills:
            for skill in matched_skills:
                st.write(f"• {skill}")
        else:
            st.write("No matching skills found.")

        st.subheader("Missing Skills")
        if missing_skills:
            for skill in missing_skills:
                st.write(f"• {skill}")
        else:
            st.write("No missing skills detected.")

        # =========================
        # RESUME IMPROVEMENT SUGGESTIONS
        # Generates realistic resume bullet ideas
        # based on missing skills.
        # =========================

        st.subheader("Suggested Resume Bullets")

        if missing_skills:
            for skill in missing_skills:
                suggested_bullet = generate_resume_bullet(skill)
                st.success(
                    f"{skill}: {suggested_bullet}"
                )
        else:
            st.write("No resume improvement suggestions needed right now.")

        # =========================
        # PRIORITY SKILL GAPS
        # Highlights the most important missing skills for the detected role.
        # =========================

        st.subheader("Priority Skill Gaps")

        if critical_missing:
            for skill in critical_missing:
                st.error(
                    f"{skill}: This is a higher-priority gap for this type of role. "
                    "Consider adding a project, bullet, or experience that demonstrates this skill."
                )
        else:
            st.write("No priority skill gaps detected.")

        st.subheader("AI Gap Explanation")

        if missing_skills:
            if ai_gap_explanation["success"]:
                st.info(ai_gap_explanation["result"])
            else:
                st.warning(ai_gap_explanation["error"])
        else:
            st.write("No AI gap explanation needed because no missing skills were detected.")

        st.subheader("Radar Insights")
        for insight in smart_analysis:
            st.info(insight)

        st.subheader("Fit Summary")
        st.info(f"Radar Status: {fit_analysis['label']}")
        st.write(f"Summary: {fit_analysis['summary']}")
        st.write(f"Effort Needed: {fit_analysis['effort_level']}")
        st.write(f"Recommended Next Step: {fit_analysis['next_action']}")

        
        st.subheader("Resume Action Plan")

        for item in action_plan:

            st.markdown(f"### {item['title']}")

            st.write("**Why This Matters**")
            st.write(item["why_it_matters"])

            st.write("**Suggested Improvement**")
            st.write(item["suggested_project"])

            st.write("**Skills You’ll Gain**")

            for skill in item["skills_gained"]:
                st.write(f"• {skill}")

            st.write("**Resources**")

            for resource in item["resources"]:
                st.markdown(
                    f"- [{resource['title']}]({resource['url']}) ({resource['type']})"
                )

            st.write(f"**Difficulty:** {item['difficulty']}")
            st.write(f"**Estimated Time:** {item['estimated_time']}")

            st.divider()

        st.subheader("Overall Recommendation")

        if final_fit_score >= 80:
            st.success("Strong alignment. This resume appears well matched to the role.")
        elif final_fit_score >= 50:
            st.warning("Moderate alignment. Strengthen the resume language before applying.")
        else:
            st.error("Needs more role evidence. This resume may need clearer role-specific skills before applying.")

    elif saved_analysis:

        match_score = saved_analysis["match_score"]
        semantic_score = saved_analysis["semantic_score"]
        final_fit_score = saved_analysis.get("final_fit_score", match_score)
        signal_strength = saved_analysis.get(
            "signal_strength",
            {
                "label": "Not Available",
                "score": 0,
                "summary": "Radar Strength was not saved for this older analysis."
            }
        )

        st.subheader("Latest Saved Match Snapshot")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Skill Match", f"{match_score}%")
        col2.metric("Resume Alignment", f"{semantic_score}%")
        col3.metric("RadarScore", f"{final_fit_score}%")
        col4.metric("Radar Strength", f"{signal_strength['score']}%")

        st.info(
            "This is your most recent saved score snapshot. "
            "Upload a resume and paste a new job description to generate a fresh role-specific analysis."
        )
    # -------------------------
    # ANALYSIS HISTORY VIEWER
    # Shows saved resume analysis history and score trends.
    # -------------------------

    st.header("Resume Analysis History")
    st.caption("Review previous resume analyses, score trends, and repeated skill gaps.")

    analysis_history = load_analysis_history()
    skill_trends = analyze_skill_trends(
        analysis_history
    )

    if len(analysis_history) > 0:

        total_analyses = len(analysis_history)

        match_scores = [
            record["analysis"].get(
                "final_fit_score",
                record["analysis"]["match_score"]
            )
            for record in analysis_history
        ]

        semantic_scores = [
            record["analysis"]["semantic_score"]
            for record in analysis_history
        ]

        latest_record = analysis_history[-1]
        latest_score = latest_record["analysis"].get(
            "final_fit_score",
            latest_record["analysis"]["match_score"]
        )
        best_score = max(match_scores)
        average_score = round(sum(match_scores) / len(match_scores), 1)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Saved Analyses", total_analyses)
        col2.metric("Latest RadarScore", f"{latest_score}%")
        col3.metric("Best RadarScore", f"{best_score}%")
        col4.metric("Average RadarScore", f"{average_score}%")

        all_missing_skills = []

        st.subheader("Top Resume Strengths")

        if len(skill_trends["trending_strengths"]) > 0:

            for skill, count in skill_trends["trending_strengths"]:
                st.success(
                    f"{skill} appeared as a matched skill in {count} analyses."
                )
        
        st.subheader("Top Skill Gaps")

        if len(skill_trends["trending_missing"]) > 0:

            for skill, count in skill_trends["trending_missing"]:
                st.warning(
                    f"{skill} appeared as a missing skill in {count} analyses."
                )

        for record in analysis_history:
            all_missing_skills.extend(
                record["analysis"]["missing_skills"]
            )

        if len(all_missing_skills) > 0:
            missing_skill_counts = pd.Series(all_missing_skills).value_counts()

            st.subheader("Most Common Missing Skills")
            st.bar_chart(missing_skill_counts)

        st.subheader("Recent Analysis History")

        history_rows = []

        for record in analysis_history[-5:]:
            history_rows.append({
                "Timestamp": record["timestamp"],
                "Final Fit Score": record["analysis"].get(
                    "final_fit_score",
                    record["analysis"]["match_score"]
                ),
                "Semantic Score": record["analysis"]["semantic_score"],
                "Matched Skills": len(record["analysis"]["matched_skills"]),
                "Missing Skills": len(record["analysis"]["missing_skills"])
            })

        history_df = pd.DataFrame(history_rows)

        st.dataframe(
            history_df,
            width="stretch",
            hide_index=True
            
        )

    else:
        st.info("No resume analyses saved yet.")

    # -------------------------
    # JOB DESCRIPTION ANALYZER
    # Detects skills and recommends resume focus areas.
    # -------------------------

    st.header("Job Description Radar")
    st.caption("Use this when you want to inspect a job description without running a full resume match.")

    job_description = st.text_area(
        "Paste Job Description",
        height=250
    )

    analyze_button = st.button("Analyze Job Description")

    if analyze_button:
        detected_skills = extract_skills(job_description)

        st.subheader("Detected Skills")

        if detected_skills:
            for item in detected_skills:
                st.write(
                    f"• {item['display_skill']} ({item['category']})"
                )
        else:
            st.write("No matching skills detected.")

        st.subheader("Skill Frequency Analysis")

        skill_frequency = calculate_skill_frequency(
            detected_skills
        )
        for skill, count in skill_frequency.items():
            st.write(f"• {skill}: {count}")    

        st.subheader("AI Job Description Summary")

        with st.spinner("RoleRadar is summarizing this job description..."):
            jd_summary = summarize_job_description_with_ai(job_description)

        if jd_summary["success"]:
            st.info(jd_summary["result"])
        else:
            st.error(jd_summary["error"])

        st.subheader("Recommended Resume Focus")

        resume_recommendations = generate_resume_recommendations(detected_skills)

        for recommendation in resume_recommendations:
            st.write(f"• {recommendation}")

    # -------------------------
    # RESUME BULLET REWRITER
    # Strengthens resume bullets and improves role alignment.
    # -------------------------

    st.header("Rewrite a Resume Bullet")

    original_bullet = st.text_area(
        "Paste Resume Bullet",
        height=150
    )

    target_job_description = st.text_area(
        "Paste Target Job Description",
        height=200
    )

    enhance_button = st.button("Enhance Resume Bullet")

    if enhance_button:

        with st.spinner("RoleRadar is rewriting your bullet..."):
            ai_result = rewrite_resume_bullet_with_ai(
                original_bullet,
                target_job_description
            )

        if ai_result["success"]:

            improved_bullet = ai_result["result"]

            keyword_matches = detect_enhancement_keywords(
                target_job_description
            )

            st.subheader("AI-Enhanced Resume Bullet")
            st.success(improved_bullet)

            st.subheader("Detected Resume Keywords")

            if keyword_matches:
                for keyword in keyword_matches:
                    st.write(f"• {keyword}")
            else:
                st.write("No major keyword matches detected from the job description.")

        else:
            st.error(ai_result["error"])