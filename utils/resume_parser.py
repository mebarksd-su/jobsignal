import pdfplumber


# =========================
# RESUME PDF PARSER
# Extracts readable text from uploaded resume PDFs.
# Returns a structured result so the app can handle errors cleanly.
# =========================


def extract_resume_text(uploaded_file):

    extracted_text = ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    extracted_text += page_text + "\n"

    except Exception:
        return {
            "success": False,
            "text": "",
            "error": (
                "RoleRadar could not read this PDF. Try uploading a different resume file or use a text-based PDF."
            )
        }

    extracted_text = extracted_text.strip()

    if extracted_text == "":
        return {
            "success": False,
            "text": "",
            "error": (
                "RoleRadar could not find readable text in this PDF. This may happen with scanned or image-based resumes."
            )
        }

    return {
        "success": True,
        "text": extracted_text,
        "error": ""
    }