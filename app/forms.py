from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, DateField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    role = SelectField(
        "I am a...",
        choices=[("student", "Student"), ("teacher", "Teacher")],
        validators=[DataRequired()]
    )
    submit = SubmitField("Register")

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class CourseForm(FlaskForm):
    title = StringField("Course Title", validators=[DataRequired(), Length(min=3, max=150)])
    description = TextAreaField("Description", validators=[Optional()])
    submit = SubmitField("Create Course")

class LessonForm(FlaskForm):
    title = StringField("Lesson Title", validators=[DataRequired(), Length(min=3, max=150)])
    video_url = StringField("Video URL", validators=[Optional(), Length(max=300)])
    content = TextAreaField("Lesson Notes / Content", validators=[Optional()])
    submit = SubmitField("Add Lesson")
class AssignmentForm(FlaskForm):
    title = StringField("Assignment Title", validators=[DataRequired(), Length(min=3, max=150)])
    description = TextAreaField("Description", validators=[Optional()])
    due_date = DateField("Due Date", validators=[Optional()], format="%Y-%m-%d")
    submit = SubmitField("Create Assignment")


class SubmissionForm(FlaskForm):
    content = TextAreaField("Your Submission", validators=[DataRequired()])
    submit = SubmitField("Submit Assignment")


class GradeForm(FlaskForm):
    grade = StringField("Grade", validators=[DataRequired()])
    feedback = TextAreaField("Feedback", validators=[Optional()])
    submit = SubmitField("Save Grade")


class QuizForm(FlaskForm):
    title = StringField("Quiz Title", validators=[DataRequired(), Length(min=3, max=150)])
    submit = SubmitField("Create Quiz")


class QuestionForm(FlaskForm):
    text = StringField("Question", validators=[DataRequired()])
    choice1 = StringField("Choice 1", validators=[DataRequired()])
    choice2 = StringField("Choice 2", validators=[DataRequired()])
    choice3 = StringField("Choice 3", validators=[Optional()])
    choice4 = StringField("Choice 4", validators=[Optional()])
    correct_choice = SelectField("Correct Choice", choices=[("1","1"),("2","2"),("3","3"),("4","4")])
    submit = SubmitField("Add Question")