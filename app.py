# backend/app.py

from fastapi import FastAPI, File, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from PyPDF2 import PdfReader
from sentence_transformers import SentenceTransformer
from faiss import IndexFlatL2
import numpy as np
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

texts = []
embeddings = []
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
index = IndexFlatL2(384)

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    reader = PdfReader(file.file)
    text = "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    chunks = [text[i:i+500] for i in range(0, len(text), 500)]
    emb = model.encode(chunks)
    index.add(np.array(emb).astype('float32'))
    texts.extend(chunks)
    return {"msg": "PDF uploaded and indexed"}

@app.post("/ask/")
async def ask_question(question: str = Form(...)):
    question_emb = model.encode([question])
    D, I = index.search(np.array(question_emb).astype('float32'), k=3)
    result = " ".join([texts[i] for i in I[0]])
    return {"answer": f"📘 Based on the docs: {result}"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)
