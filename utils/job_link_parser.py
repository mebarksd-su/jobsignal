from urllib.parse import urlparse, unquote
import re


def clean_url_words(text):

    words = re.findall(r"[a-zA-Z]+", text.lower())

    ignored_words = {
        "job",
        "jobs",
        "careers",
        "career",
        "apply",
        "application",
        "posting",
        "details",
        "view",
        "req",
        "requisition",
        "opportunity",
        "opportunities",
        "search",
        "description",
        "external",
        "en",
        "us",
        "usa",
        "remote",
        "hybrid",
        "onsite",
        "on",
        "site",
        "student",
        "students",
        "fulltime",
        "full",
        "time"
    }

    return [
        word for word in words
        if word not in ignored_words and len(word) > 2
    ]


def format_guess(text):

    return (
        text.replace("-", " ")
        .replace("_", " ")
        .strip()
        .title()
    )


def infer_application_details_from_link(job_link):

    parsed = urlparse(job_link)

    domain = parsed.netloc.lower().replace("www.", "")
    path = unquote(parsed.path.lower())
    query = unquote(parsed.query.lower())

    company_guess = ""
    role_guess = ""

    notes = []

    domain_parts = [
        part for part in domain.split(".")
        if part
    ]

    path_parts = [
        part for part in path.split("/")
        if part
    ]

    # =========================
    # GREENHOUSE
    # =========================

    if "greenhouse" in domain:

        if len(path_parts) > 0:
            company_guess = format_guess(path_parts[0])

        notes.append("Detected Greenhouse job link.")

    # =========================
    # LEVER
    # =========================

    elif "lever.co" in domain:

        if len(path_parts) > 0:
            company_guess = format_guess(path_parts[0])

        notes.append("Detected Lever job link.")

    # =========================
    # WORKDAY
    # =========================

    elif "workdayjobs" in domain or "myworkdayjobs" in domain:

        if len(domain_parts) > 0:
            company_guess = format_guess(domain_parts[0])

        notes.append("Detected Workday job link.")

    # =========================
    # LINKEDIN
    # =========================

    elif "linkedin" in domain:

        notes.append(
            "Detected LinkedIn job link. Company auto-fill may be limited from the URL alone."
        )

    # =========================
    # HANDSHAKE
    # =========================

    elif "handshake" in domain:

        notes.append(
            "Detected Handshake job link. Job details may need to be entered manually."
        )

    # =========================
    # INDEED
    # =========================

    elif "indeed" in domain:

        notes.append(
            "Detected Indeed job link. Job details may need to be entered manually."
        )

    # =========================
    # GENERIC CAREERS SITES
    # =========================

    else:

        platform_words = {
            "jobs",
            "careers",
            "boards",
            "apply",
            "recruiting",
            "talent"
        }

        if len(domain_parts) > 0:

            first_domain_part = domain_parts[0]

            if (
                first_domain_part in ["careers", "jobs"]
                and len(domain_parts) > 1
            ):
                company_guess = format_guess(domain_parts[1])

            elif first_domain_part not in platform_words:
                company_guess = format_guess(first_domain_part)

    # =========================
    # ROLE GUESSING
    # =========================

    combined_text = f"{path} {query}"

    role_words = clean_url_words(combined_text)

    if company_guess:

        company_words = company_guess.lower().split()

        role_words = [
            word for word in role_words
            if word not in company_words
        ]

    if len(role_words) >= 2:
        role_guess = " ".join(role_words[-7:]).title()

    return {
        "company": company_guess,
        "role": role_guess,
        "notes": notes
    }