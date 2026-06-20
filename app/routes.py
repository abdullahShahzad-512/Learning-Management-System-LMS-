from flask import Blueprint, render_template, redirect, url_for,flash
from app import db
from app.models import User, Course, Enrollment , Lesson
from app.forms import RegisterForm, LoginForm, CourseForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from flask import abort

main = Blueprint("main", __name__)

def teacher_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.role != "teacher":
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@main.route("/")
def home():
    return render_template("home.html")

# REGISTER
@main.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already exists!", "danger")
            return redirect(url_for("main.register"))

        hashed_password = generate_password_hash(form.password.data)

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )

        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for("main.login"))

    return render_template("register.html", form=form)

# LOGIN
@main.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("main.dashboard"))

        flash("Invalid email or password", "danger")

    return render_template("login.html", form=form)

# DASHBOARD
@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# LOGOUT
@main.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out", "info")
    return redirect(url_for("main.login"))


@main.route("/courses")
def courses():
    all_courses = Course.query.all()
    return render_template("courses.html", courses=all_courses)


@main.route("/courses/create", methods=["GET", "POST"])
@login_required
@teacher_required
def create_course():
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            title=form.title.data,
            description=form.description.data,
            teacher_id=current_user.id
        )
        db.session.add(course)
        db.session.commit()
        flash("Course created successfully!", "success")
        return redirect(url_for("main.courses"))

    return render_template("create_course.html", form=form)


@main.route("/courses/<int:course_id>")
def course_detail(course_id):
    course = Course.query.get_or_404(course_id)

    is_enrolled = False
    if current_user.is_authenticated and current_user.role == "student":
        is_enrolled = Enrollment.query.filter_by(
            student_id=current_user.id, course_id=course.id
        ).first() is not None

    return render_template("course_detail.html", course=course, is_enrolled=is_enrolled)


@main.route("/courses/<int:course_id>/enroll", methods=["POST"])
@login_required
def enroll(course_id):
    if current_user.role != "student":
        flash("Only students can enroll in courses.", "danger")
        return redirect(url_for("main.course_detail", course_id=course_id))

    course = Course.query.get_or_404(course_id)
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


@main.route("/courses/<int:course_id>/lessons/create", methods=["GET", "POST"])
@login_required
@teacher_required
def create_lesson(course_id):
    course = Course.query.get_or_404(course_id)

    if course.teacher_id != current_user.id:
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

    is_owner = current_user.role == "teacher" and course.teacher_id == current_user.id
    is_enrolled = Enrollment.query.filter_by(
        student_id=current_user.id, course_id=course.id
    ).first() is not None

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

    is_owner = current_user.role == "teacher" and course.teacher_id == current_user.id
    is_enrolled = Enrollment.query.filter_by(
        student_id=current_user.id, course_id=course.id
    ).first() is not None

    if not (is_owner or is_enrolled):
        flash("You must enroll in this course to view this lesson.", "danger")
        return redirect(url_for("main.course_detail", course_id=course.id))

    return render_template("view_lesson.html", lesson=lesson, course=course)