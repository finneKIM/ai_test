
# KoBERT의 원래 토크나이저 사용
# https://huggingface.co/jeonghyeon97/koBERT-Senti5


from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field   # 입력과 출력 형식을 자동으로 검사해주는 라이브러리
from transformers import AutoTokenizer, BertForSequenceClassification
import torch
import torch.nn.functional as F     # 각 감정의 확률을 계산하기 위한 함수
from contextlib import asynccontextmanager  # 서버 시작/종료 시점에 모델을 로드하거나 정리하기 위한 문법

SENTIMENT_LABELS = {
    0: "Angry",
    1: "Fear",
    2: "Happy",
    3: "Tender",
    4: "Sad"
}

# API 문서화와 데이터 검증을 위해 필요
class PredictRequest(BaseModel):
    text: str = Field(..., example="오늘 기분이 너무 좋아요!")

class PredictResponse(BaseModel):
    sentiment: str = Field(..., description="예측된 감정 레이블")
    probabilities: dict[str, float] = Field(
        ..., description="각 감정 레이블에 대한 softmax 확률"
    )


# lifespan — 서버 시작/종료 시 모델 로드 관리
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 앱 시작 전에 모델과 토크나이저 로드
    tokenizer = AutoTokenizer.from_pretrained("monologg/kobert", trust_remote_code=True)
    model = BertForSequenceClassification.from_pretrained("jeonghyeon97/koBERT-Senti5")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.eval()
    # 상태 저장
    app.state.tokenizer = tokenizer
    app.state.model = model
    app.state.device = device
    # 이제 앱 요청 받기 시작
    yield # 기준으로 앞뒤에서 서버 실행전과 서버 종료 후의 상태 등에 대해서 관리
    # 앱 종료 직전에 리소스 정리 가능 (필요시)
    # 예: model.cpu(), torch.cuda.empty_cache() 등



# FastAPI 앱 생성
# 앱을 만들면서 위의 lifespan을 연결 → 서버 켜질 때 모델이 자동으로 로드됨
app = FastAPI(
    lifespan=lifespan
)



# 예측 API 정의
@app.post(
    "/predict",
    response_model=PredictResponse,
    summary="감정 분석",
    description="입력된 문장에 대해 감정을 예측하고, 각 레이블에 대한 확률도 제공합니다."
)
def predict(request: PredictRequest):
    # 예측 과정
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="텍스트를 입력해주세요.")
    
    tokenizer = app.state.tokenizer
    model = app.state.model
    device = app.state.device

    # 입력 토큰화
    # → 문장을 토큰화(tokenize) 해서 숫자 ID로 변환
    # → padding, truncation으로 문장 길이를 조정
    # → tensor를 GPU나 CPU로 보냄
    inputs = tokenizer([text], return_tensors="pt", padding=True, truncation=True).to(device)

    # 예측 수행
    # → 모델 추론 (no_grad로 연산 그래프를 끔 → 더 빠르고 메모리 절약)
    # → logits: 모델의 출력 원본 점수
    # → softmax: 각 감정별 확률로 변환
    # → squeeze(): 차원 정리 → 리스트로 변환
    with torch.no_grad():
        outputs = model(**inputs)
        logits = outputs.logits
        probs = F.softmax(logits, dim=-1).squeeze().cpu().tolist()


    # 레이블 + 확률 매핑 : 감정 이름과 확률값을 딕셔너리로 묶음
    probabilities = {
        SENTIMENT_LABELS[idx]: float(probs[idx]) for idx in range(len(probs))
    }
    # 가장 높은 확률의 감정을 선택
    pred_idx = int(torch.argmax(logits, dim=-1).cpu().item())
    sentiment = SENTIMENT_LABELS.get(pred_idx, "Unknown")
    
    # 최종 결과를 PredictResponse 형식으로 반환
    return PredictResponse(sentiment=sentiment, probabilities=probabilities)

