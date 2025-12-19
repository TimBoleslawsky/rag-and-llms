# RAG and LLMs

NOTE: Data folder is not included in this repository (too big). Please create a `data` folder and add your documents
there.

## Usage

To use the functionalities in this repository, choose one of the following options:

1. Evaluate a RAG system with a predefined set of questions. For this option, run the following command (assuming the
   medical dataset is in the `data` folder):
   ```bash
   uv run python -m scripts.evaluate_rag --config "./configs/medical_rag_eval_config.yaml"
   ```
2. Interactively chat with a RAG system. For this option, run the following command:
   ```bash
   uv run python -m scripts.interact_with_rag --config "./configs/obsidian_rag_interaction_config.yaml"
   ```