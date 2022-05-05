class Response:

    def __init__(self, arg):
        self.__error = None
        if isinstance(arg, str):
            self.__error = arg
        else:
            self.__data = arg

    def isError(self):
        return self.__error is None

    def getError(self):
        return self.__error

    def getData(self):
        return self.__data

    def __str__(self):
        if self.isError():
            return self.__error
        return self.__data.__str__
