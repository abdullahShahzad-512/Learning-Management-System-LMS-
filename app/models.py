from app import db
from flask_login import UserMixin
from app import login_manager
from datetime import datetime 

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    password = db.Column(db.String(200), nullable=False)

    role = db.Column(db.String(20), default="student")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    teacher = db.relationship("User", backref="courses_created")


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("User", backref="enrollments")
    course = db.relationship("Course", backref="enrollments")

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    video_url = db.Column(db.String(300), nullable=True)
    content = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=0)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", backref="lessons")
class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", backref="assignments")


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.String(10), nullable=True)
    feedback = db.Column(db.Text, nullable=True)

    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"), nullable=False)

    student = db.relationship("User", backref="submissions")
    assignment = db.relationship("Assignment", backref="submissions")


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", backref="quizzes")


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)

    quiz = db.relationship("Quiz", backref="questions")


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)

    question = db.relationship("Question", backref="choices")


class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)

    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)

    student = db.relationship("User", backref="quiz_results")
    quiz = db.relationship("Quiz", backref="results")
