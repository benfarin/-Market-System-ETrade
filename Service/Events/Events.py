class Events:

    def __init__(self):
        self.__logs = []
        self.__errors = []

    def addEventLog(self, eventLog):
        self.__logs.append(eventLog)

    def addEventError(self, eventError):
        self.__errors.append(eventError)

    def printEvents(self):
        info = "Events: "
        info += "\n  EventsLog: "
        for eventLog in self.__logs:
            info += "\n\t" + eventLog.printEventLog() + "\n"
        info += "\n  EventsError: "
        for eventError in self.__errors:
            info += "\n\t" + eventError.printEventError() + "\n"
        return info

