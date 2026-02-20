class WrongFileTypeError(Exception):
    def __init__(self, message: str = "File not found"):
        super().__init__(message)