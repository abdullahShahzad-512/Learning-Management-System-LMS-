from flask import Blueprint

main = Blueprint("main", __name__)

# Import submodules AFTER defining `main` so they can attach routes to it
from app.routes import home, auth, courses, lessons, assignments, quizzes, admin  # noqa