# LLM Eval: Sarcasm Edition

This project is an experiment to explore how well Large Language Models (LLMs) can understand and generate sarcasm. It follows up on the blog post ["Experiment: how well can LLMs understand sarcasm? (Part 1)"](https://yoonheeha.com/posts/sarcasm_and_llm_pt1), where "sarcasm detectability" was measured subjectively. This project aims to create a more grounded and objective way to measure this capability.

For this experiment, we are comparing two LLMs: Gemini and ChatGPT.

## Test Setup

The experiment involves a conversation between two LLMs: Google's **Gemini (`gemini-2.5-flash`)** and OpenAI's **ChatGPT (`gpt-4.1-nano`)**.

1.  **Conversation:** One model is prompted to make a sarcastic comment at a specific turn in the conversation.
2.  **Reaction:** The other model has to react to the sarcastic comment.
3.  **Evaluation:** A third "judge" LLM (using Gemini) is then used to evaluate the conversation. It scores the sarcastic model's ability to generate natural-sounding sarcasm and the other model's ability to detect it. The evaluation is based on criteria such as clarity, relevance, and naturalness.

## Project Structure

```
/
├── llm/                  # Core logic for LLMs, evaluation, and prompts
│   ├── experiment.py     # Main experiment logic (setup, conversation, evaluation)
│   ├── gemini.py         # Gemini-specific implementation
│   ├── chatgpt.py        # ChatGPT-specific implementation
│   └── base.py           # Abstract base classes and data models
├── frontend/             # Simple TypeScript frontend for the web server
├── run.py                # Command-line interface (CLI) to run the experiment
├── main.py               # FastAPI web server to run the experiment via a UI
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

## Getting Started

### Prerequisites

*   Python 3.10+
*   An OpenAI API key
*   A Gemini API key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd llm-eval
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API keys:**
    Create a `.env` file in the root of the project and add your API keys:
    ```
    OPENAI_API_KEY="sk-..."
    GEMINI_API_KEY="..."
    ```

## How to Run

You can run the experiment using either the command-line interface or the web server.

### 1. Command-Line Interface

The CLI runs the experiment in your terminal and prints the conversation and evaluation results.

To run the experiment, use the `run.py` script with the model you want to evaluate for sarcasm generation (`gpt` or `gemini`).

```bash
# Evaluate ChatGPT's ability to generate sarcasm
python run.py gpt

# Evaluate Gemini's ability to generate sarcasm
python run.py gemini
```

### 2. Web Server

The web server provides a simple UI to run the experiment and see the results.

1.  **Launch the server:**
    Use `uvicorn` to start the FastAPI server.
    ```bash
    uvicorn main:app --reload
    ```

2.  **Access the UI:**
    Open your web browser and navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000).

    From the UI, you can select the model to evaluate and the sarcasm level, then run the experiment.

