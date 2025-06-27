import pytest

from llm.gemini import Gemini
from llm.chatgpt import ChatGPT

LLM_MODELS = [Gemini, ChatGPT] 

@pytest.fixture(params=LLM_MODELS)
def llm_model(request):
    llm_model = request.param # one of LLM_MODELS
    client = llm_model()

    if isinstance(client, Gemini):
        model = 'gemini-2.5-flash'
    elif isinstance(client, ChatGPT):
        model = 'gpt-4.1-nano'
    else:
        model = 'default-model'

    prompt = "You are a helpful assistant."

    client.initialize(model, prompt)

    yield client
    

