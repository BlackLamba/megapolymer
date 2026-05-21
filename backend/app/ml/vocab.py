from app.ml.constants import VOCAB_SPECIAL

# Хардкодим ровно тот список токенов, который зафиксирован в весах модели
tokens = [
    '<pad>', '<bos>', '<eos>', '<unk>', '#', '%', '(', ')', '*', '+', 
    '-', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
    '=', 'B', 'C', 'F', 'H', 'I', 'N', 'O', 'P', 'S', '[', '\\', 
    ']', 'c', 'i', 'l', 'n', 'o', 'r', 's'
]

token2idx = {t: i for i, t in enumerate(tokens)}
idx2token = {i: t for t, i in token2idx.items()}
vocab_size = len(tokens)