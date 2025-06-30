from abc import ABC, abstractmethod
from pydantic import BaseModel


class Response(BaseModel):
    sarcasm_presence: bool
    message: str


class Turn(BaseModel):
    model: str
    response: Response


class LLM(ABC):

    def __init__(self):
        self._model = ""  # which model to run (e.g. 'gemini-2.5-flash')
        self._take_first_turn = False
        self._contents = []
        self._current_response = ""

    @abstractmethod
    def initialize(self, model, prompt):
        """Initialize with API keys and such"""
        pass

    @abstractmethod
    def generate_response(self, context):
        """Generates responses, given a context and updates current_response."""
        pass

    @property
    def current_reponse(self):
        return self._current_response
