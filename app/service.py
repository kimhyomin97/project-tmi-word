import numpy as np

# 임계치는 초기값. 이후 운영 데이터로 조정
THRESHOLD_CORRECT = 0.80
THRESHOLD_PARTIAL = 0.65

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    # a, b는 L2 정규화된 벡터라고 가정(encode 시 normalize=True)
    return float(np.dot(a, b))

def judge_similarity(sim: float) -> str:
    if sim >= THRESHOLD_CORRECT:
        return "맞음"
    if sim >= THRESHOLD_PARTIAL:
        return "부분적"
    return "아님"
