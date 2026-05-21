from __future__ import annotations

import joblib
import numpy as np
import pandas as pd
from rdkit import Chem
from rdkit.Chem import rdFingerprintGenerator
from pathlib import Path
from typing import Dict, Optional, List

class PropertyPredictor:
    """Предсказывает свойства полимера по SMILES с помощью ансамбля LightGBM."""

    def __init__(self, model_path: Path):
        artifacts = joblib.load(model_path)
        self.models: Dict[str, object] = artifacts['models']          # param -> LGBMRegressor
        self.scaler = artifacts['scaler']
        self.property_cols: List[str] = artifacts['property_cols']
        self.feature_names: List[str] = artifacts.get(
            'feature_names', [f"fp_{i}" for i in range(1024)]
        )
        # Morgan fingerprint generator
        self.gen = rdFingerprintGenerator.GetMorganGenerator(radius=2, fpSize=1024)

    def predict(self, smiles: str) -> Optional[Dict[str, float]]:
        mol = Chem.MolFromSmiles(smiles)
        if mol is None:
            return None
        fp = np.array(self.gen.GetFingerprint(mol)).reshape(1, -1)
        fp_df = pd.DataFrame(fp, columns=self.feature_names)
        preds_scaled = [self.models[prop].predict(fp_df)[0] for prop in self.property_cols]
        preds_scaled = np.array(preds_scaled).reshape(1, -1)
        preds = self.scaler.inverse_transform(preds_scaled).flatten()
        return dict(zip(self.property_cols, preds))