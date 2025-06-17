class InvalidEmailException(Exception):
    def __init__(self, message="Invalid email address"):
        super().__init__(message)