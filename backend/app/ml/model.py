import torch
from torch import nn
from app.ml.vocab import token2idx, idx2token
from app.ml.constants import MAX_LEN, LATENT_DIM, VOCAB_SPECIAL

class ConditionalTransformerVAE(nn.Module):
    def __init__(self, vocab_size, emb_dim, latent_dim, num_heads, ff_dim, num_layers, max_len, feature_dim):
        super().__init__()
        self.emb = nn.Embedding(vocab_size, emb_dim, padding_idx=token2idx['<pad>'])
        self.pos_emb = nn.Parameter(torch.randn(1, max_len, emb_dim))

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=emb_dim, nhead=num_heads, dim_feedforward=ff_dim, batch_first=True
        )
        self.encoder = nn.TransformerEncoder(encoder_layer, num_layers=num_layers)
        self.feat_encoder = nn.Linear(feature_dim, latent_dim)

        self.fc_mu = nn.Linear(emb_dim + latent_dim, latent_dim)
        self.fc_logvar = nn.Linear(emb_dim + latent_dim, latent_dim)

        decoder_layer = nn.TransformerDecoderLayer(
            d_model=emb_dim, nhead=num_heads, dim_feedforward=ff_dim, batch_first=True
        )
        self.decoder = nn.TransformerDecoder(decoder_layer, num_layers=num_layers)
        self.decoder_proj = nn.Linear(latent_dim + latent_dim, emb_dim)
        self.out = nn.Linear(emb_dim, vocab_size)

    def encode(self, src, feats):
        src_mask = (src == token2idx['<pad>'])
        src_emb = self.emb(src) + self.pos_emb[:, :src.size(1)]
        src_enc = self.encoder(src_emb, src_key_padding_mask=src_mask)
        
        cls_token = src_enc[:, 0, :]
        feats_emb = self.feat_encoder(feats)
        combined = torch.cat([cls_token, feats_emb], dim=1)
        return self.fc_mu(combined), self.fc_logvar(combined)

    def reparameterize(self, mu, logvar):
        logvar = torch.clamp(logvar, min=-4, max=4)
        std = torch.exp(0.5 * logvar)
        return mu + torch.randn_like(std) * std

    def decode(self, z, feats, tgt_inp):
        tgt_mask = (tgt_inp == token2idx['<pad>'])
        feat_emb = self.feat_encoder(feats)
        z_dec = self.decoder_proj(torch.cat([z, feat_emb], dim=1)).unsqueeze(1)
        tgt_emb = self.emb(tgt_inp) + self.pos_emb[:, :tgt_inp.size(1)]

        seq_mask = nn.Transformer.generate_square_subsequent_mask(tgt_inp.size(1)).to(z.device)
        out = self.decoder(tgt=tgt_emb, memory=z_dec, tgt_mask=seq_mask, tgt_key_padding_mask=tgt_mask)
        return self.out(out)

    def forward(self, src, feats, tgt_inp):
        mu, logvar = self.encode(src, feats)
        z = self.reparameterize(mu, logvar)
        return self.decode(z, feats, tgt_inp), mu, logvar


def generate_smiles_conditional(model, target_feats, num_samples=5, temperature=0.5, device="cpu"):
    model.eval()
    with torch.no_grad():
        z = torch.randn(num_samples, LATENT_DIM).to(device)
        target_feats = target_feats.to(device)
        
        feat_emb = model.feat_encoder(target_feats)
        z_dec = model.decoder_proj(torch.cat([z, feat_emb], dim=1)).unsqueeze(1)

        input_token = torch.tensor([token2idx['<bos>']] * num_samples).unsqueeze(1).to(device)
        sequences = input_token
        finished = torch.zeros(num_samples, dtype=torch.bool).to(device)

        for _ in range(MAX_LEN - 1):
                    emb = model.emb(sequences) + model.pos_emb[:, :sequences.size(1)]
                    tgt_mask = nn.Transformer.generate_square_subsequent_mask(sequences.size(1)).to(device)
                    
                    out = model.decoder(tgt=emb, memory=z_dec, tgt_mask=tgt_mask)
                    logits = model.out(out[:, -1]) / temperature
                    
                    probs = torch.softmax(logits, dim=-1)
                    
                    next_token = torch.multinomial(probs, num_samples=1).squeeze(1)
                    
                    
                    next_token[finished] = token2idx['<pad>']
                    finished = finished | (next_token == token2idx['<eos>'])
                    
                    sequences = torch.cat([sequences, next_token.unsqueeze(1)], dim=1)
                    if finished.all():
                        break

        smiles_list = []
        for seq in sequences:
            tokens_seq = [idx2token[i.item()] for i in seq]
            if '<eos>' in tokens_seq:
                tokens_seq = tokens_seq[:tokens_seq.index('<eos>')]
            
            smiles = ''.join([t for t in tokens_seq if t not in VOCAB_SPECIAL])
            smiles_list.append(smiles)
            
        return smiles_list