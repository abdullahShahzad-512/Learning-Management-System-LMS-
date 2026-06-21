from flask import render_template
from flask_login import login_required, current_user
from app.routes import main
from app.models import Course

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/dashboard")
@login_required
def dashboard():
    teaching_count = Course.query.filter_by(teacher_id=current_user.id).count()
    enrolled_count = len(current_user.enrollments)
    return render_template("dashboard.html", teaching_count=teaching_count, enrolled_count=enrolled_count)