from flask import Blueprint,jsonify,request
from app.ai.course_generator import CourseGenerator
from app.ai.lesson_generator import LessonGenerator
from flask_login import login_required, current_user


ai_bp = Blueprint("ai",__name__,url_prefix="/api/ai")


@ai_bp.route("/course-description",methods=["POST"])
@login_required
def generate_course_description():
    try:

        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        if not data:

            return jsonify({

                "success": False,

                "message": "Invalid request."

            }), 400

        title = data.get("title", "").strip()

        generator = CourseGenerator()

        description = generator.generate_description(title)
        return jsonify({

            "success": True,

            "description": description

        }),200

    except ValueError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

    except Exception as e:

        return jsonify({

            "success": False,

            "message": "Unable to generate description.",

            "error": str(e)

        }), 500

@ai_bp.route("/lesson-content",methods=["POST"])
@login_required
def generate_lesson_content():
    try:

        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        if not data:

            return jsonify({

                "success": False,

                "message": "Invalid request."

            }), 400
        course_title = data.get("course_title", "").strip()
        lesson_title = data.get("lesson_title", "").strip()

        generator = LessonGenerator()

        lesson_content = generator.generate_content(
            course_title=course_title,
            lesson_title=lesson_title
        )
        return jsonify({

            "success": True,

            "lesson_content": lesson_content

        }),200

    except ValueError as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 400

    except Exception as e:

        return jsonify({

            "success": False,

            "message": "Unable to generate lesson content.",

            "error": str(e)

        }), 500