from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from llm.gemini import Gemini
from llm.chatgpt import ChatGPT
from llm.base import Response, Turn
from llm.evaluation import SarcasmLevel, Judge

from llm.prompts import GEMINI_PROMPT, CHATGPT_PROMPT

# Define the request body model
class EvaluateRequest(BaseModel):
    sarcasm_level: str

# Create the FastAPI app instance
app = FastAPI()

# Mount the static files directory

def setup_models(selected_level):
    gemini = Gemini()
    model = 'gemini-2.5-flash'

    level_prompt = f"{GEMINI_PROMPT} You must use sarcasm that is {selected_level.value}"
    print(level_prompt)

    gemini.initialize(model, level_prompt)

    chatgpt = ChatGPT()
    gpt_model = 'gpt-4.1-nano'
    chatgpt.initialize(gpt_model, CHATGPT_PROMPT)

    return gemini, chatgpt, gpt_model


def run_conversation(gemini, chatgpt, gpt_model, num_turns):
    content = "Hey how is it going?"
    first_response = Response(sarcasm_presence=False, message=content)
    content = Turn(model="starter", response=first_response)

    model_evaluated = gpt_model
    print(
        f"Running test on sarcasm level: {model_evaluated}, {SarcasmLevel.HARD.name}"
    )
    conversation: list[Turn] = [content]
    for _ in range(0, num_turns):
        content = chatgpt.generate_structured_response(content.response)
        conversation.append(content)
        print()
        content = gemini.generate_structured_response(content.response)
        conversation.append(content)

    return conversation, model_evaluated


def evaluate_conversation(conversation, model_evaluated) -> str:
    judge_llm = Gemini()
    judge = Judge(model_evaluated, judge_llm)
    judge.score_detectability(conversation)
    
    return judge.evaluation_report 


def run():
    selected_level = SarcasmLevel.HARD
    gemini, chatgpt, gpt_model = setup_models(selected_level)
    conversation, model_evaluated = run_conversation(gemini, chatgpt,
                                                     gpt_model, 4)
    evaluate_conversation(conversation, model_evaluated)


@app.post("/api/evaluate")
async def evaluate(request: EvaluateRequest):
    """
    Accepts a sarcasm level and returns a current conversation. #TODO: fix the description
    """
    print("evaluate")
    selected_level = SarcasmLevel[request.sarcasm_level]
    gemini, chatgpt, gpt_model = setup_models(selected_level)
    conversation, model_evaluated = run_conversation(gemini, chatgpt,
                                                     gpt_model, 4)
    evaluation_report = evaluate_conversation(conversation, model_evaluated)
    return {
        "conversation": conversation,
        "evaluation_result": evaluation_report,
    }

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
