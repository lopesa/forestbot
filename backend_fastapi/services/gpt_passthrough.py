from typing import AsyncIterable, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain.callbacks.base import BaseCallbackHandler

from langchain.callbacks import AsyncIteratorCallbackHandler
import asyncio
from langchain.schema import HumanMessage, BaseMessage


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

chain = prompt | chat

# async def send_message(content: str) -> AsyncIterable[str]:
async def send_message(content: List[BaseMessage]) -> AsyncIterable[str]:
    print(f"Content: {content}")
    callback = AsyncIteratorCallbackHandler()
    model = ChatOpenAI(
        streaming=True,
        # max_tokens=10,
        verbose=True,
        callbacks=[callback],
    )

    task = asyncio.create_task(
        # chat.agenerate(messages=[[HumanMessage(content=content)]])
        # chain.invoke({"messages": content}) 
        # chain.agenerate({"messages": content})
        # model.agenerate(messages=[[HumanMessage(content=content)]])
        model.agenerate(messages=[[HumanMessage(content=content)]])
        # model.agenerate(messages=[[BaseMessage(content=[content])]])
        # chat.agenerate_prompt(prompts=[prompt], messages=content, callbacks=[callback])
    )

    # async for token in callback.aiter():
    #   print(f"Token: {token}")
    #   yield token    

    try:
        async for token in callback.aiter():
            print(f"Token: {token}")
            yield token
    except Exception as e:
        print(f"Caught exception: {e}")
    finally:
        callback.done.set()

    await task