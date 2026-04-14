from flask import Flask, render_template, request
import PyPDF2

app = Flask(__name__)

# Skills to check (import from skills.py)
from skills import (
    technical_skills,
    ai_data_skills,
    engineering_skills,
    business_finance_skills,
    marketing_sales_skills,
    product_skills,
    management_skills,
    data_analytics_skills,
    research_skills,
    creative_skills,
    tools_skills,
    professional_skills,
    languages
)

# Group all skills into categories
skills_dict = {
    "Technical Skills": technical_skills,
    "AI & Data": ai_data_skills,
    "Engineering": engineering_skills,
    "Business & Finance": business_finance_skills,
    "Marketing & Sales": marketing_sales_skills,
    "Product": product_skills,
    "Management": management_skills,
    "Data & Analytics": data_analytics_skills,
    "Research": research_skills,
    "Creative": creative_skills,
    "Tools": tools_skills,
    "Languages": languages,
    "Professional Skills": professional_skills
}

# The main page of the website
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        text = ""

        # Get pasted text
        if request.form.get("resume_text"):
            text += request.form.get("resume_text")

        # Get uploaded PDF
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
                "found_skills": {},
                "score": 0,
                "feedback": "Please enter text or upload a PDF",
                "suggestions": []
            }
            return render_template("index.html", result=result)

        # Find skills per category
        found_skills = {}

        for category, skill_list in skills_dict.items():
            found = [skill for skill in skill_list if skill in text]
            found_skills[category] = found

        # Count words
        word_count = len(text.split())

        # Calculate score based on ALL found skills
        total_found = sum(len(skills) for skills in found_skills.values())
        score = min(total_found * 5, 100)

        # Basic feedback based on score
        if score >= 75:
            feedback = "Strong resume"
        elif score >= 55:
            feedback = "Decent resume, but could improve"
        else:
            feedback = "Needs improvement"

        # Generate suggestions based on missing categories
        suggestions = []

        for category, skills in found_skills.items():
            if len(skills) == 0:
                suggestions.append(f"Consider adding {category.lower()}")

        # Final result sent to HTML
        result = {
            "word_count": word_count,
            "found_skills": found_skills,
            "score": score,
            "feedback": feedback,
            "suggestions": suggestions
        }

    return render_template("index.html", result=result)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)