from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.routes import main
from app.models import Course, Enrollment
from app.forms import CourseForm


@main.route("/courses")
def courses():
    all_courses = Course.query.all()
    return render_template("courses.html", courses=all_courses)


@main.route("/courses/create", methods=["GET", "POST"])
@login_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(title=form.title.data, description=form.description.data, teacher_id=current_user.id)
        db.session.add(course)
        db.session.commit()
        flash("Course created! You're now the teacher of this course.", "success")
        return redirect(url_for("main.courses"))
    return render_template("create_course.html", form=form)


@main.route("/courses/<int:course_id>")
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)
    is_owner = current_user.is_authenticated and current_user.is_teacher_of(course)
    is_enrolled = current_user.is_authenticated and current_user.is_enrolled_in(course)
    return render_template("course_detail.html", course=course, is_owner=is_owner, is_enrolled=is_enrolled)

@main.route("/courses/<int:course_id>/enroll", methods=["POST"])
@login_required
def enroll(course_id):
    course = Course.query.get_or_404(course_id)

    if current_user.is_teacher_of(course):
        flash("You're the teacher of this course — you already have full access.", "info")
        return redirect(url_for("main.course_detail", course_id=course_id))

    existing = Enrollment.query.filter_by(student_id=current_user.id, course_id=course.id).first()
    if existing:
        flash("You are already enrolled in this course.", "info")
    else:
        db.session.add(Enrollment(student_id=current_user.id, course_id=course.id))
        db.session.commit()
        flash(f"Enrolled in {course.title}!", "success")

    return redirect(url_for("main.course_detail", course_id=course_id))


@main.route("/my-courses")
@login_required
def my_courses():
    if current_user.role == "teacher":
        course_list = Course.query.filter_by(teacher_id=current_user.id).all()
    else:
        course_list = [e.course for e in current_user.enrollments]

    return render_template("my_courses.html", courses=course_list)