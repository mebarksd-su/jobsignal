# =========================
# RESUME REWRITE TEMPLATES
# Stores skill-specific resume bullet suggestions.
# This file helps JobSignal turn missing skills into practical resume improvements.
# =========================


REWRITE_TEMPLATES = {

    "power bi": [
        "Built Power BI dashboards to track key performance indicators, summarize trends, and communicate business insights to stakeholders."
    ],

    "tableau": [
        "Created Tableau dashboards to visualize business performance, identify trends, and support data-driven decision-making."
    ],

    "dashboarding": [
        "Developed interactive dashboards to monitor performance metrics, simplify reporting, and communicate insights to non-technical audiences."
    ],

    "sql": [
        "Used SQL to query, clean, and analyze structured datasets in support of reporting and business intelligence workflows."
    ],

    "python": [
        "Applied Python to clean datasets, automate analysis workflows, and generate insights from structured data."
    ],

    "data analysis": [
        "Analyzed datasets to identify trends, summarize findings, and support data-informed decision-making."
    ],

    "machine learning": [
        "Built machine learning models to identify patterns, evaluate predictions, and support data-driven problem solving."
    ],

    "artificial intelligence": [
        "Applied AI tools and techniques to support automation, analysis, and workflow improvement."
    ],

    "aws": [
        "Used AWS services to support cloud-based data storage, deployment, and scalable analytics workflows."
    ],

    "communication": [
        "Communicated technical findings clearly through documentation, presentations, and collaboration with cross-functional teams."
    ],

    "stakeholder management": [
        "Collaborated with stakeholders to gather requirements, explain findings, and align analysis with business goals."
    ],

    "documentation": [
        "Created clear technical documentation to explain workflows, summarize findings, and support repeatable processes."
    ],

    "workflow automation": [
        "Built automated workflows to reduce manual tasks, improve efficiency, and support repeatable data processes."
    ]
}


def generate_resume_bullet(skill):

    skill_lower = skill.lower()

    if skill_lower in REWRITE_TEMPLATES:
        return REWRITE_TEMPLATES[skill_lower][0]

    return (
        f"Developed experience with {skill} through project-based work, "
        "technical problem-solving, and applied analysis."
    )