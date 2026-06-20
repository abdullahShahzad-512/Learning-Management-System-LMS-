from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app import db
from app.routes import main
from app.models import Course, Assignment, Submission
from app.forms import AssignmentForm, SubmissionForm, GradeForm



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