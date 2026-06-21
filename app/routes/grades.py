from flask import render_template, abort
from flask_login import login_required, current_user
from app.routes import main
from app.models import Course, Submission, Assignment, Quiz, QuizResult


@main.route("/my-grades")
@login_required
def my_grades():
    submissions = (
        Submission.query
        .filter_by(student_id=current_user.id)
        .order_by(Submission.submitted_at.desc())
        .all()
    )
    quiz_results = (
        QuizResult.query
        .filter_by(student_id=current_user.id)
        .order_by(QuizResult.taken_at.desc())
        .all()
    )
    return render_template("my_grades.html", submissions=submissions, quiz_results=quiz_results)


@main.route("/courses/<int:course_id>/gradebook")
@login_required
def course_gradebook(course_id):
    course = Course.query.get_or_404(course_id)
    if not current_user.is_teacher_of(course):
        abort(403)

    submissions = (
        Submission.query
        .join(Assignment)
        .filter(Assignment.course_id == course.id)
        .order_by(Submission.submitted_at.desc())
        .all()
    )
    quiz_results = (
        QuizResult.query
        .join(Quiz)
        .filter(Quiz.course_id == course.id)
        .order_by(QuizResult.taken_at.desc())
        .all()
    )
    return render_template("course_gradebook.html", course=course, submissions=submissions, quiz_results=quiz_results)