import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from llm.base import Response, Turn
from llm.chatgpt import ChatGPT
from llm.evaluation import Judge, SarcasmLevel
from llm.gemini import Gemini
from llm.prompts import get_prompts


class EvaluateRequest(BaseModel):
    sarcasm_level: str
    model_to_evaluate: str


app = FastAPI()


def setup_models(selected_level, model_to_evaluate: str):
    gemini = Gemini()
    gemini_model_name = "gemini-2.5-flash"

    chatgpt = ChatGPT()
    gpt_model_name = "gpt-4.1-nano"

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


async def stream_conversation(model_to_test, partner_model, model_evaluated_name,
                            num_turns, sarcasm_level: SarcasmLevel):
    content = "Hey how is it going?"
    first_response = Response(sarcasm_presence=False, message=content)
    content = Turn(model="starter", response=first_response)

    print(
        f"Running test on sarcasm level: {model_evaluated_name}, {sarcasm_level.name}"
    )
    conversation: list[Turn] = [content]
    yield f"data: {json.dumps(content.model_dump())}\n\n"

    for _ in range(0, num_turns):
        content = model_to_test.generate_structured_response(content.response)
        conversation.append(content)
        yield f"data: {json.dumps(content.model_dump())}\n\n"
        await asyncio.sleep(0.1)

        content = partner_model.generate_structured_response(content.response)
        conversation.append(content)
        yield f"data: {json.dumps(content.model_dump())}\n\n"
        await asyncio.sleep(0.1)

    yield f"data: {json.dumps({'status': 'evaluating'})}\n\n"
    judge_llm = Gemini()
    judge = Judge(model_evaluated_name, judge_llm)
    judge.score_detectability(conversation)

    evaluation_report = judge.evaluation_report
    yield f"data: {json.dumps({'evaluation_result': evaluation_report})}\n\n"


@app.get("/api/options")
async def get_options():
    return {
        "models": [
            {"value": "gpt", "label": "GPT"},
            {"value": "gemini", "label": "Gemini"},
        ],
        "sarcasm_levels": [
            {"value": "EASY", "label": "Easy"},
            {"value": "MEDIUM", "label": "Medium"},
            {"value": "HARD", "label": "Hard"},
        ],
    }


@app.get("/api/evaluate")
async def evaluate(sarcasm_level: str, model_to_evaluate: str):
    print(f"Received request: sarcasm_level={sarcasm_level}, model_to_evaluate={model_to_evaluate}")
    selected_level = SarcasmLevel[sarcasm_level]
    model_to_test, partner_model, model_evaluated_name = setup_models(
        selected_level, model_to_evaluate)
    return StreamingResponse(
        stream_conversation(model_to_test, partner_model, model_evaluated_name, 4, selected_level),
        media_type="text/event-stream",
    )


app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="frontend")
