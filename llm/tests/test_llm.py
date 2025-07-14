import pytest
from unittest.mock import patch
from llm.gemini import Gemini
from llm.chatgpt import ChatGPT


@pytest.fixture
def gemini():
    with patch('google.genai') as mock_genai:
        yield Gemini()


@pytest.fixture
def chatgpt():
    with patch('openai.OpenAI') as mock_openai:
        yield ChatGPT()


def test_gemini_initialization(gemini):
    gemini.initialize("gemini-2.5-flash", "test prompt")
    assert gemini._model == "gemini-2.5-flash"
    assert gemini._prompt == "test prompt"


def test_chatgpt_initialization(chatgpt):
    chatgpt.initialize("gpt-4.1-nano", "test prompt")
    assert chatgpt._model == "gpt-4.1-nano"
    assert chatgpt._prompt == "test prompt"
