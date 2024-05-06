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
# async def main(request: Request):
    # return StreamingResponse(fake_video_streamer(), media_type='text/event-stream')
    
    # parsed_request = await request.json()
    # llm_version = parsed_request['llmVersion']

    generator = send_message(body.messages[-1]['content'])
    # generator = send_message(body.messages)
    return StreamingResponse(generator, media_type="text/event-stream")

    # if llm_version == "rag-v1":
    #     try:
    #         res = call_rag.ask(body.messages[-1]["content"])
    #     except Exception:
    #         raise HTTPException(status_code=500, detail="Internal Server Error")
    #     return res.content
    # else:
    #     return StreamingResponse(send_message(body.messages[0]['content']), media_type="text/event-stream")
        # try:
        #     print("body.messages", body.messages[0]['content'])
        #     # generator = send_message(body.messages)
        #     # generator = send_message(body.messages[0]['content'])
        #     # res = chain.invoke({"messages": body.messages})
        #     # return StreamingResponse(generator, media_type="text/event-stream")
        #     return StreamingResponse(send_message(body.messages[0]['content']), media_type="text/event-stream")
        # except Exception:
        #     raise HTTPException(status_code=500, detail="Internal Server Error")


# async def main(request: Request, body: RequestBody):
#     parsed_request = await request.json()
#     llm_version = parsed_request['llmVersion']

#     try:
#         res = call_rag.ask(body.messages[-1]["content"]) if llm_version == "rag-v1" else chain.invoke({"messages": body.messages}) 
#     except Exception:
#         raise HTTPException(status_code=500, detail="Internal Server Error")
    
#     return res.content if llm_version == "gpt-passthrough" else res
