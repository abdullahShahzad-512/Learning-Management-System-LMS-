from app.ai.service import AIService
from app.ai.prompts import AIPrompts


class LessonGenerator:
    def __init__(self):
        self.ai_service = AIService()

    def generate_content(self, course_title: str, lesson_title: str) -> str:
        if not course_title or not lesson_title:
            raise ValueError("Both course title and lesson title are required.")

        course_title = course_title.strip()
        lesson_title = lesson_title.strip()

        if len(course_title) < 3 or len(lesson_title) < 3:
            raise ValueError("Both course title and lesson title must contain at least 3 characters.")

        system_prompt = AIPrompts.LESSON_SYSTEM

        user_prompt = AIPrompts.lesson(course_title, lesson_title)

        lesson_content = self.ai_service.generate(system_prompt=system_prompt, user_prompt=user_prompt, temperature=0.5)

        return lesson_content