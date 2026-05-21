from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class Experiment(Base):
    __tablename__ = "experiments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="processing")

    # Входные параметры для условной генерации (6 признаков из VAE)
    tg = Column(Float, nullable=False)   # Glass Transition Temperature
    td = Column(Float, nullable=False)   # Thermal Decomposition Temperature
    cp = Column(Float, nullable=False)   # Specific Heat Capacity
    tsb = Column(Float, nullable=False)  # Tensile Strength at break
    ym = Column(Float, nullable=False)   # Youngs Modulus
    rho = Column(Float, nullable=False)  # Density (вместо старого density / mw)

    user = relationship("User")
    molecules = relationship("Molecule", back_populates="experiment", cascade="all, delete-orphan")