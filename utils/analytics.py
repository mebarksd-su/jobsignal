import pandas as pd


def add_analytics_columns(df):

    if len(df) > 0:
        df["Days Since Applied"] = (
            pd.Timestamp.today() - pd.to_datetime(df["Date Added"])
        ).dt.days
    else:
        df["Days Since Applied"] = []

    df["Application Health"] = df["Days Since Applied"].apply(application_health)
    df["Recommendation"] = df.apply(follow_up_recommendation, axis=1)
    df["Priority"] = df.apply(application_priority, axis=1)

    return df


def application_health(days):

    if days < 7:
        return "Fresh"

    elif days < 14:
        return "Follow Up Soon"

    else:
        return "Stale"


def follow_up_recommendation(row):

    if row["Status"] in ["Offer", "Rejected"]:
        return "No action needed"

    if row["Application Health"] == "Fresh":
        return "Wait for response"

    elif row["Application Health"] == "Follow Up Soon":
        return "Consider following up"

    else:
        return "Follow up immediately"


def application_priority(row):

    if row["Status"] == "Offer":
        return "High Priority"

    elif row["Status"] == "Interviewing":
        return "High Priority"

    elif row["Status"] == "Applied" and row["Days Since Applied"] <= 14:
        return "Medium Priority"

    else:
        return "Low Priority"