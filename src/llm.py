import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


class GeminiLLM:

    @staticmethod
    def load():

        client = genai.Client(
            api_key=os.getenv("GOOGLE_API_KEY")
        )

        return client