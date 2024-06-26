from fastapi import APIRouter
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

from app.utils.logging import AppLogger


router = APIRouter()
logger = AppLogger().get_logger()


@router.get("/test")
async def search_simple_txt_file():
    documents = SimpleDirectoryReader("data").load_data()

    index = VectorStoreIndex.from_documents(documents,)

    query_engine = index.as_query_engine()
    response = query_engine.query("What did the author do growing up?")

    print(response)

    return response