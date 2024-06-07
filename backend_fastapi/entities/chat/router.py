import json
from entities.chat.rag_service import RAGService
from fastapi import APIRouter, Depends, HTTPException
from pydantic_base import CamelMode
from fastapi.responses import StreamingResponse

router = APIRouter()

# TO DO: Replace with setting DI per fastapi best practice https://fastapi.tiangolo.com/advanced/settings/
# the pydantic way noted above seems like the best way
# a current hack until then is: https://pypi.org/project/poetry-dotenv-plugin/


class Message(CamelMode):
    role: str = "user"
    content: str


class RequestBody(CamelMode):
    # llm_version: str
    messages: list[Message]


@router.get("")
def hello_world():
    return "Hello, home!"


@router.post("")
async def main(
    body: RequestBody,
    rag_service: RAGService = Depends(RAGService),
):
    messages = [msg.model_dump() for msg in body.messages]
    if len(messages) == 0:
        raise HTTPException(status_code=400, detail="No messages provided")
    try:
        docs = rag_service.get_augmentation_docs(messages)
        generator = rag_service.get_qa_chain_with_augmentation(messages, docs)

        # return metadata as headers, put it together on client
        docs_dict = [
            {"page_content": doc.page_content, "metadata": doc.metadata} for doc in docs
        ]

        return StreamingResponse(
            generator,
            media_type="text/event-stream",
            headers={"docs": json.dumps(docs_dict)},
        )

        # initial version
        # return rag_service.run_qa_chain(body.messages[-1].content)

        # initial version of streaming
        # generator = rag_service.get_qa_chain_stream(messages)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
