class LoginRecordDTO:
    def __init__(self, log):
        self.__loginDateRecordGuest = log.get(0)
        self.__loginDateRecordRegularMembers = log.get(1)
        self.__loginDateRecordJustManagers = log.get(2)
        self.__loginDateRecordJustOwners = log.get(3)
        self.__loginDateRecordSystemManager = log.get(4)

    def getAllGuest(self):
        return self.__loginDateRecordGuest

    def getAllRegularMembers(self):
        return self.__loginDateRecordRegularMembers

    def getAllOnlyManagers(self):
        return self.__loginDateRecordJustManagers

    def getAllOnlyOwners(self):
        return self.__loginDateRecordJustOwners

    def getAllSystemManagers(self):
        return self.__loginDateRecordSystemManager

    def __str__(self):
        toReturn = "Guests:"
        for guestId in self.__loginDateRecordGuest:
            toReturn += "\n\t" + str(guestId)
        toReturn += "\nOnly members:"
        for memberName in self.__loginDateRecordRegularMembers:
            toReturn += "\n\t" + memberName
        toReturn += "\nOnly managers:"
        for memberName in self.__loginDateRecordJustManagers:
            toReturn += "\n\t" + memberName
        toReturn += "\nOnly owners:"
        for memberName in self.__loginDateRecordJustOwners:
            toReturn += "\n\t" + memberName
        toReturn += "\nsystem managers:"
        for memberName in self.__loginDateRecordSystemManager:
            toReturn += "\n\t" + memberName
        return toReturn


