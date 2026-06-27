from flask import Blueprint
from app.routes.ai import ai_bp


main = Blueprint("main", __name__)

# Import submodules AFTER defining `main` so they can attach routes to it
from app.routes import home, auth, courses, lessons, assignments, quizzes, admin, grades, contact, ai  # noqa

main.register_blueprint(ai_bp)  # Register the AI blueprint