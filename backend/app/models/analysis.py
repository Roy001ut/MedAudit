from sqlalchemy import Column, String, Text, Numeric, Integer, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid
from app.database.base import Base

class DrugAnalysis(Base):
    __tablename__ = "drug_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    drug_name = Column(String(255), nullable=False)
    dosage = Column(String(100))
    what_is_it = Column(Text, default="")
    treats = Column(JSONB, default=[])
    side_effects = Column(JSONB, default=[])
    red_flags = Column(JSONB, default=[])
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class BillAnalysis(Base):
    __tablename__ = "bill_analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    document_id = Column(UUID(as_uuid=True), ForeignKey("documents.id"), nullable=True)
    charges = Column(JSONB, default=[])
    red_flags = Column(JSONB, default=[])
    fraud_risk_score = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class LabReport(Base):
    __tablename__ = "lab_reports"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    test_name = Column(String(255), nullable=False, index=True)
    test_value = Column(Numeric(10, 2))
    unit = Column(String(50))
    normal_range_min = Column(Numeric(10, 2))
    normal_range_max = Column(Numeric(10, 2))
    status = Column(String(50), default="normal")
    test_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
