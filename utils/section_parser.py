import re


SECTION_HEADERS = [
    "skills",
    "technical skills",
    "tools",
    "technologies",
    "core competencies",
    "tech stack"
]


def extract_skills_section(resume_text):

    lines = resume_text.split("\n")

    capture = False

    extracted_lines = []

    for line in lines:

        clean_line = line.strip().lower()

        if clean_line in SECTION_HEADERS:
            capture = True
            continue

        if capture:

            if clean_line == "":
                break

            extracted_lines.append(line)

    return "\n".join(extracted_lines)