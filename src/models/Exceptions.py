class ApplicationException(Exception):
    __exception_message__ = 'Application Exception raised'
    def __init__(self, e:Exception):
        self.__root__exception__ = e


class ResponseNotSentException(ApplicationException):
    __exception_message__ = 'Unable to send response'
