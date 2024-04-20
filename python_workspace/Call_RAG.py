import os
import sys
import openai
from dotenv import load_dotenv, find_dotenv
import logging

# Importing necessary modules and classes from langchain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma


# Setup logging
logging.basicConfig(level=logging.ERROR)


def load_environment_variables():
    """Load and return environment variables."""
    _ = load_dotenv(find_dotenv())
    return os.environ["OPENAI_API_KEY"]


def initialize_embedding(api_key):
    """Initialize OpenAI embeddings with the provided API key."""
    openai.api_key = api_key
    return OpenAIEmbeddings()


def check_vector_store(path):
    """Check if the vector store exists at the given path and return a Chroma instance or raise an exception."""
    if not os.path.exists(path):
        raise FileNotFoundError(
            "Vector store not found. Please ensure the directory exists or provide a valid path."
        )
    return Chroma(
        persist_directory=path, embedding_function=initialize_embedding(openai.api_key)
    )


def run_qa_chain(llm, vectordb, question):
    """Run the QA chain to process and respond to a specific question."""
    # Build prompt
    template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say 'thanks for asking!' at the end of the answer. 
    {context}
    Question: {question}
    Helpful Answer:"""
    QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

    # Run chain
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever=vectordb.as_retriever(),
        return_source_documents=True,
        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
    )
    result = qa_chain.invoke({"query": question})
    return result["result"]


def ask(question):
    api_key = load_environment_variables()
    embedding = initialize_embedding(api_key)

    try:
        vectordb = check_vector_store("vectorstore/chroma/")
    except FileNotFoundError as e:
        logging.error(e)
        sys.exit(1)

    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0)

    return run_qa_chain(llm, vectordb, question)


if __name__ == "__main__":
    # main()
    question = "What is the difference between OFAC and COMIFAC?"
    ask(question)
