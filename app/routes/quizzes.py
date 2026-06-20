from flask import render_template, redirect, url_for, flash, abort, request
from flask_login import login_required, current_user
from app import db
from app.routes import main
from app.models import Course, Quiz, Question, Choice, QuizResult
from app.forms import QuizForm, QuestionForm


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