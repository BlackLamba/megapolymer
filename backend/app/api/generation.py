from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from typing import List

from app.db.deps import get_db, get_current_user
from app.services.generation_service import generate_polymer_smiles
from app.models.experiment import Experiment
from app.models.molecule import Molecule

router = APIRouter(prefix="/generation", tags=["Generation"])

class GenerateRequest(BaseModel):
    tg: float = Field(..., description="Glass Transition Temperature (Tg)")
    td: float = Field(..., description="Thermal Decomposition Temperature (Td)")
    cp: float = Field(..., description="Specific Heat Capacity (Cp)")
    tsb: float = Field(..., description="Tensile Strength at break (TSb)")
    ym: float = Field(..., description="Youngs Modulus (YM)")
    rho: float = Field(..., description="Density (rho)")
    num_samples: int = Field(5, ge=1, le=20, description="Количество генерируемых молекул")

@router.post("/generate")
def generate(
    data: GenerateRequest,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # 1. Создаем эксперимент в статусе processing
    # ПРИМЕЧАНИЕ: Не забудь добавить эти колонки в свою SQLAlchemy модель Experiment!
    experiment = Experiment(
        user_id=user_id,  
        tg=data.tg,
        td=data.td,
        cp=data.cp,
        tsb=data.tsb,
        ym=data.ym,
        rho=data.rho,
        status="processing"
    )

    db.add(experiment)
    db.commit()
    db.refresh(experiment)

    try:
        # 2. Запускаем реальный генератор (возвращает список словарей молекул)
        results = generate_polymer_smiles(
            tg=data.tg, td=data.td, cp=data.cp, 
            tsb=data.tsb, ym=data.ym, rho=data.rho, 
            num_samples=data.num_samples
        )

        # 3. Сохраняем все сгенерированные молекулы в БД (связка один-ко-многим)
        db_molecules = []
        for res in results:
            mol = Molecule(
                experiment_id=experiment.id,
                smiles=res["smiles"],
                valid=res["valid"],
                predicted_tg=res["predicted_tg"],
            )
            db.add(mol)
            db_molecules.append(res)

        # 4. Переводим статус в done
        experiment.status = "done"
        db.commit()

        return {
            "experiment_id": experiment.id,
            "status": "done",
            "count": len(db_molecules),
            "results": db_molecules
        }

    except Exception as e:
        # Если нейросеть упала (например, OOM или ошибка весов) — не оставляем эксперимент в "processing" зависшим
        experiment.status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail=f"Ошибка генерации модели: {str(e)}"
        )