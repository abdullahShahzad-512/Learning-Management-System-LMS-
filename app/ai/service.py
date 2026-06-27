from flask import current_app
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)


class AIService:

    def __init__(self):

        self.client = OpenAI( base_url=current_app.config["AI_ENDPOINT"],api_key=current_app.config["AI_API_KEY"] )
        self.model = current_app.config["AI_MODEL"]
    def generate(self,user_prompt,system_prompt="",temperature=0.5):
        try:

            response = self.client.chat.completions.create(model=self.model,temperature=temperature,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {
                        "role": "user",
                        "content": user_prompt,
                    }
                ]
            )

            return response.choices[0].message.content.strip()

        except Exception as e:

            logger.exception(e)

            raise RuntimeError(f"AI Generation Failed: {e}")