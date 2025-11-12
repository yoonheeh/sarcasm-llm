import argparse
from llm.gemini import Gemini
from llm.chatgpt import ChatGPT
from llm.base import Response, Turn
from llm.evaluation import SarcasmLevel, Judge

from llm.prompts import GEMINI_PROMPT, CHATGPT_PROMPT


def setup_models(selected_level, model_to_evaluate: str):
    gemini = Gemini()
    gemini_model_name = 'gemini-2.5-flash'

    chatgpt = ChatGPT()
    gpt_model_name = 'gpt-4.1-nano'

    if model_to_evaluate == "gemini":
        level_prompt = f"{GEMINI_PROMPT} You must use sarcasm that is {selected_level.value}"
        print(f"Gemini prompt: {level_prompt}")
        gemini.initialize(gemini_model_name, level_prompt)
        chatgpt.initialize(gpt_model_name, CHATGPT_PROMPT)
        model_evaluated_name = gemini_model_name
        model_to_test = gemini
        partner_model = chatgpt
    elif model_to_evaluate == "gpt":
        level_prompt = f"{CHATGPT_PROMPT} You must use sarcasm that is {selected_level.value}"
        print(f"ChatGPT prompt: {level_prompt}")
        chatgpt.initialize(gpt_model_name, level_prompt)
        gemini.initialize(gemini_model_name, GEMINI_PROMPT)
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


def run(model_to_evaluate: str):
    selected_level = SarcasmLevel.HARD
    model_to_test, partner_model, model_evaluated_name = setup_models(
        selected_level, model_to_evaluate)
    conversation, model_evaluated = run_conversation(model_to_test, partner_model,
                                                     model_evaluated_name, 4)
    evaluate_conversation(conversation, model_evaluated)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=["gpt", "gemini"], help="Model to evaluate")
    args = parser.parse_args()
    run(args.model)