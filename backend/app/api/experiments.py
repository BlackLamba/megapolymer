from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db, get_current_user
from app.models.experiment import Experiment
from app.models.molecule import Molecule

router = APIRouter()

@router.get("/experiments")
def get_experiments(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user)
):
    experiments = (
        db.query(Experiment)
        .filter(Experiment.user_id == user_id)
        .all()
    )

    exp_ids = [e.id for e in experiments]

    molecules = (
        db.query(Molecule)
        .filter(Molecule.experiment_id.in_(exp_ids))
        .all()
    )

    molecule_map = {m.experiment_id: m for m in molecules}

    result = []

    for exp in experiments:
        mol = molecule_map.get(exp.id)

        result.append({
            "id": exp.id,
            "tg": exp.tg,
            "mw": exp.mw,
            "density": exp.density,
            "status": exp.status,

            "smiles": mol.smiles if mol else None,
            "valid": mol.valid if mol else None,
            "predicted_tg": mol.predicted_tg if mol else None,
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

    mol = (
        db.query(Molecule)
        .filter(Molecule.experiment_id == id)
        .first()
    )

    return {
        "id": exp.id,
        "status": exp.status,
        "tg": exp.tg,
        "mw": exp.mw,
        "density": exp.density,

        "smiles": mol.smiles if mol else None,
        "valid": mol.valid if mol else None,
        "predicted_tg": mol.predicted_tg if mol else None,
    }