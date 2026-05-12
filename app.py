import streamlit as st
import pandas as pd
from datetime import date
import os
import matplotlib.pyplot as plt


st.set_page_config(page_title="JobSignal", layout="wide")
page = st.sidebar.radio(
    "Navigation",
    [
        "Application Tracker",
        "AI Analyzer"
    ]
)

DATA_FILE = "data/applications.csv"

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    if "Work Arrangement" not in df.columns:
        df["Work Arrangement"] = "Not Specified"

    df["Work Arrangement"] = df["Work Arrangement"].fillna("Not Specified")

else:
    df = pd.DataFrame(columns=[
        "Date Added", "Company", "Role", "Location", "Work Arrangement", "Status", "Job Link", "Notes"
    ])

st.title("JobSignal")
if page == "Application Tracker":
 st.write("AI-powered internship and job application tracker.")

 st.header("Add New Application")

 if "company" not in st.session_state:
    st.session_state.company = ""

 if "role" not in st.session_state:
    st.session_state.role = ""

 if "location" not in st.session_state:
    st.session_state.location = ""

 if "job_link" not in st.session_state:
    st.session_state.job_link = ""

 if "notes" not in st.session_state:
    st.session_state.notes = ""

 company = st.text_input(
    "Company Name",
    key="company"
 )

 role = st.text_input(
    "Job Title",
    key="role"
 )

 location = st.text_input(
    "Location",
    key="location"
 )

 work_arrangement = st.selectbox(
    "Work Arrangement",
    ["Not Specified", "Remote", "Hybrid", "On-site"]
 )

 status = st.selectbox(
    "Application Status",
    ["Interested", "Applied", "Interview", "Rejected", "Offer"]
 )

 job_link = st.text_input(
    "Job Link",
    key="job_link"
 )

 notes = st.text_area(
    "Notes",
    key="notes"
 )

 submit_button = st.button("Add Application")

 if submit_button:

    if company.strip() == "" or role.strip() == "":
        st.error("Company name and job title are required.")

    else:
        new_application = {
           "Date Added": date.today(),
           "Company": company.strip(),
           "Role": role.strip(),
           "Location": location.strip(),
           "Work Arrangement": work_arrangement,
           "Status": status,
           "Job Link": job_link.strip(),
           "Notes": notes.strip()
        }

        df = pd.concat([df, pd.DataFrame([new_application])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)

        st.success("Application saved successfully.")
        

 st.header("Dashboard")

 total_applications = len(df)
 applied_count = len(df[df["Status"] == "Applied"])
 interview_count = len(df[df["Status"] == "Interview"])
 offer_count = len(df[df["Status"] == "Offer"])

 conversion_rate = 0
 if total_applications > 0:
    conversion_rate = round((interview_count / total_applications) * 100, 1)

 col1, col2, col3, col4, col5 = st.columns(5)
 col1.metric("Total Applications", total_applications)
 col2.metric("Applied", applied_count)
 col3.metric("Interviews", interview_count)
 col4.metric("Offers", offer_count)
 col5.metric("Interview Rate", f"{conversion_rate}%")

 st.write(
    f"You have {total_applications} total applications, "
    f"{interview_count} interviews, and {offer_count} offers tracked."
 )

 st.header("Filters")

 search_term = st.text_input("Search Company or Job Title")

 status_filter = st.selectbox(
    "Filter by Status",
    ["All", "Interested", "Applied", "Interview", "Rejected", "Offer"]
 )

 filtered_df = df.copy()

 if search_term:
    filtered_df = filtered_df[
        filtered_df["Company"].str.contains(search_term, case=False, na=False) |
        filtered_df["Role"].str.contains(search_term, case=False, na=False)
    ]

 if status_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Status"] == status_filter
    ]
 st.subheader("Applications by Status")
 status_counts = df["Status"].value_counts()
 st.bar_chart(status_counts)

 st.subheader("Application Distribution")
 fig, ax = plt.subplots(figsize=(5, 5))
 ax.pie(
    status_counts,
    labels=status_counts.index,
    autopct="%1.1f%%",
    startangle=90
 )
 ax.axis("equal")
 st.pyplot(fig)

 st.subheader("Top Companies Applied To")
 company_counts = df["Company"].value_counts().head(5)
 st.bar_chart(company_counts)

 st.subheader("Applications by Location")
 location_counts = df["Location"].replace("", "Unknown").value_counts()
 st.bar_chart(location_counts)

 st.subheader("Applications by Work Arrangement")
 work_arrangement_counts = df["Work Arrangement"].fillna("Not Specified").value_counts()
 st.bar_chart(work_arrangement_counts)
 


