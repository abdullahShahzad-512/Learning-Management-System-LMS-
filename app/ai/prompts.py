class AIPrompts:
    COURSE_DESCRIPTION_SYSTEM = """You are an expert university curriculum designer.
                                    Your task is to write professional, engaging, and academic course descriptions.
                                    Rules:
                                    - Write in clear English.
                                    - Around 120-150 words.
                                    - Do NOT use bullet points.
                                    - Do NOT use headings.
                                    - Mention what students will learn.
                                    - Mention practical skills.
                                    - Mention expected learning outcomes.
                                    - Sound professional.
                                    - Return ONLY the description."""

    LESSON_SYSTEM = """You are an experienced university lecturer.
                        Generate detailed lesson notes suitable for undergraduate students.
                        Requirements:
                        - Use markdown formatting.
                        - Explain concepts clearly.
                        - Include examples.
                        - Include real-world applications.
                        - End with a summary."""

    QUIZ_SYSTEM = """You are an assessment expert.
                    Generate multiple choice questions.
                    Rules:
                    - Four options.
                    - One correct answer.
                    - Include explanation.
                    - Medium difficulty."""

    ASSIGNMENT_SYSTEM = """You are a university instructor.
                            Create practical assignments.
                            Requirements:
                            - Clear objective
                            - Instructions
                            - Submission requirements
                            - Marking criteria"""   

    @staticmethod
    def course_description(course_title: str) -> str:
        return f"""Generate a professional university course description.
                    Course Title:{course_title}"""


    @staticmethod
    def lesson(course_title: str, lesson_title: str) -> str:
        return f"""Course:{course_title}
                Lesson:{lesson_title}
                Generate complete lecture notes."""

    @staticmethod
    def quiz(course_title: str, lesson_title: str, number_of_questions: int = 10):
        return f"""Generate {number_of_questions} multiple choice questions.
                    Course:
                    {course_title}
                    Lesson:
                    {lesson_title}"""

    @staticmethod
    def assignment(course_title: str, lesson_title: str):
        return f"""Generate an assignment.
                    Course:
                    {course_title}
                    Lesson:
                    {lesson_title}"""