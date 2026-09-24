import logging
from pathlib import Path
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from backend.services.explanation_module import explain_topic
from backend.services.learning_path import get_learning_recommendations
from backend.services.qna import answer_question
from backend.services.quiz_module import generate_quiz
from backend.services.summary_module import summarize_text

load_dotenv()
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="Educational assistant with Q&A, explanations, quizzes, summaries and learning paths."
)

app.mount(
    "/static",
    StaticFiles(directory=PROJECT_DIR / "frontend" / "static"),
    name="static",
)
templates = Jinja2Templates(directory=str(PROJECT_DIR / "frontend" / "templates"))


def service_error(exc: Exception) -> HTTPException:
    """Log provider details while returning a safe, useful API response."""
    logger.exception("EduGenie request failed", exc_info=exc)
    return HTTPException(
        status_code=502,
        detail="The learning service is unavailable. Check your Gemini API key and try again.",
    )


class TextRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=10000)


class QuizRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=20000)
    count: int = Field(default=3, ge=1, le=10)


class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=500)
    level: str = Field(default="beginner", max_length=50)
    weekly_hours: int = Field(default=5, ge=1, le=40)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: QuestionRequest):
    try:
        return {"success": True, "result": await answer_question(payload.question)}
    except Exception as exc:
        raise service_error(exc)


@app.post("/explain")
async def explain(payload: TextRequest):
    try:
        return {"success": True, "result": await explain_topic(payload.text)}
    except Exception as exc:
        raise service_error(exc)


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    try:
        return {"success": True, "result": await generate_quiz(payload.text, payload.count)}
    except Exception as exc:
        raise service_error(exc)


@app.post("/summarize")
async def summarize(payload: TextRequest):
    try:
        return {"success": True, "result": await summarize_text(payload.text)}
    except Exception as exc:
        raise service_error(exc)


@app.post("/learn/recommendations")
async def learning_recommendations(payload: LearningPathRequest):
    try:
        return {
            "success": True,
            "result": await get_learning_recommendations(
                payload.topic, payload.level, payload.weekly_hours
            ),
        }
    except Exception as exc:
        raise service_error(exc)




