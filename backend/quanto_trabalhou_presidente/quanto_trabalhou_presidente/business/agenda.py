from datetime import datetime
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

from quanto_trabalhou_presidente.entities.appointment import Appointment
from quanto_trabalhou_presidente.exceptions import QuantoTrabalhouPresidenteException


@dataclass
class Agenda:
    date: str
    url: str = 'https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/agenda-do-presidente-da-republica'

    @property
    def appointments(self) -> list:
        self.__is_date_valid()
        response = requests.get(f'{self.url}/{self.date}')
        soup = BeautifulSoup(response.text, 'html.parser')
        appointment_list = list()

        for appointment in soup.find_all(class_='item-compromisso-wrapper'):
            participants = appointment.find(class_='compromisso-participantes')
            if participants:
                participants = [participant.text.strip() for participant in participants.find_all('li')]
            else:
                participants = list()
            appointment_start = appointment.find(class_='compromisso-inicio').text
            appointment_end = appointment.find(class_='compromisso-fim').text

            appointment_list.append(
                Appointment(
                    title=appointment.find(class_='compromisso-titulo').text,
                    start=datetime.strptime(f'{self.date} {appointment_start}', '%Y-%m-%d %Hh%M'),
                    end=datetime.strptime(f'{self.date} {appointment_end}', '%Y-%m-%d %Hh%M'),
                    participants=participants
                )
            )
        return appointment_list

    def __is_date_valid(self):
        try:
            datetime.strptime(f'{self.date}', '%Y-%m-%d')
        except ValueError:
            raise QuantoTrabalhouPresidenteException(status=401, message="Data inválida")
