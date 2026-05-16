def build_resource(title, resource_type, url):
    return {
        "title": title,
        "type": resource_type,
        "url": url
    }


def has_any_skill(missing_skills_lower, skill_terms):
    return any(skill in missing_skills_lower for skill in skill_terms)


def generate_action_plan(fit_analysis, missing_skills, semantic_score):

    action_plan = []

    effort_level = fit_analysis.get(
        "effort_level",
        fit_analysis.get("tailoring_level", "Unknown")
    )
    # Supports both old and new fit analysis naming conventions.

    missing_skills_lower = [
        skill.lower() for skill in missing_skills
    ]

    # -------------------------
    # Resume Wording Plan
    # -------------------------

    if semantic_score < 40:
        action_plan.append({
            "title": "Make Your Resume Match the Role Better",
            "why_it_matters": (
                "Your resume may include relevant experience, but the wording does not clearly mirror the job description yet. "
                "Recruiters and screening tools need to quickly see how your background connects to the role."
            ),
            "suggested_project": (
                "Rewrite 2 to 3 resume bullets using language from the job description while keeping the experience truthful. "
                "Focus on tools used, outcomes, responsibilities, and who benefited from the work."
            ),
            "skills_gained": [
                "Resume writing",
                "Role alignment",
                "Professional positioning"
            ],
            "resources": [
                build_resource(
                    "Harvard Resume and Cover Letter Guide",
                    "guide",
                    "https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/"
                ),
                build_resource(
                    "Indeed Resume Keywords Guide",
                    "article",
                    "https://www.indeed.com/career-advice/resumes-cover-letters/resume-keywords"
                ),
                build_resource(
                    "YouTube: Resume Bullet Writing for Internships",
                    "video search",
                    "https://www.youtube.com/results?search_query=resume+bullet+writing+for+internships"
                ),
                build_resource(
                    "TikTok: Resume Bullet Examples",
                    "short-form video search",
                    "https://www.tiktok.com/search?q=resume%20bullet%20examples%20for%20students"
                )
            ],
            "difficulty": "Beginner",
            "estimated_time": "30 to 60 minutes"
        })

    # -------------------------
    # Communication / Stakeholder Plan
    # -------------------------

    if has_any_skill(missing_skills_lower, [
        "communication",
        "stakeholder management",
        "stakeholder",
        "stakeholders",
        "presentation",
        "presentations",
        "collaboration"
    ]):
        action_plan.append({
            "title": "Show Communication and Stakeholder Evidence",
            "why_it_matters": (
                "This role values communication, collaboration, or stakeholder work. "
                "A technical resume is stronger when it shows that you can explain findings, document work, and support people who are not technical."
            ),
            "suggested_project": (
                "Add or rewrite one bullet showing how you presented findings, documented a process, worked with a team, or explained data to someone else."
            ),
            "skills_gained": [
                "Professional communication",
                "Stakeholder collaboration",
                "Documentation",
                "Presentations"
            ],
            "resources": [
                build_resource(
                    "Google Technical Writing Course",
                    "course",
                    "https://developers.google.com/tech-writing"
                ),
                build_resource(
                    "YouTube: How to Present Data Insights",
                    "video search",
                    "https://www.youtube.com/results?search_query=how+to+present+data+insights+to+stakeholders"
                ),
                build_resource(
                    "TikTok: Presentation Tips for Students",
                    "short-form video search",
                    "https://www.tiktok.com/search?q=presentation%20tips%20for%20students"
                )
            ],
            "difficulty": "Beginner",
            "estimated_time": "30 to 45 minutes"
        })

    # -------------------------
    # Dashboard / BI Plan
    # -------------------------

    if has_any_skill(missing_skills_lower, [
        "dashboarding",
        "dashboard",
        "dashboards",
        "power bi",
        "tableau",
        "business intelligence",
        "data visualization",
        "metrics",
        "reporting"
    ]):
        action_plan.append({
            "title": "Build a Dashboard Project",
            "why_it_matters": (
                "Dashboarding and business intelligence skills are important for analytics roles because they show that you can turn data into something useful for decision-making."
            ),
            "suggested_project": (
                "Create a dashboard using a public dataset. Track 4 to 6 key metrics, add filters, and write a short README explaining the business question and insights."
            ),
            "skills_gained": [
                "Dashboarding",
                "Business intelligence",
                "Data visualization",
                "KPI reporting"
            ],
            "resources": [
                build_resource(
                    "Microsoft Learn: Power BI Learning Path",
                    "course",
                    "https://learn.microsoft.com/en-us/training/powerplatform/power-bi"
                ),
                build_resource(
                    "Tableau Free Training Videos",
                    "course",
                    "https://www.tableau.com/learn/training"
                ),
                build_resource(
                    "YouTube: Power BI Dashboard Project for Beginners",
                    "video search",
                    "https://www.youtube.com/results?search_query=power+bi+dashboard+project+for+beginners"
                ),
                build_resource(
                    "YouTube: Tableau Dashboard Project for Beginners",
                    "video search",
                    "https://www.youtube.com/results?search_query=tableau+dashboard+project+for+beginners"
                ),
                build_resource(
                    "TikTok: Power BI Dashboard Tips",
                    "short-form video search",
                    "https://www.tiktok.com/search?q=power%20bi%20dashboard%20tips"
                )
            ],
            "difficulty": "Beginner to Intermediate",
            "estimated_time": "1 weekend"
        })

    # -------------------------
    # Excel Plan
    # -------------------------

    if has_any_skill(missing_skills_lower, [
        "excel",
        "microsoft excel"
    ]):
        action_plan.append({
            "title": "Strengthen Excel Evidence",
            "why_it_matters": (
                "Excel is still one of the most common tools in internships and entry-level business roles. "
                "Showing pivot tables, formulas, charts, or spreadsheet analysis can make your resume more practical and job-ready."
            ),
            "suggested_project": (
                "Build a simple Excel analysis using a public dataset. Include pivot tables, formulas, charts, and a short summary of your findings."
            ),
            "skills_gained": [
                "Excel",
                "Pivot tables",
                "Spreadsheet analysis",
                "Reporting"
            ],
            "resources": [
                build_resource(
                    "Microsoft Excel Training",
                    "course",
                    "https://support.microsoft.com/en-us/excel"
                ),
                build_resource(
                    "YouTube: Excel Pivot Table Tutorial for Beginners",
                    "video search",
                    "https://www.youtube.com/results?search_query=excel+pivot+table+tutorial+for+beginners"
                ),
                build_resource(
                    "TikTok: Excel Tips for Beginners",
                    "short-form video search",
                    "https://www.tiktok.com/search?q=excel%20tips%20for%20beginners"
                )
            ],
            "difficulty": "Beginner",
            "estimated_time": "2 to 4 hours"
        })

    # -------------------------
    # Cloud Plan
    # -------------------------

    if has_any_skill(missing_skills_lower, [
        "cloud",
        "aws",
        "azure",
        "gcp",
        "cloud deployment"
    ]):
        action_plan.append({
            "title": "Deploy a Small Cloud Project",
            "why_it_matters": (
                "The job description mentions cloud or deployment skills. "
                "Even a small hosted project shows that you understand how applications move from your laptop to a real environment."
            ),
            "suggested_project": (
                "Deploy a small Streamlit dashboard, portfolio app, or analytics project using Streamlit Community Cloud, Render, AWS, or another beginner-friendly platform."
            ),
            "skills_gained": [
                "Cloud deployment",
                "Environment variables",
                "Application hosting",
                "Production basics"
            ],
            "resources": [
                build_resource(
                    "Streamlit App Deployment Guide",
                    "documentation",
                    "https://docs.streamlit.io/deploy"
                ),
                build_resource(
                    "Render Python App Deployment",
                    "documentation",
                    "https://render.com/docs/deploy-python"
                ),
                build_resource(
                    "AWS EC2 Getting Started",
                    "documentation",
                    "https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/EC2_GetStarted.html"
                ),
                build_resource(
                    "YouTube: Deploy Streamlit App Tutorial",
                    "video search",
                    "https://www.youtube.com/results?search_query=deploy+streamlit+app+tutorial"
                )
            ],
            "difficulty": "Intermediate",
            "estimated_time": "1 to 2 weekends"
        })

    # -------------------------
    # Automation Plan
    # -------------------------

    if has_any_skill(missing_skills_lower, [
        "automation",
        "workflow automation",
        "scripting",
        "data automation",
        "process improvement"
    ]):
        action_plan.append({
            "title": "Create an Automation Workflow Project",
            "why_it_matters": (
                "Automation shows that you can reduce manual work and improve efficiency, which is valuable in data, operations, IT, and business roles."
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
                build_resource(
                    "Automate the Boring Stuff with Python",
                    "book",
                    "https://automatetheboringstuff.com/"
                ),
                build_resource(
                    "Pandas Getting Started",
                    "documentation",
                    "https://pandas.pydata.org/docs/getting_started/index.html"
                ),
                build_resource(
                    "YouTube: Python Automation Project for Beginners",
                    "video search",
                    "https://www.youtube.com/results?search_query=python+automation+project+for+beginners"
                ),
                build_resource(
                    "TikTok: Python Automation Ideas",
                    "short-form video search",
                    "https://www.tiktok.com/search?q=python%20automation%20ideas"
                )
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
                "Recruiters want to see proof that you can query, filter, join, and summarize structured data."
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
                build_resource(
                    "SQLBolt Interactive Lessons",
                    "interactive practice",
                    "https://sqlbolt.com/"
                ),
                build_resource(
                    "Mode SQL Tutorial",
                    "tutorial",
                    "https://mode.com/sql-tutorial/"
                ),
                build_resource(
                    "Kaggle Datasets",
                    "dataset library",
                    "https://www.kaggle.com/datasets"
                ),
                build_resource(
                    "YouTube: SQL Portfolio Project for Beginners",
                    "video search",
                    "https://www.youtube.com/results?search_query=sql+portfolio+project+for+beginners"
                ),
                build_resource(
                    "TikTok: SQL Beginner Tips",
                    "short-form video search",
                    "https://www.tiktok.com/search?q=sql%20beginner%20tips"
                )
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
                build_resource(
                    "Pandas Getting Started",
                    "documentation",
                    "https://pandas.pydata.org/docs/getting_started/index.html"
                ),
                build_resource(
                    "Kaggle Python Course",
                    "course",
                    "https://www.kaggle.com/learn/python"
                ),
                build_resource(
                    "Matplotlib Tutorials",
                    "documentation",
                    "https://matplotlib.org/stable/tutorials/index.html"
                ),
                build_resource(
                    "YouTube: Python Data Analysis Project for Beginners",
                    "video search",
                    "https://www.youtube.com/results?search_query=python+data+analysis+project+for+beginners"
                ),
                build_resource(
                    "TikTok: Python Data Analysis Tips",
                    "short-form video search",
                    "https://www.tiktok.com/search?q=python%20data%20analysis%20tips"
                )
            ],
            "difficulty": "Beginner to Intermediate",
            "estimated_time": "1 to 2 weekends"
        })

    # -------------------------
    # AI / Machine Learning Plan
    # -------------------------

    if has_any_skill(missing_skills_lower, [
        "ai",
        "artificial intelligence",
        "machine learning",
        "llm",
        "large language models",
        "generative ai",
        "predictive modeling"
    ]):
        action_plan.append({
            "title": "Build a Small AI or Prediction Project",
            "why_it_matters": (
                "AI and machine learning skills are easier for recruiters to trust when you can point to a small working project instead of only listing the terms."
            ),
            "suggested_project": (
                "Build a beginner AI project such as a resume bullet rewriter, simple classifier, chatbot prototype, or prediction model using a public dataset."
            ),
            "skills_gained": [
                "AI fundamentals",
                "Prompt engineering",
                "Model evaluation",
                "Applied machine learning"
            ],
            "resources": [
                build_resource(
                    "Google Machine Learning Crash Course",
                    "course",
                    "https://developers.google.com/machine-learning/crash-course"
                ),
                build_resource(
                    "Kaggle Intro to Machine Learning",
                    "course",
                    "https://www.kaggle.com/learn/intro-to-machine-learning"
                ),
                build_resource(
                    "OpenAI API Documentation",
                    "documentation",
                    "https://platform.openai.com/docs"
                ),
                build_resource(
                    "YouTube: Beginner AI Project Tutorial",
                    "video search",
                    "https://www.youtube.com/results?search_query=beginner+ai+project+tutorial+python"
                ),
                build_resource(
                    "TikTok: AI Project Ideas for Students",
                    "short-form video search",
                    "https://www.tiktok.com/search?q=ai%20project%20ideas%20for%20students"
                )
            ],
            "difficulty": "Intermediate",
            "estimated_time": "1 to 2 weekends"
        })

    # -------------------------
    # Final Fallback Plan
    # -------------------------

    if len(action_plan) == 0:
        action_plan.append({
            "title": "Polish Resume Impact",
            "why_it_matters": (
                "Your resume already shows some alignment with this role. "
                "The next improvement is making your experience more specific, measurable, and easy to understand."
            ),
            "suggested_project": (
                "Update 3 resume bullets by adding tools used, project context, measurable results, or business impact."
            ),
            "skills_gained": [
                "Resume improvement",
                "Impact writing",
                "Professional positioning"
            ],
            "resources": [
                build_resource(
                    "Harvard Resume and Cover Letter Guide",
                    "guide",
                    "https://careerservices.fas.harvard.edu/resources/create-a-strong-resume/"
                ),
                build_resource(
                    "YouTube: Resume Tips for College Students",
                    "video search",
                    "https://www.youtube.com/results?search_query=resume+tips+for+college+students"
                ),
                build_resource(
                    "TikTok: Resume Tips for College Students",
                    "short-form video search",
                    "https://www.tiktok.com/search?q=resume%20tips%20for%20college%20students"
                )
            ],
            "difficulty": "Beginner",
            "estimated_time": "30 minutes"
        })

    return action_plan