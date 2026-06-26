from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.routes import main
from app.models import Course, Lesson
from app.forms import LessonForm
from werkzeug.utils import secure_filename
import os, uuid



@main.route("/courses/<int:course_id>/lessons/create", methods=["GET", "POST"])
@login_required
def create_lesson(course_id):
    form = LessonForm()

    if form.validate_on_submit():
        video_path = None

        # CHECK IF FILE EXISTS
        if form.video.data:
            file = form.video.data

            # 🔥 Avoid filename conflicts
            filename = str(uuid.uuid4()) + "_" + secure_filename(file.filename)

            # ✅ Proper cross-platform folder path
            upload_folder = os.path.join(
                "app", "static", "uploads", "videos", str(course_id)
            )

            # ✅ Create folder if not exists
            os.makedirs(upload_folder, exist_ok=True)

            # ✅ Full path for saving file
            upload_path = os.path.join(upload_folder, filename)
            file.save(upload_path)

            # 🔥 IMPORTANT: store RELATIVE path (not full path)
            video_path = f"uploads/videos/{course_id}/{filename}"

        lesson = Lesson(
            title=form.title.data,
            video_url=video_path,   # ✅ now correct
            content=form.content.data,
            course_id=course_id
        )

        db.session.add(lesson)
        db.session.commit()

        return redirect(url_for("main.course_detail", course_id=course_id))

    return render_template("create_lesson.html", form=form)


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

    # Access control
    if not (current_user.is_teacher_of(course) or current_user.is_enrolled_in(course)):
        flash("You must enroll in this course to view this lesson.", "danger")
        return redirect(url_for("main.course_detail", course_id=course.id))

    # 🔥 FIX: Ensure correct video URL for template
    video_url = None
    if lesson.video_url:
        video_url = url_for('static', filename=lesson.video_url)

    return render_template(
        "view_lesson.html",
        lesson=lesson,
        course=course,
        video_url=video_url
    )
@main.route("/lessons/<int:lesson_id>/delete", methods=["POST"])
@login_required
def delete_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    course = lesson.course

    #  Only teacher can delete
    if not current_user.is_teacher_of(course):
        flash("You are not authorized to delete this lesson.", "danger")
        return redirect(url_for("main.course_detail", course_id=course.id))

    #  Delete video file from server
    if lesson.video_url:
        file_path = os.path.join("app", "static", lesson.video_url)

        if os.path.exists(file_path):
            os.remove(file_path)

    #  Delete lesson from DB
    db.session.delete(lesson)
    db.session.commit()

    flash("Lesson deleted successfully.", "success")
    return redirect(url_for("main.course_detail", course_id=course.id))