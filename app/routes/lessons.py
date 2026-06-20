from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.routes import main
from app.models import Course, Lesson
from app.forms import LessonForm



@main.route("/courses/<int:course_id>/lessons/create", methods=["GET", "POST"])
@login_required
def create_lesson(course_id):
    course = Course.query.get_or_404(course_id)
    if not current_user.is_teacher_of(course):
        abort(403)

    form = LessonForm()
    if form.validate_on_submit():
        lesson = Lesson(
            title=form.title.data,
            video_url=form.video_url.data,
            content=form.content.data,
            course_id=course.id
        )
        db.session.add(lesson)
        db.session.commit()
        flash("Lesson added successfully!", "success")
        return redirect(url_for("main.course_lessons", course_id=course.id))

    return render_template("create_lesson.html", form=form, course=course)


@main.route("/courses/<int:course_id>/lessons")
@login_required
def course_lessons(course_id):
    course = Course.query.get_or_404(course_id)
    is_owner = current_user.is_teacher_of(course)
    is_enrolled = current_user.is_enrolled_in(course)

    if not (is_owner or is_enrolled):
        flash("You must enroll in this course to view its lessons.", "danger")
        return redirect(url_for("main.course_detail", course_id=course.id))

    lessons = Lesson.query.filter_by(course_id=course.id).order_by(Lesson.order).all()
    return render_template("course_lessons.html", course=course, lessons=lessons, is_owner=is_owner)


@main.route("/lessons/<int:lesson_id>")
@login_required
def view_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.course

    if not (current_user.is_teacher_of(course) or current_user.is_enrolled_in(course)):
        flash("You must enroll in this course to view this lesson.", "danger")
        return redirect(url_for("main.course_detail", course_id=course.id))

    return render_template("view_lesson.html", lesson=lesson, course=course)