import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from llm.base import Response, Turn
from llm.evaluation import Judge, SarcasmLevel
from llm.gemini import Gemini
from llm.experiment import setup_models


class EvaluateRequest(BaseModel):
    sarcasm_level: str
    model_to_evaluate: str


app = FastAPI()


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
