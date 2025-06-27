# LLM Eval (in progress)
On "Experiment: how well can LLMs understand sarcasm? (Part 1)" [blog post](https://yoonheeha.com/posts/sarcasm_and_llm_pt1),
"sarcasm detectability" was measured quite subjectively and qualitatively with me as the only judge. 
Then, I got interested in properly measuring how good they are, so that my claim
can have at least a little grounding. 

For this experiment, I am going to compare just two LLMs: ChatGPT and Gemini. 

## Test Setup
Gemini (`gemini-2.5-flash`) and ChatGPT (`gpt-4.1-nano`) are setup to carry
out conversation. One will be prompted to make a sarcastc comment
and the other will have to react to the sarcastic comment.

Later whether the model receiving the sarcastic comment will be evaluated
 on whether the caught that the comment was sarcastic, along with presence of
sarcasm, sarcasm level (how intense it was) and relevance. 


