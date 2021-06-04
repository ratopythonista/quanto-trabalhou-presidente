from typing import List

from pydantic import Field, BaseModel

from quanto_trabalhou_presidente.models import parse_openapi


class Appointment(BaseModel):
    title: str = Field(..., description="Titulo do evento")
    start: int = Field(..., description="Timestamp do inicio do evento")
    end: int = Field(..., description="Timestamp do fim do evento")
    participants: List[str] = Field(..., description="Participantes relacionados no evento")
    durantion: int = Field(..., description="Duração em segundos da atividade")


class GetAgendaResponse(BaseModel):
    agenda: List[Appointment]
    total_time: int = Field(..., description="Duração total em segundos das atividades do dia")


GET_AGENDA_RESPONSES = parse_openapi([])
