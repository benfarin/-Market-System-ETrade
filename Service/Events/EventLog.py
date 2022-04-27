class EventLog:

    def __init__(self, actionName, *args):
        self.__actionName = actionName
        self.__args = []
        for i in range(len(args)):
            self.__args.append(args[i])

    def printEventLog(self):
        info = " " + self.__actionName + ":"
        for arg in self.__args:
            info += "\n\t\t" + arg
        return info

