from functools import lru_cache
from typing import List
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/paraphrase-multilingual-mpnet-base-v2"

@lru_cache(maxsize=1)
def get_model() -> SentenceTransformer:
    # 최초 호출 시 모델을 다운로드/로딩
    return SentenceTransformer(MODEL_NAME)

def embed_texts(texts: List[str]) -> np.ndarray:
    model = get_model()
    # ndarray(float32), shape = (N, 384)
    vecs = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return vecs
