import numpy as np
import re

# 다국어 모델의 현실적인 임계값 설정
# 영어-한국어 번역의 경우 0.6 이상이면 의미상 일치로 봄
THRESHOLD_CORRECT = 0.60
THRESHOLD_PARTIAL = 0.40

def cosine_sim(a: np.ndarray, b: np.ndarray) -> float:
    # a, b는 L2 정규화된 벡터라고 가정(encode 시 normalize=True)
    return float(np.dot(a, b))

def preprocess_text(text: str) -> str:
    """텍스트 전처리: 소문자 변환, 특수문자 제거"""
    # 소문자 변환
    text = text.lower()
    # 연속된 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    # 앞뒤 공백 제거
    return text.strip()

def judge_similarity(sim: float) -> str:
    if sim >= THRESHOLD_CORRECT:
        return "맞음"
    if sim >= THRESHOLD_PARTIAL:
        return "부분적"
    return "아님"
