from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.document import Document, DocumentType
from app.services.document_service import DocumentService
from app.dependencies import get_current_user_id

router = APIRouter()

@router.post("/upload/{doc_type}", status_code=status.HTTP_201_CREATED)
async def upload(doc_type: str, file: UploadFile = File(...), user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        dt = DocumentType[doc_type.upper()]
    except KeyError:
        raise HTTPException(status_code=400, detail=f"Invalid type: {doc_type}")

    try:
        fpath = await DocumentService.save_file(file, user_id)
        text = await DocumentService.extract_text(fpath, file.content_type)

        doc = Document(user_id=user_id, document_type=dt, original_filename=file.filename, file_path=fpath, raw_text=text)
        db.add(doc)
        db.commit()
        db.refresh(doc)

        return {"id": str(doc.id), "filename": file.filename, "status": "uploaded"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def list_docs(user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    docs = db.query(Document).filter(Document.user_id == user_id).all()
    return [{"id": str(d.id), "filename": d.original_filename, "type": d.document_type.value} for d in docs]
