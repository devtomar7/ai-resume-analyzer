from PyPDF2 import PdfReader

skills_db = {
    "Data Scientist": ["python", "machine learning", "pandas", "numpy", "tensorflow"],
    "Web Developer": ["html", "css", "javascript", "react", "node", "mongodb"],
    "Backend Developer": ["python", "java", "sql", "mongodb", "node"],
    "AI Engineer": ["python", "machine learning", "deep learning", "tensorflow", "pytorch"]
}


def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    return text.lower()


def analyze_resume(pdf_path, job_desc=""):

    text = extract_text_from_pdf(pdf_path)

    detected_skills = []
    all_skills = set()

    for role in skills_db:
        all_skills.update(skills_db[role])

    for skill in all_skills:
        if skill in text:
            detected_skills.append(skill)

    score = min(len(detected_skills) * 10, 100)

    best_role = None
    max_match = 0
    missing_skills = []

    for role, skills in skills_db.items():

        match = len(set(detected_skills) & set(skills))

        if match > max_match:
            max_match = match
            best_role = role
            missing_skills = list(set(skills) - set(detected_skills))

    match_percent = 0

    if job_desc:
        job_desc = job_desc.lower()
        match_count = 0

        for skill in detected_skills:
            if skill in job_desc:
                match_count += 1

        if detected_skills:
            match_percent = int((match_count / len(detected_skills)) * 100)

    # AI feedback
    feedback = []

    if score < 50:
        feedback.append("Your resume needs more technical skills.")

    if missing_skills:
        feedback.append("Consider learning: " + ", ".join(missing_skills))

    if "project" not in text:
        feedback.append("Add project experience to improve your resume.")

    return score, detected_skills, best_role, missing_skills, match_percent, feedback