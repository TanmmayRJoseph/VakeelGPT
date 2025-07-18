import os
from fpdf import FPDF
from typing import TypedDict
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_core.messages import HumanMessage, SystemMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found!")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.5,
    google_api_key=GOOGLE_API_KEY
)


# Define Agent State
class AgentState(TypedDict):
    pdf_path: str
    pdf_text: list
    user_query: str
    matched_clause: str
    explanation_mode: str
    final_explanation: str
    qa_history: list  # NEW


# Embeddings & VectorStore setup
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
pdf_path = "Separation Agreement.pdf"
persist_directory = r"C:\Users\Tanmmay R Joseph\OneDrive\Desktop\VakeelGPT\Backend"
collection_name = "pdf"

pdf_loader = PyPDFLoader(pdf_path)
pages = pdf_loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
pages_split = text_splitter.split_documents(pages)

if not os.path.exists(persist_directory):
    os.makedirs(persist_directory)

vectorstore = Chroma.from_documents(
    documents=pages_split,
    embedding=embeddings,
    persist_directory=persist_directory,
    collection_name=collection_name
)


# ---------- Node Functions ----------

def load_pdf_node(state: AgentState) -> AgentState:
    loader = PyPDFLoader(state["pdf_path"])
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    state["pdf_text"] = splitter.split_documents(pages)
    return state


def get_user_query_node(state: AgentState) -> AgentState:
    query = input("\n📩 Enter your legal question: ")
    state["user_query"] = query
    return state


def retrieve_clause_node(state: AgentState) -> AgentState:
    matches = vectorstore.similarity_search(query=state["user_query"], k=1)
    state["matched_clause"] = matches[0].page_content if matches else "No relevant clause found."
    return state


def explain_clause_node(state: AgentState) -> AgentState:
    prompt = f"""You're a legal assistant. Explain the following clause from a separation agreement in a simple and clear way:

Clause: {state['matched_clause']}

User's Question: {state['user_query']}

Explanation:"""
    response = llm.invoke(prompt)
    state["final_explanation"] = response.content.strip()
    return state


def get_user_choice_node(state: AgentState) -> AgentState:
    choice = input("🧠 Do you want a 'layman' explanation or a 'lawyer' explanation? ").strip().lower()
    if choice not in ["layman", "lawyer"]:
        print("Invalid choice. Defaulting to layman.")
        choice = "layman"
    state["explanation_mode"] = choice
    return state


def reformat_explanation_node(state: AgentState) -> AgentState:
    tone = "in simple layman's terms" if state["explanation_mode"] == "layman" else "in detailed legal language"
    system_message = SystemMessage(
        content=f"You are a legal expert. Explain the clause {tone}."
    )
    human_message = HumanMessage(
        content=f"Clause: {state['matched_clause']}\nQuery: {state['user_query']}"
    )
    response = llm.invoke([system_message, human_message])
    explanation = response.content.strip()
    state["final_explanation"] = explanation

    # Print explanation
    print("\n📜 Final Explanation:\n")
    print(explanation)
    return state


def export_full_summary_pdf(state: AgentState) -> AgentState:
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.set_auto_page_break(auto=True, margin=15)

        pdf.multi_cell(0, 10, "Legal Clause Q&A Summary\n\n")

        for idx, qa in enumerate(state["qa_history"], 1):
            q = f"\nQ{idx}: {qa['question']}"
            clause = f"Matched Clause:\n{qa['clause']}"
            ans = f"Explanation:\n{qa['answer']}\n" + "-" * 80

            for content in [q, clause, ans]:
                pdf.multi_cell(0, 10, content.encode('latin-1', 'replace').decode('latin-1'))

        filename = "Full_Clause_Conversation_Summary.pdf"
        pdf.output(filename)
        print(f"\n✅ Final multi-Q PDF saved as: {filename}")
    except Exception as e:
        print(f"Error creating summary PDF: {e}")
    return state


# ---------- Run Multi-Q Loop Agent ----------

def run_agent_loop(state: AgentState) -> AgentState:
    # Step 1: Load PDF once
    state = load_pdf_node(state)

    while True:
        # One full Q&A interaction
        state = get_user_query_node(state)
        state = retrieve_clause_node(state)
        state = explain_clause_node(state)
        state = get_user_choice_node(state)
        state = reformat_explanation_node(state)

        # Save Q&A to history
        state["qa_history"].append({
            "question": state["user_query"],
            "clause": state["matched_clause"],
            "answer": state["final_explanation"]
        })

        # Ask for another question
        ask_more = input("\n Do you want to ask another question? (yes/no): ").strip().lower()
        if ask_more not in ["yes", "y"]:
            break

    # Export final summary PDF
    state = export_full_summary_pdf(state)
    return state


# ---------- Initial State ----------

initial_state: AgentState = {
    "pdf_path": pdf_path,
    "pdf_text": None,
    "user_query": None,
    "matched_clause": None,
    "explanation_mode": None,
    "final_explanation": None,
    "qa_history": []  # NEW
}

# Run the loop-based agent
run_agent_loop(initial_state)