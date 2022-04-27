class EventError:

    def __init__(self, actionName, *args):
        self.__actionName = actionName
        self.__args = []
        for i in range(len(args)):
            self.__args.append(args[i])

    def printEventError(self):
        print(self.__args)
