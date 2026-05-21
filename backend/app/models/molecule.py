from sqlalchemy import Column, Integer, String, Boolean, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Molecule(Base):
    __tablename__ = "molecules"

    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, ForeignKey("experiments.id"))

    smiles = Column(String, nullable=False)
    valid = Column(Boolean, nullable=False, default=False)
    predicted_tg = Column(Float, nullable=True)

    experiment = relationship("Experiment", back_populates="molecules")