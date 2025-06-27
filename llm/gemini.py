import os
from dotenv import load_dotenv

from google import genai
from google.genai import types

from .base import LLM, Response

load_dotenv()

class Gemini(LLM):

    def initialize(self, model, prompt):
        self._client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self._model = model
        self._prompt = prompt

    def generate_response(self, content):
        """Generates and returns text (str) response."""
        self._contents.append(content)
        self._current_response = self._client.models.generate_content(
            model=self._model,
            contents=self._contents,
            config=types.GenerateContentConfig(
                system_instruction=self._prompt
            ),
        )
        print(f"{self._model}: {self._current_response.text}")
        return self._current_response.text

    def generate_structured_response(self, content):
        """Generates and returns structured output of type Response."""
        self._contents.append(content)
        self._current_response = self._client.models.generate_content(
            model=self._model,
            contents=self._contents,
            config=types.GenerateContentConfig(
                system_instruction=self._prompt,
                response_mime_type="application/json",
                response_schema=Response,
            ),
        )
        print(f"{self._model}: {self._current_response.candidates[0].content.parts[0].text}")
        #TODO: should response always be text or of type "Response"?
        return self._current_response.parsed
