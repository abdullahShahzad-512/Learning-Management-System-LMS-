import json

from app.ai.service import AIService
from app.ai.prompts import AIPrompts


class QuizGenerator:

    def __init__(self):
        self.ai_service = AIService()

    def generate_quiz(self,course_title: str,lesson_title: str,difficulty: str = "Medium",question_count: int = 10) -> dict:

        course_title = course_title.strip()
        lesson_title = lesson_title.strip()

        if not course_title or not lesson_title:
            raise ValueError("Both course title and lesson title are required.")

        if len(course_title) < 3 or len(lesson_title) < 3:
            raise ValueError("Both course title and lesson title must contain at least 3 characters.")

        system_prompt = AIPrompts.QUIZ_SYSTEM

        user_prompt = AIPrompts.quiz(course_title,lesson_title,difficulty,question_count)

        response = self.ai_service.generate(system_prompt=system_prompt,user_prompt=user_prompt,temperature=1)

        try:
            return json.loads(response)

        except json.JSONDecodeError:
            raise ValueError("AI returned an invalid JSON response.")