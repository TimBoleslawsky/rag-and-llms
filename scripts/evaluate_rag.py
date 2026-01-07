import argparse
import json
import os
from datetime import datetime

from utils import ConfigHandler, RAG, GithubContextPromptV1, CounterfactualPromptV1, MedicalContextPromptV1


def evaluate_rag(config):
    """Comprehensive evaluation of the RAG pipeline. """
    print("=================Building RAG Pipeline:=================")
    rag = RAG(config)

    print("=================Evaluation:=================")
    num_rag_is_correct = 0
    num_model_without_context_is_correct = 0
    num_model_with_context_is_correct = 0
    num_retrieval_is_correct = 0

    example_questions = rag.questions.head(50)
    iteration = 0

    detailed_results = []

    if config.prompt_name == "MedicalContextPromptV1":
        prompt = MedicalContextPromptV1().get_prompt()
    elif config.prompt_name == "CounterfactualPromptV1":
        prompt = CounterfactualPromptV1().get_prompt()
    elif config.prompt_name == "GithubContextPromptV1":
        prompt = GithubContextPromptV1().get_prompt()
    else:
        raise ValueError(f"Unknown prompt name: {config.prompt_name}")

    for question in example_questions.itertuples():
        iteration += 1
        result_rag = rag.rag_chain.invoke(question.question)
        prompt_with_question = prompt.format(
            context="",
            question=question.question
        )
        prompt_with_question_and_context = prompt.format(
            context=rag.documents.loc[question.gold_document_id, "content"],
            question=question.question
        )
        result_model_without_context = rag.llm.invoke(prompt_with_question)
        result_model_with_context = rag.llm.invoke(prompt_with_question_and_context)
        answer_rag = result_rag["answer"].strip().lower()
        answer_model_without_context = result_model_without_context.strip().lower()
        answer_model_with_context = result_model_with_context.strip().lower()
        gold_answer = question.gold_label.lower()

        retrieved_document_id = result_rag["retrieved_docs"][0].metadata["id"]
        gold_document_id = question.gold_document_id

        rag_correct = answer_rag.startswith(gold_answer)
        model_without_context_correct = answer_model_without_context.startswith(gold_answer)
        model_with_context_correct = answer_model_with_context.startswith(gold_answer)
        retrieval_correct = retrieved_document_id == gold_document_id

        if rag_correct:
            num_rag_is_correct += 1
        if model_without_context_correct:
            num_model_without_context_is_correct += 1
        if retrieval_correct:
            num_retrieval_is_correct += 1
        if model_with_context_correct:
            num_model_with_context_is_correct += 1

        detailed_results.append({
            "iteration": iteration,
            "question": question.question,
            "rag_answer": answer_rag,
            "answer_model_without_context": answer_model_without_context,
            "answer_model_with_context": answer_model_with_context,
            "gold_answer": gold_answer,
            "rag_correct": rag_correct,
            "model_without_context_correct": model_without_context_correct,
            "model_with_context_correct": model_with_context_correct,
            "retrieval_correct": retrieval_correct,
            "retrieved_document_id": retrieved_document_id,
            "gold_document_id": gold_document_id
        })

        # Every 25 iteration, print example results (question.Index is random)
        if iteration % 25 == 0:
            print(f"--- Example for Iteration {iteration} ---")
            print("Question:", question.question)
            print("RAG Answer:", answer_rag[:50])
            print("Model Alone without Context Answer:", answer_model_without_context[:50])
            print("Model Alone with Context Answer:", answer_model_with_context[:50])
            print("Gold Answer:", gold_answer)
            print("RAG Correct:", rag_correct)
            print("Model Alone without Context Correct:", model_without_context_correct)
            print("Model Alone with Context Correct:", model_with_context_correct)
            print("Retrieved Document ID:", retrieved_document_id)
            print("Gold Document ID:", gold_document_id)
            print("Retrieval Correct:", retrieval_correct)
            print("Retrieved Document Content:", result_rag["retrieved_docs"][0].page_content)

    rag_accuracy = num_rag_is_correct / len(example_questions)
    model_without_context_accuracy = num_model_without_context_is_correct / len(example_questions)
    model_with_context_accuracy = num_model_with_context_is_correct / len(example_questions)
    retrieval_accuracy = num_retrieval_is_correct / len(example_questions)

    print("RAG Accuracy:", rag_accuracy)
    print("Model Alone without Context Accuracy:", model_without_context_accuracy)
    print("Model Alone with Context Accuracy:", model_with_context_accuracy)
    print("Retrieval Accuracy:", retrieval_accuracy)

    # Save results to file
    os.makedirs("results", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"results/evaluation_{timestamp}.json"

    results_data = {
        "timestamp": datetime.now().isoformat(),
        "config": vars(config),
        "summary": {
            "total_questions": len(example_questions),
            "rag_accuracy": rag_accuracy,
            "model_without_context_accuracy": model_without_context_accuracy,
            "model_with_context_accuracy": model_with_context_accuracy,
            "retrieval_accuracy": retrieval_accuracy,
            "rag_correct": num_rag_is_correct,
            "model_without_context_correct": num_model_without_context_is_correct,
            "model_with_context_correct": num_model_with_context_is_correct,
            "retrieval_correct": num_retrieval_is_correct
        },
        "detailed_results": detailed_results
    }

    with open(results_file, "w") as f:
        json.dump(
            results_data,
            f,
            indent=2,
            default=lambda o: vars(o) if hasattr(o, "__dict__") else str(o)
        )

    print(f"\nResults saved to: {results_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    arguments = parser.parse_args()
    config_handler = ConfigHandler()
    current_config = config_handler.handle_config(arguments)

    evaluate_rag(current_config)
