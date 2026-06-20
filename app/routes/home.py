from flask import render_template
from flask_login import login_required
from app.routes import main

@main.route("/")
def home():
    return render_template("home.html")

@main.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")