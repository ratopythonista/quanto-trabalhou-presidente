from typing import Optional

from pydantic import Field, BaseModel


class Pagination(BaseModel):
    next: str = Field(..., description="Url da próxima página")
    previous: str = Field(..., description="Url da página anterior")


class Message(BaseModel):
    status: int = Field(..., description="Código http")
    message: str = Field(..., description="Texto explicativo")
    stacktrace: Optional[str] = Field("", description="Stacktrace do erro")


DEFAULT_RESPONSES = [
    Message(status=422, message="Os parâmetros da requisição estão inválidos!",
            stacktrace="Traceback (most recent call last): ..."),
    Message(status=500, message="Ocorreu um erro interno!", stacktrace="Traceback (most recent call last): ...")
]


def parse_openapi(responses: list) -> dict:
    responses.extend(DEFAULT_RESPONSES)
    return {example.status: {"content": {"application/json": {"example": example.dict()}}, "model": Message}
            for example in responses}
