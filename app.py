from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

# Skills to check
tech_skills = [
    "python", "java", "sql", "machine learning", "data analysis", "git", "flask", "excel"
]

professional_skills = [
    "teamwork", "communication", "problem solving", "leadership"
]

# The main page of the website
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        text = ""
        if request.form.get("resume_text"):
            text += request.form.get("resume_text")
        file = request.files.get("resume_file")
        if file and file.filename.endswith(".pdf"):
            try:
                reader = PyPDF2.PdfReader(file)
                for page in reader.pages:
                    text += page.extract_text() or ""
            except:
                pass  # Prevents crash if PDF is problematic

        text = text.lower()

        # Handle empty input
        if not text.strip():
            result = {
                "word_count": 0,
                "tech_skills": [],
                "professional_skills": [],
                "score": 0,
                "feedback": "Please enter text or upload a PDF"
            }
            return render_template("index.html", result=result)

        tech_found = [skill for skill in tech_skills if skill in text]
        prof_found = [skill for skill in professional_skills if skill in text]

        word_count = len(text.split())
        score = min((len(tech_found) + len(prof_found)) * 10, 100)

        if score >= 75:
            feedback = "Strong resume"
        elif score >= 55:
            feedback = "Decent resume, but could improve"
        else:
            feedback = "Needs improvement"

        result = {
            "word_count": word_count,
            "tech_skills": tech_found,
            "professional_skills": prof_found,
            "score": score,
            "feedback": feedback
        }

    return render_template("index.html", result=result)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)