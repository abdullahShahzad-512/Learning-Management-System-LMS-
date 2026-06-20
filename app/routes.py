from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User, Course, Enrollment , Lesson, Assignment, Submission, Quiz, Question, Choice, QuizResult
from app.forms import RegisterForm, LoginForm, CourseForm, LessonForm, AssignmentForm, SubmissionForm, GradeForm, QuizForm, QuestionForm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from functools import wraps
from flask import abort

main = Blueprint("main", __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
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

@main.route("/courses/<int:course_id>/assignments/create", methods=["GET", "POST"])
@login_required
def create_assignment(course_id):
    course = Course.query.get_or_404(course_id)
    if not current_user.is_teacher_of(course):
        abort(403)

    form = AssignmentForm()
    if form.validate_on_submit():
        assignment = Assignment(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            course_id=course.id
        )
        db.session.add(assignment)
        db.session.commit()
        flash("Assignment created!", "success")
        return redirect(url_for("main.course_detail", course_id=course.id))

    return render_template("create_assignment.html", form=form, course=course)


@main.route("/assignments/<int:assignment_id>", methods=["GET", "POST"])
@login_required
def assignment_detail(assignment_id):
    assignment = Assignment.query.get_or_404(assignment_id)
    course = assignment.course

    is_owner = current_user.is_teacher_of(course)
    is_enrolled = current_user.is_enrolled_in(course)

    if not (is_owner or is_enrolled):
        flash("You must be enrolled to view this assignment.", "danger")
        return redirect(url_for("main.course_detail", course_id=course.id))

    if is_owner:
        submissions = Submission.query.filter_by(assignment_id=assignment.id).all()
        return render_template("assignment_detail_teacher.html", assignment=assignment, submissions=submissions)

    form = SubmissionForm()
    existing = Submission.query.filter_by(student_id=current_user.id, assignment_id=assignment.id).first()

    if form.validate_on_submit() and not existing:
        db.session.add(Submission(content=form.content.data, student_id=current_user.id, assignment_id=assignment.id))
        db.session.commit()
        flash("Assignment submitted!", "success")
        return redirect(url_for("main.assignment_detail", assignment_id=assignment.id))

    return render_template("assignment_detail_student.html", assignment=assignment, form=form, existing=existing)


@main.route("/submissions/<int:submission_id>/grade", methods=["GET", "POST"])
@login_required
def grade_submission(submission_id):
    submission = Submission.query.get_or_404(submission_id)
    if not current_user.is_teacher_of(submission.assignment.course):
        abort(403)

    form = GradeForm(obj=submission)
    if form.validate_on_submit():
        submission.grade = form.grade.data
        submission.feedback = form.feedback.data
        db.session.commit()
        flash("Grade saved!", "success")
        return redirect(url_for("main.assignment_detail", assignment_id=submission.assignment_id))

    return render_template("grade_submission.html", form=form, submission=submission)

@main.route("/courses/<int:course_id>/quizzes/create", methods=["GET", "POST"])
@login_required
def create_quiz(course_id):
    course = Course.query.get_or_404(course_id)
    if not current_user.is_teacher_of(course):
        abort(403)

    form = QuizForm()
    if form.validate_on_submit():
        quiz = Quiz(title=form.title.data, course_id=course.id)
        db.session.add(quiz)
        db.session.commit()
        flash("Quiz created — now add questions!", "success")
        return redirect(url_for("main.add_question", quiz_id=quiz.id))

    return render_template("create_quiz.html", form=form, course=course)


@main.route("/quizzes/<int:quiz_id>/questions/add", methods=["GET", "POST"])
@login_required
def add_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    if not current_user.is_teacher_of(quiz.course):
        abort(403)

    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(text=form.text.data, quiz_id=quiz.id)
        db.session.add(question)
        db.session.flush()

        for i, text in enumerate([form.choice1.data, form.choice2.data, form.choice3.data, form.choice4.data], start=1):
            if text:
                db.session.add(Choice(text=text, is_correct=(str(i) == form.correct_choice.data), question_id=question.id))

        db.session.commit()
        flash("Question added! Add another or move on.", "success")
        return redirect(url_for("main.add_question", quiz_id=quiz.id))

    return render_template("add_question.html", form=form, quiz=quiz)


@main.route("/quizzes/<int:quiz_id>", methods=["GET", "POST"])
@login_required
def take_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    course = quiz.course

    if not current_user.is_enrolled_in(course):
        flash("You must be an enrolled student to take this quiz.", "danger")
        return redirect(url_for("main.course_detail", course_id=course.id))

    if request.method == "POST":
        score = 0
        for question in quiz.questions:
            selected = request.form.get(f"question_{question.id}")
            correct = next((c for c in question.choices if c.is_correct), None)
            if selected and correct and int(selected) == correct.id:
                score += 1

        db.session.add(QuizResult(score=score, total=len(quiz.questions), student_id=current_user.id, quiz_id=quiz.id))
        db.session.commit()
        flash(f"Quiz submitted! You scored {score}/{len(quiz.questions)}", "success")
        return redirect(url_for("main.course_detail", course_id=course.id))

    return render_template("take_quiz.html", quiz=quiz)