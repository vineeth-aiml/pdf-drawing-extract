from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.sql import func
from app.db.session import Base

class Document(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String, default="uploaded")  # uploaded|processing|done|failed
    pipeline = Column(String, default="final")
    error = Column(Text, nullable=True)

class ExtractionResult(Base):
    __tablename__ = "results"
    doc_id = Column(String, primary_key=True, index=True)
    json_path = Column(String, nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
