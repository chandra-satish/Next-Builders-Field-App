import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from app.services.search_service import SearchService
# Get HF_TOKEN
# hf_token = os.getenv("HF_TOKEN")

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Enable CORS - allow local dev and production URL from env
origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Resolve path to documents.json
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'documents.json')

# Load documents and model at startup
with open(DATA_PATH, 'r') as f:
    documents = json.load(f)

print("Loading embedding model...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize Search Service
search_service = SearchService(documents, model)
# search_service = SearchService(documents, hf_token)
@app.get("/")
async def root():
    return {"message": "Next Construction Solutions API is running"}

@app.get("/search")
async def search(q: str = Query(..., min_length=1)):
    return search_service.hybrid_search(q)

if __name__ == "__main__":
    import uvicorn
    # Use PORT from environment variable (required for deployment)
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
