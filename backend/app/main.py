import json
import os
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
from app.services.search_service import SearchService

app = FastAPI()

# Enable CORS for React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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

@app.get("/")
async def root():
    return {"message": "Next Construction Solutions API is running"}

@app.get("/search")
async def search(q: str = Query(..., min_length=1)):
    return search_service.hybrid_search(q)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
