class QuantoTrabalhouPresidenteException(Exception):
    def __init__(self, status: int, message: str):
        self.status_code = status
        self.message = message


class RequiredFieldException(QuantoTrabalhouPresidenteException):
    def __init__(self, class_, required: str):
        message = f"{class_}: {required} not informed"
        super().__init__(406, message)
