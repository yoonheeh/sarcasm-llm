from llm.gemini import Gemini
from llm.chatgpt import ChatGPT
from llm.base import Response, Turn

from enum import Enum


class SarcasmLevel(Enum):
    EASY = "very obvious"
    MEDIUM = "relatively obvious but some might not recognize"
    HARD = "very very subtle such that no one recognizes that it's a sarcasm"
    #TODO: better prompt needed to make more subtle sarcasm


def run():
    selected_level = SarcasmLevel.HARD

    gemini = Gemini()
    model = 'gemini-2.5-flash'
    prompt = """You are having a conversation with a friend. Respond very 
                 sarcastically only once on your second turn. The rest of 
                 conversation should be conducted WITHOUT sarcasm."""

    level_prompt = f"{prompt} You must use sarcasm that is {selected_level.value}"
    print(level_prompt)

    gemini.initialize(model, level_prompt)

    # ChatGPT
    chatgpt = ChatGPT()
    gpt_model = 'gpt-4.1-nano'
    gpt_prompt = "You are having a conversation with a friend. Discuss topic you are passionate about"
    chatgpt.initialize(gpt_model, gpt_prompt)

    content = "Hey how is it going?"
    num_turns = 4
    first_response = Response(sarcasm_presence=False, message=content)
    content = Turn(model="starter", response=first_response)

    model_evaluated = gpt_model
    print(
        f"Running test on sarcasm level: {model_evaluated}, {selected_level.name}"
    )
    conversation: list[Turn] = [content]
    for _ in range(0, num_turns):
        #input("===")
        content = chatgpt.generate_structured_response(content.response)
        conversation.append(content)
        print()
        content = gemini.generate_structured_response(content.response)
        conversation.append(content)

    evaluate(conversation, model_evaluated)


def conversation_to_content(conversation):
    """Converts conversation (list[Response]) to content to be fed to 
    judge LLM."""
    pass


class Judge:

    def __init__(self, model_evaluated):
        self._judge = Gemini()
        model = 'gemini-2.5-flash'  #TODO: maybe use more advanced model?
        prompt = """You are an expert on sarcasm detection. Evaluate each turn of the conversation \ 
                 between two parties, and evaluate sarcasm for the following \
                 criteria: clarity (how obvious the sarcasm was), relevance and \
                 naturalness (how well it integrates with rest of the conversation) \
                  on a scale of 1 to 10. Be a very critical evaluator."""
        evaluation_rubric = """Evaluation rubric for relevance is as follows:
        1-3 (poor): the response ignores the sarcastic tone or is completely irrelevant to the topic.
        4-6 (fair): the response continues the topic but may miss the nuance of the sarcastic tone.
        7-8 (good): the response acknowledges the sarcastic tone and continues the conversation naturally.
        9-10 (excellent): the response is highly relevant, clverly plays along with or challenges the sarcasm, and feels very human-like.
        """
        evaluation_criteria = f"{model_evaluated} is getting evaluated. Score {model_evaluated}'s response to sarcasm."
        prompt.join([evaluation_rubric, evaluation_criteria])
        self._judge.initialize(model, prompt)

    def score_detectability(self, conversation: list[Turn]):
        # need to define which model is getting evaluated
        # Test feeding directly to the model
        conversation_str = ''
        for conv in conversation:
            conversation_str += str(conv.model_dump())
        self._judge.generate_response(conversation_str)


def evaluate(conversation, model_evaluated):
    # initialize judge
    judge = Judge(model_evaluated)
    judge.score_detectability(conversation)


if __name__ == "__main__":
    run()
