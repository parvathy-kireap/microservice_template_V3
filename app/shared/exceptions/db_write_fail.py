from fastapi import status


class DBAWriteFailedException(Exception):
    """
    when the data adding failed
    """
    code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str, code: int = 500):
        self.code = code
        super().__init__(message)
