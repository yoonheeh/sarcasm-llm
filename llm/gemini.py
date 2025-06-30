import os
from functools import singledispatch
from dotenv import load_dotenv

from google import genai
from google.genai import types

from .base import LLM, Response, Turn

load_dotenv()


@singledispatch
def parse_content(content):
    raise TypeError(f"Unsupported data type: {type(content).__name__}")


@parse_content.register(str)
def _(content):
    return content


@parse_content.register(Response)
def _(content):
    return content.message


class Gemini(LLM):

    def initialize(self, model, prompt):
        self._client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        self._model = model
        self._prompt = prompt
        self._chat_config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                thinking_budget=0),  # -1 to enable
            system_instruction=self._prompt,
            response_mime_type="application/json",
            response_schema=Response,
        )
        self._chat = self._client.chats.create(
            model=self._model,
            config=self._chat_config,
        )

    def generate_response(self, content):
        """Generates and returns text (str) response."""
        self._contents.append(parse_content(content))
        self._current_response = self._client.models.generate_content(
            model=self._model,
            contents=self._contents,
            config=types.GenerateContentConfig(
                system_instruction=self._prompt),
        )
        print(f"{self._model}: {self._current_response.text}")
        return self._current_response.text

    def generate_structured_response(self, content: Response) -> Turn:
        """Generates and returns structured output of type Response."""
        self._contents.append(parse_content(content))
        self._current_response = self._chat.send_message(
            parse_content(content))

        print(f"{self._model}: {self._current_response.text}")
        turn = Turn(model=self._model,
                    response=Response.model_validate_json(
                        self._current_response.text))
        return turn
