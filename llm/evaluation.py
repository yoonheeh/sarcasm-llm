from enum import Enum
from .base import LLM, Turn

class SarcasmLevel(Enum):
    EASY = "very obvious"
    MEDIUM = "relatively obvious but some might not recognize"
    HARD = "very very subtle such that no one recognizes that it's a sarcasm"

from .prompts import JUDGE_PROMPT, EVALUATION_RUBRIC

class Judge:

    def __init__(self, model_evaluated, judge_llm: LLM):
        self._judge = judge_llm
        self._evaluation_report = ""
        model = 'gemini-2.5-flash'  #TODO: maybe use more advanced model?
        evaluation_criteria = f"{model_evaluated} is getting evaluated. Score {model_evaluated}'s response to sarcasm."
        prompt = "\n".join([JUDGE_PROMPT, EVALUATION_RUBRIC, evaluation_criteria])
        self._judge.initialize(model, prompt)

    @property
    def evaluation_report(self):
        return self._evaluation_report

    def score_detectability(self, conversation: list[Turn]):
        # need to define which model is getting evaluated
        # Test feeding directly to the model
        conversation_str = ''
        for conv in conversation:
            conversation_str += str(conv.model_dump())
        self._evaluation_report = self._judge.generate_response(conversation_str)

