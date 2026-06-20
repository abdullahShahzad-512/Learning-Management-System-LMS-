from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.routes import main
from app.decorators import admin_required
from app.models import User, Course, Enrollment, QuizResult


@main.route("/admin")
@login_required
@admin_required
def admin_dashboard():
    total_users = User.query.count()
    total_courses = Course.query.count()
    total_enrollments = Enrollment.query.count()
    total_quiz_attempts = QuizResult.query.count()
    recent_users = User.query.order_by(User.id.desc()).limit(5).all()

    return render_template(
        "admin_dashboard.html",
        total_users=total_users,
        total_courses=total_courses,
        total_enrollments=total_enrollments,
        total_quiz_attempts=total_quiz_attempts,
        recent_users=recent_users
    )


@main.route("/admin/users")
@login_required
@admin_required
def admin_users():
    users = User.query.all()
    return render_template("admin_users.html", users=users)


@main.route("/admin/users/<int:user_id>/toggle-admin", methods=["POST"])
@login_required
@admin_required
def toggle_admin(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You can't change your own admin status.", "danger")
        return redirect(url_for("main.admin_users"))

    user.role = "user" if user.is_admin() else "admin"
    db.session.commit()
    flash(f"{user.username}'s role updated.", "success")
    return redirect(url_for("main.admin_users"))


@main.route("/admin/users/<int:user_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash("You can't delete your own account.", "danger")
        return redirect(url_for("main.admin_users"))

    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", "info")
    return redirect(url_for("main.admin_users"))


@main.route("/admin/courses/<int:course_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    flash("Course deleted.", "info")
    return redirect(url_for("main.admin_courses"))


@main.route("/admin/courses")
@login_required
@admin_required
def admin_courses():
    courses = Course.query.all()
    return render_template("admin_courses.html", courses=courses)