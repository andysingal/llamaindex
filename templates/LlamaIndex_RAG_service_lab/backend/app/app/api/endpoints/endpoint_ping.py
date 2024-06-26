from fastapi import APIRouter


router = APIRouter()


@router.get("/ping")
def hello():
    return {"message": "pong"}
