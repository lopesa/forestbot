from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import BaseMessage
from langchain_core.output_parsers import StrOutputParser


class GPTPassthroughService:
    def __init__(self, model_name="gpt-3.5-turbo-1106", temperature=0.2):
        self.chat = ChatOpenAI(model=model_name, temperature=temperature)
        self.parser = StrOutputParser()
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a helpful assistant. Answer all questions to the best of your ability.",
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        self.chain = self.prompt | self.chat | self.parser

    async def get_res_stream(self, messages):
        stream = self.chain.astream({"messages": messages})
        print('stream', stream)
        async for chunk in stream:
          print('chunk', chunk)
          yield chunk
        await stream.aclose()
