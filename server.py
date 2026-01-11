from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles 
from pydantic import BaseModel
import os

import content_generator
import document_generator

app = FastAPI()

# Enable CORS (Still good to have)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class RequestBody(BaseModel):
    text: str

# --- API ROUTES ---
@app.post("/generate")
async def generate_document(payload: RequestBody):
    # (Keep your existing logic here)
    print(f"Received Request: {payload.text[:30]}...")
    data = content_generator.generate_report_content(payload.text)
    if not data: raise HTTPException(status_code=500, detail="AI Generation Failed")
    
    try: document_generator.generate_pdf()
    except Exception as e: raise HTTPException(status_code=500, detail=f"PDF Failed: {str(e)}")
    
    pdf_path = os.path.join("output", "strategic_report.pdf")
    return FileResponse(pdf_path, media_type="application/pdf", filename="report.pdf")

# --- SERVE REACT FRONTEND (THE MAGIC PART) ---
# 1. Mount the "static" folder (CSS/JS)
app.mount("/static", StaticFiles(directory="client/build/static"), name="static")

# 2. Catch-all route to serve React's index.html
@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    # If the file exists in build (like favicon.ico), serve it
    file_path = os.path.join("client/build", full_path)
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return FileResponse(file_path)
    
    # Otherwise, return the main React HTML file
    return FileResponse("client/build/index.html")