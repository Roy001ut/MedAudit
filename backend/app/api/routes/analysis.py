from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database.session import get_db
from app.models.document import Document
from app.models.analysis import DrugAnalysis, BillAnalysis
from app.services.drug_service import DrugService
from app.services.bill_service import BillService
from app.dependencies import get_current_user_id

router = APIRouter()

class DrugRequest(BaseModel):
    drug_name: str
    dosage: str

class BillRequest(BaseModel):
    document_id: str
    patient_diagnosis: str = None

@router.post("/drug")
async def analyze_drug(req: DrugRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    try:
        result = DrugService.analyze_drug(req.drug_name, req.dosage)

        da = DrugAnalysis(user_id=user_id, drug_name=req.drug_name, dosage=req.dosage, what_is_it=result.get("what_is_it", ""), treats=result.get("treats", []), side_effects=result.get("side_effects", []), red_flags=result.get("red_flags", []))
        db.add(da)
        db.commit()

        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/bill")
async def analyze_bill(req: BillRequest, user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)):
    doc = db.query(Document).filter(Document.id == req.document_id, Document.user_id == user_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    try:
        result = BillService.analyze_bill(doc.raw_text, req.patient_diagnosis)

        ba = BillAnalysis(user_id=user_id, document_id=req.document_id, charges=result.get("charges", []), red_flags=result.get("red_flags", []), fraud_risk_score=result.get("fraud_risk_score", 0))
        db.add(ba)
        db.commit()

        return result
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
