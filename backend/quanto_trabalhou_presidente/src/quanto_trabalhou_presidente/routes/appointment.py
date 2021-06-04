from fastapi import APIRouter, Path

from quanto_trabalhou_presidente.business.agenda import Agenda
from quanto_trabalhou_presidente.entities.appointment import Appointment
from quanto_trabalhou_presidente.models.appointment import GetAgendaResponse, GET_AGENDA_RESPONSES

router = APIRouter()


@router.get('/agenda/{date}', status_code=200, summary="Day Agenda",
            responses=GET_AGENDA_RESPONSES, response_model=GetAgendaResponse)
def agenda(date: str = Path(..., description="Data de consulta da agenda", example='2021-06-01')):
    appointment_list = Agenda(date).appointments
    return {
        'agenda': list(map(Appointment.format, appointment_list)),
        'total_time': sum([appointment.duration for appointment in appointment_list])
    }
