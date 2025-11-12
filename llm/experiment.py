from llm.gemini import Gemini
from llm.chatgpt import ChatGPT
from llm.base import Response, Turn
from llm.evaluation import SarcasmLevel, Judge
from llm.prompts import get_prompts


def setup_models(selected_level, model_to_evaluate: str):
    gemini = Gemini()
    gemini_model_name = 'gemini-2.5-flash'

    chatgpt = ChatGPT()
    gpt_model_name = 'gpt-4.1-nano'

    model_prompt, partner_prompt = get_prompts(selected_level.value)

    if model_to_evaluate == "gemini":
        print(f"Gemini prompt: {model_prompt}")
        print(f"ChatGPT prompt: {partner_prompt}")
        gemini.initialize(gemini_model_name, model_prompt)
        chatgpt.initialize(gpt_model_name, partner_prompt)
        model_evaluated_name = gemini_model_name
        model_to_test = gemini
        partner_model = chatgpt
    elif model_to_evaluate == "gpt":
        print(f"ChatGPT prompt: {model_prompt}")
        print(f"Gemini prompt: {partner_prompt}")
        chatgpt.initialize(gpt_model_name, model_prompt)
        gemini.initialize(gemini_model_name, partner_prompt)
        model_evaluated_name = gpt_model_name
        model_to_test = chatgpt
        partner_model = gemini
    else:
        raise ValueError("Invalid model to evaluate. Choose 'gpt' or 'gemini'.")

    return model_to_test, partner_model, model_evaluated_name


def run_conversation(model_to_test, partner_model, model_evaluated, num_turns):
    content = "Hey how is it going?"
    first_response = Response(sarcasm_presence=False, message=content)
    content = Turn(model="starter", response=first_response)

    print(
        f"Running test on sarcasm level: {model_evaluated}, {SarcasmLevel.HARD.name}"
    )
    conversation: list[Turn] = [content]
    for _ in range(0, num_turns):
        content = model_to_test.generate_structured_response(content.response)
        conversation.append(content)
        print()
        content = partner_model.generate_structured_response(content.response)
        conversation.append(content)

    return conversation, model_evaluated


def evaluate_conversation(conversation, model_evaluated):
    judge_llm = Gemini()
    judge = Judge(model_evaluated, judge_llm)
    judge.score_detectability(conversation)
