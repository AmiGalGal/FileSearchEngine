#File purpose: turn text into vectors

from sentence_transformers import SentenceTransformer
from sentence_transformers import util
import torch

model = SentenceTransformer('all-MiniLM-L6-v2')

def embed(sentence):
    embeddings = model.encode(sentence)
    return embeddings

def similarity(query_emb, chunk_emb):
    query_emb = torch.tensor(query_emb, dtype=torch.float32)
    chunk_emb = torch.tensor(chunk_emb, dtype=torch.float32)
    score = util.cos_sim(query_emb, chunk_emb)
    return score
