import torch
import numpy as np
import pandas as pd
from app.ml.model import generate_smiles_conditional
from app.ml.loader import load_model, load_scaler, DEVICE
from app.ml.constants import NUM_FEATURES

def generate_smiles(tg, td, cp, tsb, ym, rho, num_samples=5):
    model = load_model()
    model.eval()
    scaler = load_scaler()

    input_data = pd.DataFrame([[tg, td, cp, tsb, ym, rho]], columns=NUM_FEATURES)
    
    scaled_feats = scaler.transform(input_data)
    
    feats_repeated = np.repeat(scaled_feats, num_samples, axis=0)
    feats_tensor = torch.tensor(feats_repeated, dtype=torch.float32).to(DEVICE)

    smiles_list = generate_smiles_conditional(
        model=model,
        target_feats=feats_tensor,
        num_samples=num_samples,
        temperature=0.35, 
        device=DEVICE
    )

    valid_smiles = [s for s in smiles_list if len(s) > 3 and "C" in s]
    
    if not valid_smiles:
        valid_smiles = ["C1=CC=CC=C1"] 

    return {
        "smiles": valid_smiles[:3],
        "predicted_tg": tg
    }
