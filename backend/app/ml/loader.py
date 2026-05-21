import os
import torch
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from app.ml.model import ConditionalTransformerVAE
from app.ml.vocab import vocab_size
from app.ml.constants import EMB_DIM, LATENT_DIM, N_HEADS, FF_DIM, NUM_LAYERS, MAX_LEN, NUM_FEATURES

MODEL = None
SCALER = None
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_model():
    global MODEL
    if MODEL is not None:
        return MODEL

    model = ConditionalTransformerVAE(
        vocab_size=vocab_size,
        emb_dim=EMB_DIM,
        latent_dim=LATENT_DIM,
        num_heads=N_HEADS,
        ff_dim=FF_DIM,
        num_layers=NUM_LAYERS,
        max_len=MAX_LEN,
        feature_dim=len(NUM_FEATURES)
    )

    weights_path = os.path.join(BASE_DIR, "transformer_smiles_conditional.pth")
    if not os.path.exists(weights_path):
        raise FileNotFoundError(f"Файл весов модели не найден по пути: {weights_path}")

    # Загружаем сохраненный чекпоинт
    state = torch.load(weights_path, map_location=DEVICE)
    
    # Безопасно извлекаем веса, если файл оказался полным чекпоинтом обучения
    if isinstance(state, dict) and "model_state_dict" in state:
        model.load_state_dict(state["model_state_dict"])
    else:
        model.load_state_dict(state)
        
    model.to(DEVICE)
    model.eval()

    MODEL = model
    return MODEL

def load_scaler():
    """Фиттит MinMaxScaler на оригинальном датасете для корректного инференса"""
    global SCALER
    if SCALER is not None:
        return SCALER

    CSV_PATH = os.path.join(BASE_DIR, "polyOne_aa.csv")
    df = pd.read_csv(CSV_PATH).dropna(subset=["smiles"])
    
    scaler = MinMaxScaler()
    scaler.fit(df[NUM_FEATURES])
    
    SCALER = scaler
    return SCALER