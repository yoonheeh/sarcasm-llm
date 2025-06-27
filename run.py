from llm.gemini import (
    Gemini,
)
from llm.chatgpt import ChatGPT


def run():
    gemini = Gemini()
    model = 'gemini-2.5-flash'
    prompt = "You are having a conversation with a friend. Respond very sarcastically only on your second turn."
    gemini.initialize(model, prompt)

    # ChatGPT
    chatgpt = ChatGPT()
    gpt_model = 'gpt-4.1-nano'
    gpt_prompt = "You are having a conversation with a friend about your loud neighbors."
    chatgpt.initialize(gpt_model, gpt_prompt) 

    content = "Hey how is it going?"
    num_turns = 4
    structured_content: Response = {
        "sarcasm_presence": False,
        "message": content,
    }

    conversation = [structured_content]
    for _ in range(0, num_turns):
        input("====")
        content = gemini.generate_structured_response(content)
        conversation.append(content)
        print()
        content = chatgpt.generate_structured_response(content)
        conversation.append(content)

def conversation_to_content(conversation):
    """Converts conversation (list[Response]) to content to be fed to 
    judge LLM."""
    pass

def evaluate(conversation):
    # initialize judge
    judge = Gemini()
    model = 'gemini-2.5-flash' #TODO: maybe use more advanced model?
    prompt = "You are an expert on sarcasm detection. Evaluate a conversation " 
             "between two parties, and evaluate sarcasm for the following "
             "criteria: clarity (how obvious the sarcasm was), relevance and "
             "naturalness (how well it integrates with rest of the conversation)"
             " on a scale of 1 to 10."
    judge.initialize(model, prompt)
    content = conversation_to_content(conversation)
    judge_response = judge.generate_structured_response(structure, content)


if __name__ == "__main__":
    run()
