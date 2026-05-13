import pandas as pd


def generate_recommendations(df):

    recommendations = []

    if len(df) == 0:
        return ["No application data available yet."]

    # -----------------------------
    # Interview Rate
    # -----------------------------

    interview_count = len(
        df[df["Status"] == "Interviewing"]
    )

    application_count = len(
        df[df["Status"] == "Applied"]
    )

    if application_count > 0:

        interview_rate = (
            interview_count / len(df)
        ) * 100

        if interview_rate < 10:
            recommendations.append(
                "Interview rate is low. Consider improving resume targeting and keyword optimization."
            )

        elif interview_rate >= 25:
            recommendations.append(
                "Interview rate is strong. Your application strategy appears effective."
            )

    # -----------------------------
    # Rejection Analysis
    # -----------------------------

    rejection_count = len(
        df[df["Status"] == "Rejected"]
    )

    if rejection_count >= 5:
        recommendations.append(
            "High rejection volume detected. Consider tailoring applications more specifically to each role."
        )

    # -----------------------------
    # Work Arrangement Trends
    # -----------------------------

    remote_count = len(
        df[df["Work Arrangement"] == "Remote"]
    )

    hybrid_count = len(
        df[df["Work Arrangement"] == "Hybrid"]
    )

    onsite_count = len(
        df[df["Work Arrangement"] == "On-site"]
    )

    if remote_count > hybrid_count and remote_count > onsite_count:
        recommendations.append(
            "Most applications are remote-focused. Expanding into hybrid opportunities may increase response rates."
        )

    # -----------------------------
    # Location Intelligence
    # -----------------------------

    top_locations = (
        df["Location"]
        .value_counts()
        .head(1)
    )

    if len(top_locations) > 0:

        top_location = top_locations.index[0]

        recommendations.append(
            f"Most application activity is concentrated in {top_location}."
        )

    # -----------------------------
    # Application Velocity
    # -----------------------------

    if "Date Added" in df.columns:

        recent_apps = len(
            df[df["Days Since Applied"] <= 7]
        )

        if recent_apps >= 15:
            recommendations.append(
                "High recent application volume detected. Ensure quality is not being sacrificed for quantity."
            )

    # -----------------------------
    # Offer Performance
    # -----------------------------

    offer_count = len(
        df[df["Status"] == "Offer"]
    )

    if offer_count >= 3:
        recommendations.append(
            "Strong offer conversion detected. Your resume and interview process appear highly effective."
        )

    return recommendations