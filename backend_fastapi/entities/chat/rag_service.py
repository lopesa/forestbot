import os
import sys
from typing import Any
import openai
import logging

# Importing necessary modules and classes from langchain
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA, create_retrieval_chain, create_history_aware_retriever
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.callbacks.base import AsyncCallbackHandler, BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.runnables import RunnablePassthrough, RunnableParallel
import time

# Setup logging
logging.basicConfig(level=logging.ERROR)

class MyCustomAsyncHandler(AsyncCallbackHandler):
    async def on_llm_new_token(self, token: str, **kwargs: Any) -> Any:
        print("New token received:", token)
        yield token

    async def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        print("LLM response:", response)


class RAGService:
    def __init__(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, verbose=True, streaming=True, callbacks=[MyCustomAsyncHandler()])
        # self.parser = StrOutputParser()
        # self.parser = JsonOutputParser()
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

    def run_qa_chain(self, question):
        """Run the QA chain to process and respond to a specific question."""
        # Build prompt
        template = """Use the following pieces of context to answer the question at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer. Use three sentences maximum. Keep the answer as concise as possible. Always say 'thanks for asking!' at the end of the answer. 
        {context}
        Question: {question}
        Helpful Answer:"""
        QA_CHAIN_PROMPT = PromptTemplate.from_template(template)

        # Run chain
        qa_chain = RetrievalQA.from_chain_type(
            self.llm,
            retriever=self.vectordb.as_retriever(),
            return_source_documents=True,
            chain_type_kwargs={"prompt": QA_CHAIN_PROMPT},
        )
        result = qa_chain.invoke({"query": question})
        return result["result"]
    
    async def get_qa_chain_stream(self, messages):
        print('messages', messages)
        if len(messages) == 0:
            return
        
        last_message = messages[-1]
        chat_history = []

        if len(messages) > 1:
            chat_history = messages[:-1]

    # from here: https://python.langchain.com/v0.1/docs/expression_language/primitives/passthrough/
        retriever = self.vectordb.as_retriever()

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



        # retrieval_chain = RetrievalQA.from_chain_type(
        #     self.llm,
        #     retriever=self.vectordb.as_retriever(),
        #     return_source_documents=True,
        #     chain_type_kwargs={"prompt": prompt},
        # )

        # retrieval_chain = (
        #     # {"context": retriever, "messages": RunnablePassthrough()}
        #     # RunnablePassthrough.assign()
        #     prompt
        #     | self.llm
        #     | StrOutputParser()
        #     # | JsonOutputParser()
        # )

        context_docs_chain = create_history_aware_retriever(self.llm, retriever, prompt)

        # stream = retrieval_chain.astream({"chat_history": chat_history, "input": last_message["content"]})
        docs = context_docs_chain.invoke({"chat_history": chat_history, "input": last_message["content"]})

        final_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", f'{last_message["content"]} {{context}}'),
            ]
        )
            

        final_chain = create_stuff_documents_chain(self.llm, final_prompt)

        stream = final_chain.astream({"context": docs})



        print('stream', stream)
        async for chunk in stream:
          print('chunk', chunk)
          yield chunk
        await stream.aclose()

        # retrieval_chain_with_source = RunnableParallel(
        #     {"context": retriever, "messages": RunnablePassthrough()}
        # ).assign(answer=retrieval_chain)

        # for chunk in retrieval_chain_with_source.stream(messages):
        #     print('chunk', chunk)

        # try:
        #   # test = retrieval_chain_with_source.invoke({"messages": messages})
        #   test = retrieval_chain.invoke({"messages": messages})

        # except Exception as e:
        #     print('error', e)

        # async for chunk in retrieval_chain_with_source.astream({"messages": messages}):
        #     print(chunk)
        #     yield chunk
        

        # stream = retrieval_chain.astream({"messages": messages})

        # async for chunk in stream:
        #   print('chunk', chunk)
        #   yield chunk
        # await time.sleep(3)


    # async def get_qa_chain_stream(self, messages):
    #     # print ('messages', messages)
    #     # form here: https://api.python.langchain.com/en/latest/chains/langchain.chains.retrieval_qa.base.RetrievalQA.html

    #     system_prompt = (
    #         "Use the given context to answer the question. "
    #         "If you don't know the answer, say you don't know. "
    #         "Use three sentence maximum and keep the answer concise. "
    #         "Context: {context}"
    #     )

    #     prompt = ChatPromptTemplate.from_messages(
    #         [
    #             ("system", system_prompt),
    #             MessagesPlaceholder(variable_name="messages"),
    #             # ("human", "{input}"),
    #         ]
    #     )

    #     question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
        
    #     chain = create_retrieval_chain(self.vectordb.as_retriever(), question_answer_chain)

    #     stream = chain.abatch({"messages": messages})
    #     # print('stream', stream)
    #     # # return stream
    #     # # print('stream', stream)
    #     async for chunk in stream:
    #       print('chunk', chunk)
    #       yield chunk
    #     await stream.aclose()


    #     # return chain.astream({"messages": messages})


# Usage example
if __name__ == "__main__":
    rag_service = RAGService()
    question = "What is the difference between OFAC and COMIFAC?"
    result = rag_service.run_qa_chain(question)
    print(result)
