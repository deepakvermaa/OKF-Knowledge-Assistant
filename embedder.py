from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


def load_model():
    model = SentenceTransformer(EMBEDDING_MODEL)
    return model


def create_embedding(text, model):
    embedding = model.encode(text)
    return embedding