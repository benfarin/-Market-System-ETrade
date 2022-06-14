from Backend.Service.DTO.GuestDTO import GuestDTO
from Backend.Service.DTO.MemberDTO import MemberDTO


class LoginRecordDTO:
    def __init__(self, log):
        self.__loginDateRecordGuest = []
        self.__loginDateRecordRegularMembers = []
        self.__loginDateRecordJustManagers = []
        self.__loginDateRecordJustOwners = []
        self.__loginDateRecordSystemManager = []

        for record in log.get(0):
            self.__loginDateRecordGuest.append(GuestDTO(record))
        for record in log.get(1):
            self.__loginDateRecordRegularMembers.append(MemberDTO(record))
        for record in log.get(2):
            self.__loginDateRecordJustManagers.append(MemberDTO(record))
        for record in log.get(3):
            self.__loginDateRecordJustOwners.append(MemberDTO(record))
        for record in log.get(4):
            self.__loginDateRecordSystemManager.append(MemberDTO(record))

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

    def setAllGuest(self, loginGuest):
        self.__loginDateRecordGuest = []
        for record in loginGuest:
            self.__loginDateRecordGuest.append(GuestDTO(record))

    def setAllRegularGuest(self, regularMembers):
        self.__loginDateRecordRegularMembers = []
        for record in regularMembers:
            self.__loginDateRecordRegularMembers.append(MemberDTO(record))

    def setAllOnlyManagers(self, justManagers):
        self.__loginDateRecordRegularMembers = []
        for record in justManagers:
            self.__loginDateRecordJustManagers.append(MemberDTO(record))

    def setAllOnlyOwners(self, onlyOwners):
        self.__loginDateRecordRegularMembers = []
        for record in onlyOwners:
            self.__loginDateRecordJustOwners.append(MemberDTO(record))

    def setAllSystemManagers(self, systemManagers):
        self.__loginDateRecordRegularMembers = []
        for record in systemManagers:
            self.__loginDateRecordSystemManager.append(MemberDTO(record))

    def __str__(self):
        toReturn = "Guests:"
        for guest in self.__loginDateRecordGuest:
            toReturn += "\n\t\t" + guest.getUserID()
        toReturn += "\n\tOnly members:"
        for member in self.__loginDateRecordRegularMembers:
            toReturn += "\n\t\t" + member.getMemberName()
        toReturn += "\n\tOnly managers:"
        for manager in self.__loginDateRecordJustManagers:
            toReturn += "\n\t\t" + manager.getMemberName()
        toReturn += "\n\tOnly owners:"
        for owner in self.__loginDateRecordJustOwners:
            toReturn += "\n\t\t" + owner.getMemberName()
        toReturn += "\n\tOnly owners:"
        for owner in self.__loginDateRecordJustOwners:
            toReturn += "\n\t\t" + owner.getMemberName()
        return toReturn


