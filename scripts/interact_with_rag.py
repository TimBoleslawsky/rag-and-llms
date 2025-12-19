import argparse

from utils import RAG, ConfigHandler


def interact_with_rag(config):
    """" Builds interactive session with the RAG pipeline. """
    print("=================Building RAG Pipeline=================")
    rag = RAG(config)

    print("=================Interactive RAG Session:=================")
    while True:
        user_question = input("Enter your question (or type 'exit' to quit): ")
        if user_question.lower() == 'exit':
            print("Exiting the interactive session.")
            break

        result_rag = rag.rag_chain.invoke(user_question)
        answer_rag = result_rag["answer"].strip()

        print("\nRAG Answer:")
        print(answer_rag)
        print("\nRetrieved Document Content:")
        print(result_rag["retrieved_docs"][0].page_content)
        print("--------------------------------------------------")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to the YAML configuration file.")
    arguments = parser.parse_args()
    config_handler = ConfigHandler()
    current_config = config_handler.handle_config(arguments)

    interact_with_rag(current_config)
