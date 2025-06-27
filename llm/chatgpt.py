import os
from dotenv import load_dotenv 

from openai import OpenAI

from .base import LLM, Response

load_dotenv()

class ChatGPT(LLM):

    def initialize(self, model, prompt):
        self._client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self._model = model
        self._initialize_prompt(prompt)

    def _initialize_prompt(self, prompt):
        self._prompt = prompt
        self._history = [
            {
                "role": "developer",
                "content": prompt,
            }
        ]
    
    def _make_message(self, content):
        message = {
            "role": "user",
            "content": content,
        }
        return message

    def generate_response(self, content):
        self._history.append(self._make_message(content))
        self._current_response = self._client.chat.completions.create(
            model=self._model,
            messages=self._history,
        )
        print(f"{self._model}: {self._current_response.choices[0].message.content}")
        self._history.append(self._current_response.choices[0].message)
        return self._current_response.choices[0].message.content

    def generate_structured_response(self, content):
        self._history.append(self._make_message(content))
        self._current_response = self._client.responses.parse(
            model=self._model,
            input=self._history,
            text_format=Response,
        )
        print(f"{self._model}: {self._current_response.output_parsed.message}")
        self._history.append(self._current_response.output_parsed.message)
        return self._current_response.output_parsed


