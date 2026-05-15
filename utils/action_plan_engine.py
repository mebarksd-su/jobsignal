def generate_action_plan(fit_analysis, missing_skills, semantic_score):

    action_plan = []

    tailoring_level = fit_analysis["tailoring_level"]

    missing_skills_lower = [
        skill.lower() for skill in missing_skills
    ]

    # -------------------------
    # Resume Wording Plan
    # -------------------------

    if semantic_score < 40:
        action_plan.append({
            "title": "Improve Resume Wording Alignment",
            "why_it_matters": (
                "Your resume includes some relevant skills, but the wording does not closely match the job description. "
                "Applicant tracking systems and recruiters often look for language that clearly reflects the role's responsibilities."
            ),
            "suggested_project": (
                "Rewrite 2 to 3 resume bullets using phrases from the job description while keeping the bullets honest and based on real experience."
            ),
            "skills_gained": [
                "Resume tailoring",
                "ATS optimization",
                "Professional writing"
            ],
            "resources": [
                {
                    "title": "Harvard Resume and Cover Letter Guide",
                    "type": "guide",
                    "url": "https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/"
                },
                {
                    "title": "Indeed Resume Keywords Guide",
                    "type": "article",
                    "url": "https://www.indeed.com/career-advice/resumes-cover-letters/resume-keywords"
                }
            ],
            "difficulty": "Beginner",
            "estimated_time": "30 to 60 minutes"
        })

    # -------------------------
    # Communication Plan
    # -------------------------

    if "communication" in missing_skills_lower:
        action_plan.append({
            "title": "Add Communication Evidence",
            "why_it_matters": (
                "This role emphasizes communication, collaboration, or stakeholder interaction. "
                "A technical resume can look incomplete if it only lists tools without showing how you explained results or worked with others."
            ),
            "suggested_project": (
                "Add a bullet showing a time you explained data, documented a process, presented findings, worked with a team, or supported a non-technical audience."
            ),
            "skills_gained": [
                "Professional communication",
                "Stakeholder collaboration",
                "Documentation"
            ],
            "resources": [
                {
                    "title": "Google Technical Writing Course",
                    "type": "course",
                    "url": "https://developers.google.com/tech-writing"
                }
            ],
            "difficulty": "Beginner",
            "estimated_time": "30 minutes"
        })

    # -------------------------
    # Cloud Plan
    # -------------------------

    if "cloud" in missing_skills_lower or "aws" in missing_skills_lower:
        action_plan.append({
            "title": "Build a Cloud Deployment Project",
            "why_it_matters": (
                "The job description mentions cloud or AWS skills. "
                "Even a small deployed project can show that you understand how applications move from your laptop to a real hosted environment."
            ),
            "suggested_project": (
                "Deploy your JobSignal Streamlit app or another small analytics dashboard using AWS EC2, Streamlit Community Cloud, or Render."
            ),
            "skills_gained": [
                "AWS basics",
                "Cloud deployment",
                "Environment variables",
                "Application hosting"
            ],
            "resources": [
                {
                    "title": "AWS EC2 Getting Started",
                    "type": "documentation",
                    "url": "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html"
                },
                {
                    "title": "Streamlit App Deployment Guide",
                    "type": "documentation",
                    "url": "https://docs.streamlit.io/deploy"
                },
                {
                    "title": "Render Python App Deployment",
                    "type": "documentation",
                    "url": "https://render.com/docs/deploy-python"
                }
            ],
            "difficulty": "Intermediate",
            "estimated_time": "1 to 2 weekends"
        })

    # -------------------------
    # Automation Plan
    # -------------------------

    if "automation" in missing_skills_lower:
        action_plan.append({
            "title": "Create an Automation Workflow Project",
            "why_it_matters": (
                "Automation appears in the job description, which means the employer likely values reducing manual work and improving efficiency."
            ),
            "suggested_project": (
                "Build a Python script that reads a CSV, cleans the data, generates a summary report, and exports a finished file automatically."
            ),
            "skills_gained": [
                "Python scripting",
                "Workflow automation",
                "Data cleaning",
                "Process improvement"
            ],
            "resources": [
                {
                    "title": "Automate the Boring Stuff with Python",
                    "type": "book",
                    "url": "https://automatetheboringstuff.com/"
                },
                {
                    "title": "Pandas Getting Started",
                    "type": "documentation",
                    "url": "https://pandas.pydata.org/docs/getting_started/index.html"
                }
            ],
            "difficulty": "Beginner to Intermediate",
            "estimated_time": "1 weekend"
        })

    # -------------------------
    # SQL Plan
    # -------------------------

    if "sql" in missing_skills_lower:
        action_plan.append({
            "title": "Strengthen SQL Project Evidence",
            "why_it_matters": (
                "SQL is a core skill for many data, analytics, and business intelligence roles. "
                "If a job asks for SQL, recruiters want to see proof that you can query, filter, join, and summarize structured data."
            ),
            "suggested_project": (
                "Create a small SQL project using a public dataset. Write queries that answer business questions, then summarize the results in a short README."
            ),
            "skills_gained": [
                "SQL querying",
                "Joins",
                "Aggregations",
                "Business analysis"
            ],
            "resources": [
                {
                    "title": "SQLBolt Interactive Lessons",
                    "type": "interactive practice",
                    "url": "https://sqlbolt.com/"
                },
                {
                    "title": "Kaggle Datasets",
                    "type": "dataset library",
                    "url": "https://www.kaggle.com/datasets"
                }
            ],
            "difficulty": "Beginner to Intermediate",
            "estimated_time": "1 weekend"
        })

    # -------------------------
    # Python Plan
    # -------------------------

    if "python" in missing_skills_lower:
        action_plan.append({
            "title": "Build a Python Analytics Project",
            "why_it_matters": (
                "Python is one of the most common technical requirements for analytics and AI-related internships. "
                "A project gives recruiters concrete proof that you can use Python beyond classroom exercises."
            ),
            "suggested_project": (
                "Build a Python project that loads a dataset, cleans it with pandas, creates charts, and explains the findings in a README."
            ),
            "skills_gained": [
                "Python",
                "Pandas",
                "Data cleaning",
                "Data visualization"
            ],
            "resources": [
                {
                    "title": "Pandas Getting Started",
                    "type": "documentation",
                    "url": "https://pandas.pydata.org/docs/getting_started/index.html"
                },
                {
                    "title": "Matplotlib Tutorials",
                    "type": "documentation",
                    "url": "https://matplotlib.org/stable/tutorials/index.html"
                }
            ],
            "difficulty": "Beginner to Intermediate",
            "estimated_time": "1 to 2 weekends"
        })

    # -------------------------
    # Final Fallback Plan
    # -------------------------

    if len(action_plan) == 0:
        action_plan.append({
            "title": "Polish Resume Impact",
            "why_it_matters": (
                "Your resume already shows solid alignment with this role. "
                "The next improvement is making your experience more specific, measurable, and outcome-driven."
            ),
            "suggested_project": (
                "Update 3 resume bullets by adding measurable results, tools used, project context, or business impact."
            ),
            "skills_gained": [
                "Resume optimization",
                "Impact writing",
                "Professional positioning"
            ],
            "resources": [
                {
                    "title": "Harvard Resume and Cover Letter Guide",
                    "type": "guide",
                    "url": "https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/"
                }
            ],
            "difficulty": "Beginner",
            "estimated_time": "30 minutes"
        })

    return action_plan