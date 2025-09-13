# Project TMI Word

영어 <-> 한글 텍스트 유사도 판단을 위한 API 서버

## 기능

- **텍스트 임베딩**: 입력된 텍스트를 벡터로 변환
- **유사도 판단**: 영어와 한국어 텍스트의 유사도를 측정
- **다국어 지원**: sentence-transformers 모델 사용

## API 엔드포인트

### 1. 헬스 체크

```bash
curl -X GET "http://localhost:8000/health"
```

### 2. 텍스트 임베딩

```bash
curl -X POST "http://localhost:8000/embed" \
  -H "Content-Type: application/json" \
  -d '{"text": "안녕하세요"}'
```

### 3. 유사도 판단

```bash
curl -X POST "http://localhost:8000/judge" \
  -H "Content-Type: application/json" \
  -d '{"en": "hello", "ko": "안녕"}'
```

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 서버 실행

```bash
uvicorn app.main:app --reload --port 8000
```

### 3. API 문서 확인

브라우저에서 `http://localhost:8000/docs` 접속

## 모델 정보

- **모델**: `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`
- **임베딩 차원**: 384
- **지원 언어**: 100개 이상

## 유사도 기준

- **맞음**: 0.80 이상 (매우 유사한 의미)
- **부분적**: 0.65~0.79 (어느 정도 유사한 의미)
- **아님**: 0.65 미만 (유사하지 않음)

## 프로젝트 구조

```
project-tmi-word/
├── app/
│   ├── main.py      # FastAPI 앱 설정
│   ├── api.py       # API 엔드포인트
│   ├── model.py     # 모델 로딩 및 임베딩
│   ├── service.py   # 유사도 계산 로직
│   └── schema.py    # Pydantic 스키마
├── requirements.txt
├── Dockerfile
└── README.md
```

## 예시

### 정확한 번역

```bash
curl -X POST "http://localhost:8000/judge" \
  -H "Content-Type: application/json" \
  -d '{"en": "The cat is sleeping", "ko": "고양이가 자고 있다"}'
```

**응답:**

```json
{
  "similarity": 0.823456,
  "label": "맞음"
}
```

### 부분적으로 일치

```bash
curl -X POST "http://localhost:8000/judge" \
  -H "Content-Type: application/json" \
  -d '{"en": "I love reading", "ko": "나는 독서를 좋아한다"}'
```

**응답:**

```json
{
  "similarity": 0.56789,
  "label": "부분적"
}
```

## 라이선스

MIT License
