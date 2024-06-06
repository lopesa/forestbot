import os
import sys
from typing import Any
import openai
import logging

# Importing necessary modules and classes from langchain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA, create_history_aware_retriever
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain

# example question:
# What is the difference between OFAC and COMIFAC?

# Setup logging
logging.basicConfig(level=logging.ERROR)
class RAGService:
    def __init__(self, model_name="gpt-3.5-turbo-1106", temperature=0.2):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model=model_name, temperature=temperature)
        cwd = os.getcwd()
        try:
            self.vectordb = self.check_vector_store(
                os.path.join(cwd, "vectorstore/chroma/")
            )
        except FileNotFoundError as e:
            logging.error(e)
            sys.exit(1)

    def check_vector_store(self, path):
        """Check if the vector store exists at the given path and return a Chroma instance or raise an exception."""
        if not os.path.exists(path):
            raise FileNotFoundError(
                "Vector store not found. Please ensure the directory exists or provide a valid path. Path:",
                path,
            )
        return Chroma(
            persist_directory=path,
            embedding_function=self.initialize_embedding(openai.api_key),
        )

    def initialize_embedding(self, api_key):
        """Initialize OpenAI embeddings with the provided API key."""
        openai.api_key = api_key
        return OpenAIEmbeddings()

    # this is, as literal as possible, a translation of Guillame's work
    # in the jupyter notebook
    def run_qa_chain(self, question):
        """Run the QA chain to process and respond to a specific question."""
        # Build prompt
        template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say 'thanks for asking!' at the end of the answer. 
        {context}
        Question: {question}
        Helpful Answer:"""
        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        # Run chain
        # RetrievalQA.from_chain_type is deprecated
        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=self.vectordb.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        )
        result = qa_chain.invoke({"query": question})
        return result["result"]
    

    # this augments Guillame's work to take in a message history and
    # return a response as a stream
    async def get_qa_chain_stream(self, messages):
        
        if len(messages) == 0:
            return
        
        last_message = messages[-1]
        chat_history = []

        if len(messages) > 1:
            chat_history = messages[:-1]

        retriever = self.vectordb.as_retriever()

        # TODO: this is returning much more than 3 sentences.
        system_prompt = (
            "Use the given context to answer the question. "
            "If you don't know the answer, say you don't know. "
            "Use three sentence maximum and keep the answer concise. "
            # "Context: {context}"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
            ]
        )

        # in place of the deprecated RetrievalQA.from_chain_type
        # https://python.langchain.com/v0.1/docs/modules/chains/
        context_docs_chain = create_history_aware_retriever(self.llm, retriever, prompt)

        docs = context_docs_chain.invoke({"chat_history": chat_history, "input": last_message["content"]})

        final_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", f'{last_message["content"]} {{context}}'),
            ]
        )        

        final_chain = create_stuff_documents_chain(self.llm, final_prompt)

        stream = final_chain.astream({"context": docs})

        # print('stream', stream)
        async for chunk in stream:
          # print('chunk', chunk)
          yield chunk

        # TODO: return 'docs' (above) also to the client as metadata
        # await stream.aclose()