if page == "AI Analyzer":
 st.header("AI Job Description Analyzer")

 job_description = st.text_area(
    "Paste Job Description",
    height=250
 )

 analyze_button = st.button("Analyze Job Description")

 if analyze_button:

    detected_skills = []

    skill_keywords = [
        "Python",
        "SQL",
        "Excel",
        "Machine Learning",
        "AI",
        "Data Visualization",
        "Tableau",
        "Communication",
        "Leadership",
        "Cloud",
        "AWS",
        "Power BI"
    ]

    for skill in skill_keywords:
        if skill.lower() in job_description.lower():
           detected_skills.append(skill)

    st.subheader("Detected Skills")

    if detected_skills:
        for skill in detected_skills:
           st.write(f"• {skill}")
    else:
        st.write("No matching skills detected.")

    st.subheader("AI Summary")

    st.write(
        "This role appears focused on analytical, technical, and communication skills. "
        "Candidates should emphasize relevant technical projects, problem-solving ability, "
        "and real-world experience."
    )
    st.subheader("Recommended Resume Focus")

    resume_recommendations = []

    if "Python" in detected_skills:
        resume_recommendations.append(
        "Highlight Python projects involving automation, analytics, or AI workflows."
        )

    if "SQL" in detected_skills:
        resume_recommendations.append(
        "Emphasize experience working with databases, queries, and structured datasets."
        )

    if "Machine Learning" in detected_skills or "AI" in detected_skills:
        resume_recommendations.append(
        "Showcase AI-related projects, model experimentation, or data-driven research."
        )

    if "Tableau" in detected_skills or "Power BI" in detected_skills:
        resume_recommendations.append(
        "Include dashboard or visualization projects demonstrating business insights."
        )

    if len(resume_recommendations) == 0:
        resume_recommendations.append(
        "Focus on transferable technical and communication skills."
        )

    for recommendation in resume_recommendations:
        st.write(f"• {recommendation}")

 st.header("Delete Application")
 if len(df) > 0:
    delete_index = st.selectbox(
        "Select Application to Delete",
        df.index,
        format_func=lambda x: f"{df.loc[x, 'Company']} - {df.loc[x, 'Role']}"
    )
    delete_button = st.button("Delete Selected Application")

    if delete_button:
        df = df.drop(delete_index)
        df = df.reset_index(drop=True)
        df.to_csv(DATA_FILE, index=False)
        st.success("Application deleted successfully.")
        st.rerun()

 st.header("Export Data")
 csv_data = df.to_csv(index=False).encode("utf-8")
 st.download_button(
    label="Download Applications CSV",
    data=csv_data,
    file_name="jobsignal_applications.csv",
    mime="text/csv"
 )

 st.subheader("Recent Applications")
 recent_df = df.tail(5)

 st.dataframe(
     recent_df,
     width="stretch"
 )

 st.header("Saved Applications")

 st.write(f"Showing {len(df)} applications.")
 from datetime import datetime

 df["Days Since Applied"] = (
    datetime.today() - pd.to_datetime(df["Date Added"])
 ).dt.days

 st.subheader("Key Insights")
 most_common_status = df["Status"].mode()[0]
 top_company = df["Company"].mode()[0]

 st.info(
    f"""
    • Most common application status: {most_common_status}

    • Company applied to most often: {top_company}

    • Total tracked applications: {len(df)}

    • Average days since applying: {round(df['Days Since Applied'].mean(), 1)}
    """
 )

 def application_health(days):
    if days < 7:
        return "Fresh"
    elif days < 14:
        return "Follow Up Soon"
    else:
        return "Stale"
 df["Application Health"] = df["Days Since Applied"].apply(application_health)

 def follow_up_recommendation(row):
    if row["Status"] in ["Offer", "Rejected"]:
        return "No action needed"
    if row["Application Health"] == "Fresh":
        return "Wait for response"
    elif row["Application Health"] == "Follow Up Soon":
        return "Consider following up"
    else:
        return "Follow up immediately"
 df["Recommendation"] = df.apply(follow_up_recommendation, axis=1)

 display_columns = [
    "Date Added",
    "Days Since Applied",
    "Application Health",
    "Recommendation",
    "Company",
    "Role",
    "Location",
    "Work Arrangement",
    "Status",
    "Job Link",
    "Notes"
 ]
 st.subheader("Manage Applications")

 header1, header2, header3, header4, header5 = st.columns([2, 2, 2, 2, 1])

 header1.write("**Company**")
 header2.write("**Role**")
 header3.write("**Status**")
 header4.write("**Location**")
 header5.write("**Action**")
 for index, row in df.iterrows():
    col1, col2, col3, col4, col5 = st.columns([2,2,2,2,1])

    col1.write(row["Company"])
    col2.write(row["Role"])
    col3.write(row["Status"])
    col4.write(
    row["Location"] if pd.notna(row["Location"]) else "Not Specified"
 )

    if col5.button("Delete", key=f"delete_{index}"):

        df = df.drop(index=index)
        df = df.reset_index(drop=True)

        df.to_csv(DATA_FILE, index=False)

        st.success("Application deleted successfully.")

        st.rerun()

# st.dataframe(df[display_columns], width="stretch")