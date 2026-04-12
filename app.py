from flask import Flask, render_template, request

app = Flask(__name__)

# Skills to check
tech_skills = [
    "python", "java", "sql", "machine learning", "data analysis", "git", "flask", "excel"
]

professional_skills = [
    "teamwork", "communication", "problem solving", "leadership"
]
