from contextlib import asynccontextmanager
from fastapi import FastAPI
from .api import router
from .model import get_model

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 기동 시 모델 미리 로딩(콜드스타트 감소)
    _ = get_model()
    yield

app = FastAPI(title="project-tmi-word", lifespan=lifespan)
app.include_router(router)
