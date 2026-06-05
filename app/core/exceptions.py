class BaseAppException(Exception):
    def __init__(self, message:str):
        self.message = message
        super().__init__(self.message)

class LLMException(BaseAppException):
    pass

class DatabaseException(BaseAppException):
    pass

class VectorDBException(BaseAppException):
    pass

class ResearchException(BaseAppException):
    pass

class NotFoundException(BaseAppException):
    pass

class ValidationException(BaseAppException):
    pass
