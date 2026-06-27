from app.ai.service import AIService
from app.ai.prompts import AIPrompts


class CourseGenerator:
    def __init__(self):
        self.ai_service = AIService()

    def generate_description(self, course_title: str) -> str:
        if not course_title:
            raise ValueError("Course title is required.")

        course_title = course_title.strip()

        if len(course_title) < 3:
            raise ValueError("Course title must contain at least 3 characters.")

        system_prompt = AIPrompts.COURSE_DESCRIPTION_SYSTEM

        user_prompt = AIPrompts.course_description(course_title)

        description = self.ai_service.generate(system_prompt=system_prompt,user_prompt=user_prompt,temperature=0.7)

        return description