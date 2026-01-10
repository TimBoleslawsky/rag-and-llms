import json
import glob
import os

def normalize_answer(text):
    text = text.lower()
    if text.startswith("yes"):
        return "yes"
    elif text.startswith("no"):
        return "no"
    elif text.startswith("assistant: no"):
        return  "no"
    elif text.startswith("assistant: yes"):
        return "yes"
    else:
        return text.strip()

def recalc_accuracy(json_file):
    # Load the JSON data
    with open(json_file, "r") as f:
        data = json.load(f)

    total_questions = len(data["detailed_results"])
    rag_correct_count = 0
    model_without_context_correct_count = 0
    model_with_context_correct_count = 0
    retrieval_correct_count = 0

    # Process each question
    for item in data["detailed_results"]:
        # Normalize all answer fields to 'yes'/'no'
        item["answer_model_without_context"] = normalize_answer(item["answer_model_without_context"])
        item["answer_model_with_context"] = normalize_answer(item["answer_model_with_context"])
        item["rag_answer"] = normalize_answer(item["rag_answer"])

        # Update correctness flags based on gold_answer
        item["rag_correct"] = (item["rag_answer"] == item["gold_answer"])
        item["model_without_context_correct"] = (item["answer_model_without_context"] == item["gold_answer"])
        item["model_with_context_correct"] = (item["answer_model_with_context"] == item["gold_answer"])
        item["retrieval_correct"] = bool(item.get("retrieval_correct", False))

        # Count correct answers
        rag_correct_count += int(item["rag_correct"])
        model_without_context_correct_count += int(item["model_without_context_correct"])
        model_with_context_correct_count += int(item["model_with_context_correct"])
        retrieval_correct_count += int(item["retrieval_correct"])

    # Update summary section
    data["summary"]["total_questions"] = total_questions
    data["summary"]["rag_accuracy"] = rag_correct_count / total_questions
    data["summary"]["model_without_context_accuracy"] = model_without_context_correct_count / total_questions
    data["summary"]["model_with_context_accuracy"] = model_with_context_correct_count / total_questions
    data["summary"]["retrieval_accuracy"] = retrieval_correct_count / total_questions
    data["summary"]["rag_correct"] = rag_correct_count
    data["summary"]["model_without_context_correct"] = model_without_context_correct_count
    data["summary"]["model_with_context_correct"] = model_with_context_correct_count
    data["summary"]["retrieval_correct"] = retrieval_correct_count

    # Save corrected JSON
    filename = os.path.basename(json_file)
    corrected_file = os.path.join("results_corrected", f"{filename}_corrected.json")
    with open(corrected_file, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Processed and saved: {corrected_file}")

if __name__ == "__main__":
    for file in glob.glob(os.path.join("results", "*.json")):
        recalc_accuracy(file)