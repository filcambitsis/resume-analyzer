from flask import Flask, render_template, request

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
        text = request.form.get["resume_text"].lower()
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


# run the app
if __name__ == "__main__":
    app.run(debug=True)