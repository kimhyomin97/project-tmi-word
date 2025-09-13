from pydantic import BaseModel, Field

class HealthResp(BaseModel):
    status: str = "ok"

class EmbedReq(BaseModel):
    text: str = Field(..., min_length=1)

class EmbedResp(BaseModel):
    dim: int
    # 디버깅용: 앞의 몇 개 값만 노출
    head: list[float]

class JudgeReq(BaseModel):
    en: str = Field(..., min_length=1)
    ko: str = Field(..., min_length=1)

class JudgeResp(BaseModel):
    similarity: float
    label: str

class JudgeDetailedReq(BaseModel):
    en: str = Field(..., min_length=1)
    ko: str = Field(..., min_length=1)

class JudgeDetailedResp(BaseModel):
    overall_similarity: float
    overall_label: str
    word_similarities: list[dict]