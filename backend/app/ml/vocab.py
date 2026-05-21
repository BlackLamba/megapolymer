import os
import pandas as pd
from app.ml.constants import VOCAB_SPECIAL

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "polyOne_aa.csv")

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"Не найден датасет для сборки словаря по пути: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)
df = df.dropna(subset=["smiles"])

def tokenize(smiles):
    return list(smiles)

all_tokens = set()
for s in df["smiles"]:
    all_tokens.update(tokenize(s))

tokens = VOCAB_SPECIAL + sorted(list(all_tokens))

token2idx = {t: i for i, t in enumerate(tokens)}
idx2token = {i: t for t, i in token2idx.items()}
vocab_size = len(token2idx)