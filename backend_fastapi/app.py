from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
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
    parsed_request = await request.json()
    llm_version = parsed_request['llmVersion']

    try:
        res = call_rag.ask(body.messages[-1]["content"]) if llm_version == "rag-v1" else chain.invoke({"messages": body.messages}) 
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return res.content if llm_version == "gpt-passthrough" else res
