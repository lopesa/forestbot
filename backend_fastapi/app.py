from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from services.gpt_passthrough import chain, send_message
import asyncio

import services.call_rag as call_rag


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TO DO: Replace with setting DI per fastapi best practice https://fastapi.tiangolo.com/advanced/settings/

# the following doesn't work any more for some reason
# load_dotenv()

# the pydantic way noted above seems like the best way
# a current hack until then is: https://pypi.org/project/poetry-dotenv-plugin/ 

class RequestBody(BaseModel):
    messages: list

# async def fake_video_streamer():
#     for i in range(10):
#         yield b"some fake video bytes"
#         await asyncio.sleep(0.5)


# @app.get("/")
# async def main():
#     return StreamingResponse(fake_video_streamer())
# def hello_world():
#     return "Hello, home!"


@app.post("/api/chat")
async def main(request: Request, body: RequestBody):
    parsed_request = await request.json()
    llm_version = parsed_request['llmVersion']

    if llm_version == "rag-v1":
        try:
            res = call_rag.ask(body.messages[-1]["content"])
        except Exception as e:
            print('error:', e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
        return res.content
    else:
        try:
            generator = send_message(body.messages)         
        except Exception:
            raise HTTPException(status_code=500, detail="Internal Server Error")
        return StreamingResponse(generator, media_type="text/event-stream")
