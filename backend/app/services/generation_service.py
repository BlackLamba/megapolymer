from rdkit import Chem
from app.ml.inference import generate_smiles as ml_generate_smiles

def check_smiles_validity(smiles: str) -> bool:
    """Проверяет, является ли строка SMILES химически валидной"""
    if not smiles:
        return False
    try:
        mol = Chem.MolFromSmiles(smiles)
        return mol is not None
    except Exception:
        return False

def generate_polymer_smiles(
    tg: float, 
    td: float, 
    cp: float, 
    tsb: float, 
    ym: float, 
    rho: float, 
    num_samples: int = 1
):
    # Вызываем тяжелый ML-инференс
    ml_result = ml_generate_smiles(
        tg=tg, td=td, cp=cp, tsb=tsb, ym=ym, rho=rho, 
        num_samples=num_samples
    )
    
    # Собираем результаты с валидацией через RDKit
    generated_molecules = []
    for smiles_str in ml_result["smiles"]:
        is_valid = check_smiles_validity(smiles_str)
        generated_molecules.append({
            "smiles": smiles_str,
            "valid": is_valid,
            "predicted_tg": ml_result["predicted_tg"]  # Или твоя кастомная логика оценки
        })
        
    return generated_molecules