import torch
import numpy as np
from app.ml.model import generate_smiles_conditional
from app.ml.loader import load_model, load_scaler, DEVICE

def generate_smiles(tg, td, cp, tsb, ym, rho, num_samples=1):
    # Загружаем кэшированные инстансы модели и скалера
    model = load_model()
    scaler = load_scaler()

    # 1. Собираем массив строго в том порядке, в котором обучался MinMaxScaler
    raw_feats = np.array([[tg, td, cp, tsb, ym, rho]], dtype=np.float32)
    
    # 2. Нормализуем данные (важнейший шаг!)
    scaled_feats = scaler.transform(raw_feats)
    
    # Сразу размножаем вектор признаков под количество сэмплов (num_samples)
    feats_repeated = np.repeat(scaled_feats, num_samples, axis=0)
    feats_tensor = torch.tensor(feats_repeated, dtype=torch.float32).to(DEVICE)

    # 3. Генерация последовательностей SMILES
    smiles_list = generate_smiles_conditional(
        model=model,
        target_feats=feats_tensor,
        num_samples=num_samples,
        temperature=0.8,
        device=DEVICE
    )

    # Возвращаем список сгенерированных молекул
    return {
        "smiles": smiles_list,
        "predicted_tg": tg
    }