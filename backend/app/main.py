from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from app.config import settings
from app.database.session import engine
from app.models import user, document, analysis
from app.api.routes import auth, documents, analysis

# Create tables
user.User.metadata.create_all(bind=engine)
document.Document.metadata.create_all(bind=engine)
analysis.DrugAnalysis.metadata.create_all(bind=engine)
analysis.BillAnalysis.metadata.create_all(bind=engine)
analysis.LabReport.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="MedAudit API", version="1.0.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/api/auth")
app.include_router(documents.router, prefix="/api/documents")
app.include_router(analysis.router, prefix="/api/analysis")
