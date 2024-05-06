from typing import List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain.schema import BaseMessage
from langchain_core.output_parsers import StrOutputParser


chat = ChatOpenAI(model="gpt-3.5-turbo-1106", temperature=0.2)

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful assistant. Answer all questions to the best of your ability.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

parser = StrOutputParser()

chain = prompt | chat | parser

async def send_message(content: List[BaseMessage]):
  stream = chain.astream({"messages": content})
  async for chunk in stream:
    yield chunk
  await stream.aclose()