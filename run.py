import argparse
from llm.evaluation import SarcasmLevel
from llm.experiment import setup_models, run_conversation, evaluate_conversation


def run(model_to_evaluate: str):
    selected_level = SarcasmLevel.HARD
    model_to_test, partner_model, model_evaluated_name = setup_models(
        selected_level, model_to_evaluate)
    conversation, model_evaluated = run_conversation(model_to_test, partner_model,
                                                     model_evaluated_name, 4)
    evaluate_conversation(conversation, model_evaluated)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("model", choices=["gpt", "gemini"], help="Model to evaluate")
    args = parser.parse_args()
    run(args.model)