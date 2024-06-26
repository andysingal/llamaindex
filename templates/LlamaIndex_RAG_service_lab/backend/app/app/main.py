from contextlib import asynccontextmanager
from fastapi import FastAPI

from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

from app.api.api_router import api_router
from app.utils.logging import AppLogger
from app.config import settings


logger = AppLogger().get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info('[Main] Setting up the app...')
    logger.info('[Main] Set LLM and Embedding models.')
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-base-en-v1.5")
    Settings.llm = Ollama(base_url=settings.OLLAMA_URL, model="llama3", request_timeout=10000.0)
    logger.info('[Main] App setup complete.')
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix='/api/v1')

logger.info('[Main] FastAPI app started.')