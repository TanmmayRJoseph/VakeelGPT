from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import legal_agent

app = FastAPI(title="VakeelGPT API")
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",  # Sometimes needed too
]
@app.get("/")
def read_root():
    return {"message": "Welcome to VakeelGPT API. Use the /docs endpoint for API documentation."}


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Set your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(legal_agent.router)
