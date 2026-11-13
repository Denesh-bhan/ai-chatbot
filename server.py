from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field
from typing import List, Optional
import uuid
from datetime import datetime

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI()
api_router = APIRouter(prefix="/api")


# ---------- Models ----------
class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    subtitle: str
    type: str  # "research paper" | "practical guide" | "dataset"
    pages: int = 0
    year: int = 2024


class DocumentIn(BaseModel):
    title: str
    subtitle: str
    type: str
    pages: int = 0
    year: int = 2024


class Prompt(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    order: int = 0
    text: str


class PromptIn(BaseModel):
    text: str
    order: int = 0


class Citation(BaseModel):
    doc: str
    page: int


class Answer(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    keywords: List[str]
    answer: str
    citations: List[Citation] = []


class AnswerIn(BaseModel):
    keywords: List[str]
    answer: str
    citations: List[Citation] = []


class Stat(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    label: str
    value: str
    order: int = 0


class StatIn(BaseModel):
    label: str
    value: str
    order: int = 0


class ChatMessage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    role: str  # "user" | "assistant"
    content: str
    citations: List[Citation] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatIn(BaseModel):
    query: str
    session_id: Optional[str] = None


# ---------- Helpers ----------
def _strip_mongo_id(d):
    if not d:
        return d
    d.pop("_id", None)
    return d


async def _score_answer(query: str):
    """Simple keyword-overlap scoring over the answers collection."""
    q = query.lower()
    best = None
    best_score = 0
    async for a in db.answers.find():
        score = sum(1 for kw in a.get("keywords", []) if kw.lower() in q)
        if score > best_score:
            best_score = score
            best = a
    return _strip_mongo_id(best) if best_score > 0 else None


# ---------- Routes ----------
@api_router.get("/")
async def root():
    return {"message": "WattWisdom API online"}


@api_router.get("/library")
async def get_library():
    docs = [_strip_mongo_id(d) async for d in db.documents.find().sort("year", 1)]
    stats = [_strip_mongo_id(s) async for s in db.stats.find().sort("order", 1)]
    counts = {
        "researchPapers": await db.documents.count_documents({"type": "research paper"}),
        "practicalGuides": await db.documents.count_documents({"type": "practical guide"}),
        "datasets": await db.documents.count_documents({"type": "dataset"}),
    }
    return {"documents": docs, "stats": stats, "counts": counts}


@api_router.get("/prompts", response_model=List[Prompt])
async def get_prompts():
    return [Prompt(**_strip_mongo_id(p)) async for p in db.prompts.find().sort("order", 1)]


@api_router.post("/documents", response_model=Document)
async def add_document(body: DocumentIn):
    d = Document(**body.dict())
    await db.documents.insert_one(d.dict())
    return d


@api_router.post("/prompts", response_model=Prompt)
async def add_prompt(body: PromptIn):
    p = Prompt(**body.dict())
    await db.prompts.insert_one(p.dict())
    return p


@api_router.post("/answers", response_model=Answer)
async def add_answer(body: AnswerIn):
    a = Answer(**body.dict())
    await db.answers.insert_one(a.dict())
    return a


@api_router.post("/stats", response_model=Stat)
async def add_stat(body: StatIn):
    s = Stat(**body.dict())
    await db.stats.insert_one(s.dict())
    return s


@api_router.post("/chat")
async def chat(body: ChatIn):
    query = (body.query or "").strip()
    if not query:
        raise HTTPException(status_code=400, detail="query is required")

    session_id = body.session_id or str(uuid.uuid4())

    user_msg = ChatMessage(role="user", content=query)
    match = await _score_answer(query)
    if match:
        bot_msg = ChatMessage(
            role="assistant",
            content=match["answer"],
            citations=[Citation(**c) for c in match.get("citations", [])],
        )
    else:
        bot_msg = ChatMessage(
            role="assistant",
            content=(
                "That question is grounded outside the currently indexed sources. "
                "WattWisdom will not speculate beyond the JETIR1405001 paper, the practical guide, "
                "or the Kaggle Smart-meters-in-London bundle."
            ),
            citations=[],
        )

    await db.chat_sessions.update_one(
        {"id": session_id},
        {
            "$setOnInsert": {"id": session_id, "created_at": datetime.utcnow()},
            "$push": {"messages": {"$each": [user_msg.dict(), bot_msg.dict()]}},
        },
        upsert=True,
    )

    return {"session_id": session_id, "user_msg": user_msg.dict(), "bot_msg": bot_msg.dict()}


# ---------- Seed ----------
from seed_data import DOCUMENTS, PROMPTS, ANSWERS, STATS  # noqa: E402


@api_router.post("/seed")
async def seed():
    await db.documents.delete_many({})
    await db.prompts.delete_many({})
    await db.answers.delete_many({})
    await db.stats.delete_many({})

    if DOCUMENTS:
        await db.documents.insert_many([Document(**d).dict() for d in DOCUMENTS])
    if PROMPTS:
        await db.prompts.insert_many([Prompt(**p).dict() for p in PROMPTS])
    if ANSWERS:
        await db.answers.insert_many([Answer(**a).dict() for a in ANSWERS])
    if STATS:
        await db.stats.insert_many([Stat(**s).dict() for s in STATS])

    return {
        "documents": len(DOCUMENTS),
        "prompts": len(PROMPTS),
        "answers": len(ANSWERS),
        "stats": len(STATS),
        "status": "seeded",
    }


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
