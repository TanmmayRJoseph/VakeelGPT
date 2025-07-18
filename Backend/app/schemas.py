from typing import Optional
from pydantic import BaseModel

class QuestionRequest(BaseModel):
    question: str
    mode: Optional[str] = "layman"  # layman or lawyer
    session_id: str

class QuestionResponse(BaseModel):
    answer: str
    clause: str
    explanation: str

class PDFResponse(BaseModel):
    download_link: str
