from fastapi import APIRouter
from .schema import HealthResp, EmbedReq, EmbedResp, JudgeReq, JudgeResp
from .model import embed_texts
from .service import cosine_sim, judge_similarity

router = APIRouter()

@router.get("/health", response_model=HealthResp)
def health():
    return HealthResp()

@router.post("/embed", response_model=EmbedResp)
def embed(req: EmbedReq):
    v = embed_texts([req.text])[0]
    return EmbedResp(dim=len(v), head=[float(x) for x in v[:8]])

@router.post("/judge", response_model=JudgeResp)
def judge(req: JudgeReq):
    v_en, v_ko = embed_texts([req.en, req.ko])
    sim = cosine_sim(v_en, v_ko)
    label = judge_similarity(sim)
    return JudgeResp(similarity=round(sim, 6), label=label)
