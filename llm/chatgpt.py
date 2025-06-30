from functools import singledispatch
import os
from dotenv import load_dotenv

from openai import OpenAI

from .base import LLM, Response, Turn

load_dotenv()


@singledispatch
def make_message(content):
    raise TypeError(f"Unsupoorted data type: {type(content).__name__}")


@make_message.register(str)
def _(content, role: str = "user"):
    return {
        "role": role,
        "content": content,
    }


@make_message.register(Response)
def _(content, role: str = "user"):
    return {
        "role": role,
        "content": content.message,
    }


class ChatGPT(LLM):

    def initialize(self, model, prompt):
        self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._model = model
        self._initialize_prompt(prompt)

    def _initialize_prompt(self, prompt):
        self._prompt = prompt
        self._history = [make_message(prompt, "developer")]

    def generate_response(self, content):
        self._history.append(make_message(content))
        self._current_response = self._client.chat.completions.create(
            model=self._model,
            messages=self._history,
        )
        print(
            f"{self._model}: {self._current_response.choices[0].message.content}"
        )
        self._history.append(self._current_response.choices[0].message)
        return self._current_response.choices[0].message.content

    def generate_structured_response(self, content: Response) -> Turn:
        self._history.append(make_message(content))
        self._current_response = self._client.responses.parse(
            model=self._model,
            input=self._history,
            text_format=Response,
        )
        print(f"{self._model}: {self._current_response.output_parsed}")
        self._history.append(
            make_message(self._current_response.output_parsed.message,
                         "assistant"))
        turn = Turn(model=self._model,
                    response=self._current_response.output_parsed)
        return turn
