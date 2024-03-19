from typing import Literal, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from typing_extensions import Annotated

from db.models import Extractor, get_session
from extraction.parsing import parse_binary_input
from server.extraction_runnable import ExtractResponse, extract_entire_document
from server.models import DEFAULT_MODEL
from server.retrieval import extract_from_content

router = APIRouter(
    prefix="/extract",
    tags=["extract"],
    responses={404: {"description": "Not found"}},
)


@router.post("", response_model=ExtractResponse)
async def extract_using_existing_extractor(
    *,
    extractor_id: Annotated[UUID, Form()],
    text: Optional[str] = Form(None),
    mode: Literal["entire_document", "retrieval"] = Form("entire_document"),
    file: Optional[UploadFile] = File(None),
    model_name: Optional[str] = Form(DEFAULT_MODEL),
    session: Session = Depends(get_session),
) -> ExtractResponse:
    """Endpoint that is used with an existing extractor.

    This endpoint will be expanded to support upload of binary files as well as
    text files.
    """
    if text is None and file is None:
        raise HTTPException(status_code=422, detail="No text or file provided.")

    extractor = session.query(Extractor).filter(Extractor.uuid == extractor_id).scalar()
    if extractor is None:
        raise HTTPException(status_code=404, detail="Extractor not found.")

    if text:
        text_ = text
    else:
        documents = parse_binary_input(file.file)
        # TODO: Add metadata like location from original file where
        # the text was extracted from
        text_ = "\n".join([document.page_content for document in documents])

    if mode == "entire_document":
        return await extract_entire_document(text_, extractor, model_name)
    elif mode == "retrieval":
        return await extract_from_content(text_, extractor, model_name)
    else:
        raise ValueError(
            f"Invalid mode {mode}. Expected one of 'entire_document', 'retrieval'."
        )
