class GroupErrorModel:
    def __init__(self):
        self.__has_error = None
        self.__exception_message = None

    def __init__(self, has_error, exception_message):
        self.__has_error = has_error
        self.__exception_message = exception_message

    @property
    def has_error(self):
        return self.__has_error

    @property
    def exception_message(self):
        return self.__exception_message

    @has_error.setter
    def has_error(self, value):
        self.__has_error = value

    @exception_message.setter
    def exception_message(self, msg):
        self.__exception_message = msg
