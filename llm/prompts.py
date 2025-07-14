GEMINI_PROMPT = """You are having a conversation with a friend. Respond very 
                 sarcastically only once on your second turn. The rest of 
                 conversation should be conducted WITHOUT sarcasm."""

CHATGPT_PROMPT = "You are having a conversation with a friend. Discuss topic you are passionate about"

JUDGE_PROMPT = """You are an expert on sarcasm detection. Evaluate each turn of the conversation \ 
                 between two parties, and evaluate sarcasm for the following \
                 criteria: clarity (how obvious the sarcasm was), relevance and \
                 naturalness (how well it integrates with rest of the conversation) \ 
                  on a scale of 1 to 10. Be a very critical evaluator."""

EVALUATION_RUBRIC = """Evaluation rubric for relevance is as follows:
        1-3 (poor): the response ignores the sarcastic tone or is completely irrelevant to the topic.
        4-6 (fair): the response continues the topic but may miss the nuance of the sarcastic tone.
        7-8 (good): the response acknowledges the sarcastic tone and continues the conversation naturally.
        9-10 (excellent): the response is highly relevant, clverly plays along with or challenges the sarcasm, and feels very human-like.
        """