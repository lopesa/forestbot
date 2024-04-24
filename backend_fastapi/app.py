from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# TO DO: Replace with setting DI per fastapi best practice https://fastapi.tiangolo.com/advanced/settings/
load_dotenv()

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

app = FastAPI()


class RequestBody(BaseModel):
    messages: list


@app.get("/")
def hello_world():
    return "Hello, home!"


@app.post("/api/chat")
async def main(request: Request, body: RequestBody):
    test = chain.invoke({"messages": body.messages})
    try:
        res = test.content
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return res
