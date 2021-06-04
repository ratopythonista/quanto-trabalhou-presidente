from datetime import datetime
from dataclasses import dataclass


@dataclass
class Appointment:
    title: str
    start: datetime
    end: datetime
    participants: list

    @property
    def duration(self) -> int:
        return (self.end - self.start).total_seconds()

    @staticmethod
    def format(appointment: 'Appointment'):
        return {
            'title': appointment.title,
            'start': appointment.start.timestamp(),
            'end': appointment.end.timestamp(),
            'participants': appointment.participants,
            'durantion': appointment.duration
        }
