from flask import Flask, render_template, request, send_file
from analyzer import analyze_resume
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        file = request.files["resume"]
        job_desc = request.form.get("jobdesc")

        if file:

            path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(path)

            score, skills, role, missing, match, feedback = analyze_resume(path, job_desc)

            return render_template(
                "index.html",
                score=score,
                skills=skills,
                role=role,
                missing=missing,
                match=match,
                feedback=feedback
            )

    return render_template("index.html")


@app.route("/download")
def download():

    score = request.args.get("score")
    role = request.args.get("role")
    skills = request.args.get("skills")
    missing = request.args.get("missing")

    file_path = "resume_report.pdf"

    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("AI Resume Analyzer Report", styles['Title']))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph(f"Resume Score: {score}", styles['Normal']))
    elements.append(Paragraph(f"Recommended Role: {role}", styles['Normal']))
    elements.append(Paragraph(f"Detected Skills: {skills}", styles['Normal']))
    elements.append(Paragraph(f"Missing Skills: {missing}", styles['Normal']))

    pdf = SimpleDocTemplate(file_path)
    pdf.build(elements)

    return send_file(file_path, as_attachment=True)

    if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
