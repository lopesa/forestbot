from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from services.gpt_passthrough import chain

import services.call_rag as call_rag


app = FastAPI()

# TO DO: Replace with setting DI per fastapi best practice https://fastapi.tiangolo.com/advanced/settings/

# the following doesn't work any more for some reason
# load_dotenv()

# the pydantic way noted above seems like the best way
# a current hack until then is: https://pypi.org/project/poetry-dotenv-plugin/ 

class RequestBody(BaseModel):
    messages: list


@app.get("/")
def hello_world():
    return "Hello, home!"


@app.post("/api/chat")
async def main(request: Request, body: RequestBody):
    # gpt_passthrough = chain.invoke({"messages": body.messages})
    rag_response = call_rag.ask(body.messages[-1]["content"])
    try:
        # res = gpt_passthrough.content
        res = rag_response
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    return res
