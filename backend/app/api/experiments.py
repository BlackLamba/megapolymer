from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from collections import defaultdict

from app.db.deps import get_db, get_current_user
from app.models.experiment import Experiment
from app.models.molecule import Molecule

router = APIRouter()

@router.get("/experiments")
def get_experiments(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    # 1. Получаем все эксперименты пользователя
    experiments = (
        db.query(Experiment)
        .filter(Experiment.user_id == user_id)
        .all()
    )

    exp_ids = [e.id for e in experiments]

    # 2. Получаем ВСЕ молекулы для этих экспериментов
    molecules = (
        db.query(Molecule)
        .filter(Molecule.experiment_id.in_(exp_ids))
        .all()
    )

    # 3. Группируем молекулы в списки по experiment_id (чтобы не терять сэмплы)
    molecule_map = defaultdict(list)
    for m in molecules:
        molecule_map[m.experiment_id].append({
            "id": m.id,
            "smiles": m.smiles,
            "valid": m.valid,
            "predicted_tg": m.predicted_tg
        })

    result = []
    for exp in experiments:
        result.append({
            "id": exp.id,
            "status": exp.status,
            # Отдаем актуальные 6 признаков из базы
            "tg": exp.tg,
            "td": exp.td,
            "cp": exp.cp,
            "tsb": exp.tsb,
            "ym": exp.ym,
            "rho": exp.rho,
            # Отдаем массив всех сгенерированных молекул
            "molecules": molecule_map.get(exp.id, [])
        })

    return result

@router.get("/experiments/{id}")
def get_experiment(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    exp = (
        db.query(Experiment)
        .filter(
            Experiment.id == id,
            Experiment.user_id == user_id
        )
        .first()
    )

    if not exp:
        raise HTTPException(status_code=404, detail="Experiment not found")

    # Собираем все молекулы текущего эксперимента
    molecules = (
        db.query(Molecule)
        .filter(Molecule.experiment_id == id)
        .all()
    )

    return {
        "id": exp.id,
        "status": exp.status,
        # Актуальные 6 параметров структуры
        "tg": exp.tg,
        "td": exp.td,
        "cp": exp.cp,
        "tsb": exp.tsb,
        "ym": exp.ym,
        "rho": exp.rho,
        # Список результатов
        "molecules": [
            {
                "id": m.id,
                "smiles": m.smiles,
                "valid": m.valid,
                "predicted_tg": m.predicted_tg
            } for m in molecules
        ]
    }