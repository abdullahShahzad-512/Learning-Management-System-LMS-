from app import db
from flask_login import UserMixin
from datetime import datetime


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")  # only meaningful value: "admin"

    def is_admin(self):
        return self.role == "admin"

    def is_teacher_of(self, course):
        return self.id == course.teacher_id

    def is_enrolled_in(self, course):
        return Enrollment.query.filter_by(student_id=self.id, course_id=course.id).first() is not None


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    thumbnail = db.Column(db.String(255), default="uploads/thumbnails/default-cover-banner.jpg")  
    teacher = db.relationship("User", backref=db.backref("courses_created", cascade="all, delete-orphan"))


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("User", backref=db.backref("enrollments", cascade="all, delete-orphan"))
    course = db.relationship("Course", backref=db.backref("enrollments", cascade="all, delete-orphan"))


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    video_url = db.Column(db.String(300), nullable=True)
    content = db.Column(db.Text, nullable=True)
    order = db.Column(db.Integer, default=0)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", backref=db.backref("lessons", cascade="all, delete-orphan"))


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", backref=db.backref("assignments", cascade="all, delete-orphan"))


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    grade = db.Column(db.String(10), nullable=True)
    feedback = db.Column(db.Text, nullable=True)

    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    assignment_id = db.Column(db.Integer, db.ForeignKey("assignment.id"), nullable=False)

    student = db.relationship("User", backref=db.backref("submissions", cascade="all, delete-orphan"))
    assignment = db.relationship("Assignment", backref=db.backref("submissions", cascade="all, delete-orphan"))


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    course = db.relationship("Course", backref=db.backref("quizzes", cascade="all, delete-orphan"))


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)

    quiz = db.relationship("Quiz", backref=db.backref("questions", cascade="all, delete-orphan"))


class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200), nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"), nullable=False)

    question = db.relationship("Question", backref=db.backref("choices", cascade="all, delete-orphan"))


class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)
    taken_at = db.Column(db.DateTime, default=datetime.utcnow)

    student_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)

    student = db.relationship("User", backref=db.backref("quiz_results", cascade="all, delete-orphan"))
    quiz = db.relationship("Quiz", backref=db.backref("results", cascade="all, delete-orphan"))