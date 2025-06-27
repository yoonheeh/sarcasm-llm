#integration tests
import pytest

from llm.base import Response


@pytest.mark.integration
def test_generate_response(llm_model):

    content = "Can you help me with pytest?"
    resp = llm_model.generate_response(content)
    assert type(resp) == str

@pytest.mark.integration
def test_generate_structured_response(llm_model):
    content = "Can you help me with pytest?"
    resp = llm_model.generate_structured_response(content)
    structured_resp: Response = resp
    assert isinstance(structured_resp, Response)
