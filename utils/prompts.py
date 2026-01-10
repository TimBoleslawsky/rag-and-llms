from langchain_core.prompts import ChatPromptTemplate


class MedicalContextPromptV1:
    @staticmethod
    def get_prompt() -> ChatPromptTemplate:
        template = """Based on the following medical context, if available, please answer the question ONLY with "yes" or "no", no other text.
        Context: {context}
        Question: {question}
        Answer:""".strip()
        prompt = ChatPromptTemplate.from_template(template)

        return prompt


class CounterfactualPromptV1:
    @staticmethod
    def get_prompt() -> ChatPromptTemplate:
        template = """Based on the following context, if available, please answer the question about a location by providing ONLY the location name.
        Context: {context}
        Question: {question}
        Answer:""".strip()
        prompt = ChatPromptTemplate.from_template(template)

        return prompt


class GithubContextPromptV1:
    @staticmethod
    def get_prompt() -> ChatPromptTemplate:
        template = """Based on the following GitHub documentation context, if available, please answer the question as accurately as possible.
        Context: {context}
        Question: {question}
        Answer:""".strip()
        prompt = ChatPromptTemplate.from_template(template)

        return prompt
