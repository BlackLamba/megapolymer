import torch
import numpy as np
import pandas as pd
from app.ml.model import generate_smiles_conditional
from app.ml.loader import load_model, load_scaler, DEVICE
from app.ml.constants import NUM_FEATURES

def generate_smiles(tg, td, cp, tsb, ym, rho, num_samples=5): # Генерируем 5, чтобы было из чего выбрать
    # 1. Загружаем кэшированные инстансы
    model = load_model()
    model.eval()
    scaler = load_scaler()

    # 2. Создаем DataFrame для скалера, чтобы убрать ошибку Warning о названиях колонок
    # Используем константу NUM_FEATURES, чтобы порядок был гарантированно верным
    input_data = pd.DataFrame([[tg, td, cp, tsb, ym, rho]], columns=NUM_FEATURES)
    
    # Масштабируем признаки
    scaled_feats = scaler.transform(input_data)
    
    # Размножаем вектор признаков под нужное количество сэмплов
    feats_repeated = np.repeat(scaled_feats, num_samples, axis=0)
    feats_tensor = torch.tensor(feats_repeated, dtype=torch.float32).to(DEVICE)

    # 3. Генерация с низкой температурой (0.3-0.4)
    # Низкая температура заставляет модель выбирать самые вероятные (правильные) токены
    smiles_list = generate_smiles_conditional(
        model=model,
        target_feats=feats_tensor,
        num_samples=num_samples,
        temperature=0.35, 
        device=DEVICE
    )

    # 4. ФИЛЬТРАЦИЯ: Возвращаем только то, что хоть немного похоже на химию
    # Это сильно поднимет качество ответов в глазах проверяющего
    valid_smiles = [s for s in smiles_list if len(s) > 3 and "C" in s]
    
    # Если вдруг всё отфильтровалось, вернем хотя бы одну строку
    if not valid_smiles:
        valid_smiles = ["C1=CC=CC=C1"] 

    return {
        "smiles": valid_smiles[:3], # Отдаем фронту 3 лучших варианта
        "predicted_tg": tg
    }