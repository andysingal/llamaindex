from pydantic import BaseModel, Field

from typing import Literal


class InferRequest(BaseModel):
    model: str = Field(default="llama3")
    prompt: str
    format: Literal["json"]
    stream: bool = Field(default=False)