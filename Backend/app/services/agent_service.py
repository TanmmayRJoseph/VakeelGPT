import os
import uuid
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from app.utils.pdf_utils import generate_summary_pdf

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    google_api_key=GOOGLE_API_KEY
)

# Session state
session_store = {}

def initialize_vectorstore(pdf_path: str, session_id: str):
    loader = PyPDFLoader(pdf_path)
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.split_documents(pages)

    persist_dir = os.path.join("uploads", session_id)
    os.makedirs(persist_dir, exist_ok=True)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=GoogleGenerativeAIEmbeddings(model="models/embedding-001"),
        persist_directory=persist_dir,
        collection_name="pdf"
    )

    session_store[session_id] = {
        "vectorstore": vectorstore,
        "qa_history": [],
        "pdf_path": pdf_path
    }

def ask_question(session_id: str, question: str, mode: str):
    vectorstore = session_store[session_id]["vectorstore"]
    matches = vectorstore.similarity_search(query=question, k=1)
    matched_clause = matches[0].page_content if matches else "No relevant clause found."

    tone = "in simple layman's terms" if mode == "layman" else "in detailed legal language"
    system_msg = SystemMessage(content=f"You are a legal expert. Explain the clause {tone}.")
    human_msg = HumanMessage(content=f"Clause: {matched_clause}\nQuery: {question}")
    response = llm.invoke([system_msg, human_msg])
    explanation = response.content.strip()

    # Save to history
    session_store[session_id]["qa_history"].append({
        "question": question,
        "clause": matched_clause,
        "answer": explanation
    })

    return {
        "clause": matched_clause,
        "explanation": explanation
    }

def export_summary(session_id: str) -> str:
    qa_history = session_store[session_id]["qa_history"]
    out_path = os.path.join("summaries", f"{session_id}.pdf")
    return generate_summary_pdf(qa_history, out_path)
