from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFacePipeline
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

from .process_data import MedicalDataProcessor, GithubDataProcessor
from .prompts import MedicalContextPromptV1, GithubContextPromptV1


class RAG:
    def __init__(self, config):
        self.llm = None

        # Load documents based on type
        if config.documents.type == "medical":
            self.documents, self.questions = MedicalDataProcessor.load_data()
        elif config.documents.type == "github":
            self.documents = GithubDataProcessor.load_data(
                owner=config.documents.owner,
                repo=config.documents.repo,
                path=config.documents.path,
            )
            self.questions = None
        else:
            raise ValueError(f"Unknown document type: {config.documents.type}")

        # Build RAG chain
        self.rag_chain = self.build_rag_chain(
            model_config=config.model_config,
            embedding_model_name=config.embedding_model_name,
            prompt_name=config.prompt_name,
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap
        )

    def build_rag_chain(self, model_config, embedding_model_name, prompt_name, chunk_size,
                        chunk_overlap):
        """Build a RAG chain using HuggingFace model and Chroma vector store."""

        # Load HuggingFace model
        self.llm = self._load_model(model_config)

        # Load embedding model
        embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)

        # Chunk the documents using RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        metadata = [{"id": idx} for idx in self.documents.index]
        documents = text_splitter.create_documents(texts=self.documents.content.tolist(), metadatas=metadata)
        split_documents = text_splitter.split_documents(documents)

        # Defining a vector store using Chroma
        vector_store = Chroma.from_documents(documents=split_documents, embedding=embedding_model)

        # Create RAG chain
        if prompt_name == "MedicalContextPromptV1":
            prompt = MedicalContextPromptV1().get_prompt()
        elif prompt_name == "GithubContextPromptV1":
            prompt = GithubContextPromptV1().get_prompt()
        else:
            raise ValueError(f"Unknown prompt name: {prompt_name}")

        retriever = vector_store.as_retriever(search_kwargs={"k": 1})
        runnable_parallel = RunnableParallel(
            context=retriever | (lambda docs: "\n\n".join(doc.page_content for doc in docs)),
            question=RunnablePassthrough(),
            retrieved_docs=retriever
        )
        chain = (
                prompt
                | self.llm
                | StrOutputParser()
        )
        rag_chain = runnable_parallel.assign(answer=chain)

        return rag_chain

    @staticmethod
    def _load_model(model_config) -> HuggingFacePipeline:
        """Load a HuggingFace model."""

        # Load a model that is free to use
        tokenizer = AutoTokenizer.from_pretrained(model_config.name)
        model = AutoModelForCausalLM.from_pretrained(model_config.name)

        # Set pad token for batching
        tokenizer.pad_token = tokenizer.eos_token

        hf_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_length=model_config.max_length,
            return_full_text=False,
            batch_size=4,
            do_sample=True,
            temperature=model_config.temperature
        )
        llm = HuggingFacePipeline(pipeline=hf_pipeline)

        return llm
