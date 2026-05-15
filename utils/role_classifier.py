def classify_role_type(job_description):

    job_description = job_description.lower()

    role_scores = {
        "Data Analyst": 0,
        "Business Intelligence": 0,
        "AI / Machine Learning": 0,
        "Cloud / Data Engineering": 0,
        "GIS / Spatial Analytics": 0
    }

    role_keywords = {
        "Data Analyst": [
            "data analyst",
            "data analysis",
            "excel",
            "sql",
            "reporting"
        ],
        "Business Intelligence": [
            "business intelligence",
            "power bi",
            "tableau",
            "dashboard",
            "dashboards",
            "kpi"
        ],
        "AI / Machine Learning": [
            "machine learning",
            "ai",
            "artificial intelligence",
            "nlp",
            "llm",
            "predictive modeling"
        ],
        "Cloud / Data Engineering": [
            "aws",
            "azure",
            "gcp",
            "etl",
            "data pipeline",
            "data pipelines",
            "cloud"
        ],
        "GIS / Spatial Analytics": [
            "gis",
            "arcgis",
            "qgis",
            "spatial",
            "geospatial",
            "mapping"
        ]
    }

    for role_type, keywords in role_keywords.items():
        for keyword in keywords:
            if keyword in job_description:
                role_scores[role_type] += 1

    best_role = max(role_scores, key=role_scores.get)

    if role_scores[best_role] == 0:
        return "General Analytics"

    return best_role