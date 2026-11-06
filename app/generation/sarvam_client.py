import os

from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()


class SarvamClient:

    def __init__(self):

        api_key = os.getenv("SARVAM_API_KEY")

        if not api_key:
            raise ValueError("SARVAM_API_KEY is missing")

        self.client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.sarvam.ai/v2",
            timeout=60.0,
            max_retries=2
        )

        self.model = os.getenv(
            "SARVAM_MODEL",
            "sarvam-105b"
        )

    async def generate(self, system_prompt: str, user_prompt: str):

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            temperature=0.1,
            max_tokens=1500
        )

        return {
            "answer": response.choices[0].message.content,
            "model": response.model,
            "usage": (
                response.usage.model_dump()
                if response.usage else None
            )
        }