from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import FileResponse
import os, uuid, shutil
from fastapi import HTTPException
from app.services.agent_service import initialize_vectorstore, ask_question, export_summary
from app.schemas import QuestionRequest, QuestionResponse, PDFResponse

router = APIRouter()

@router.post("/upload")
def upload_pdf(file: UploadFile = File(...)):
    session_id = str(uuid.uuid4())
    os.makedirs("uploads", exist_ok=True)
    save_path = os.path.join("uploads", f"{session_id}.pdf")

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    initialize_vectorstore(save_path, session_id)
    return {"session_id": session_id, "message": "PDF uploaded and processed."}

@router.post("/ask/", response_model=QuestionResponse)
def ask(request: QuestionRequest):
    session_id = request.session_id
    if session_id not in os.listdir("uploads"):
        raise HTTPException(status_code=400, detail="Invalid session ID. Please upload a PDF first.")

    response = ask_question(session_id, request.question, request.mode)
    return QuestionResponse(
        answer=response['explanation'],
        clause=response['clause'],
        explanation=response['explanation']
    )

@router.get("/download-summary/", response_model=PDFResponse)
def download(session_id: str):
    pdf_path = export_summary(session_id)
    return PDFResponse(download_link=f"/summaries/{session_id}.pdf")

@router.get("/summaries/{filename}")
def serve_pdf(filename: str):
    file_path = os.path.join("summaries", filename)
    return FileResponse(file_path, media_type='application/pdf', filename=filename)
