from Business.Managment.UserManagment import UserManagment
from Exceptions.CustomExceptions import NoSuchMemberException


class MemberManagment(UserManagment):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MemberManagment.__instance is None:
            MemberManagment()
        return MemberManagment.__instance

    def __init__(self):
        """ Virtually private constructor. """
        super(MemberManagment, self).__init__()
        if MemberManagment.__instance is None:
            MemberManagment.__instance = self

    def getMembersFromUser(self):
        return self.getMembers()

    def getActiveUserFromUser(self):
        return self.getActiveUser()

    def checkOnlineUserFromUser(self, userId):
        return super().checkOnlineUser(userId)

    def createStore(self, storeName, userID, bank, address):
        try:
            self.checkOnlineUser(userID)
            member = self.getMembers().get(userID)
            if member is None:
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.createStore(storeName, bank, address)
        except Exception as e:
            raise Exception(e)

    def logoutMember(self, userName):
        user = self.getMembers().get(userName)
        self.checkOnlineUser(user.getUserID())
        system_manager = self.getSystemManagers().get(userName)
        if user is not None:
            self.getMembers().get(userName).setLoggedIn(False)
            self.getMembers().get(userName).setMemberCheck(False)
            self.__activeUsers.pop(user.getUserID())
        if system_manager is not None:
            self.__systemManager.get(userName).setLoggedIn(False)
            self.__systemManager.get(userName).setMemberCheck(False)
            self.__activeUsers.pop(system_manager.getUserID())
        return self.enterSystem()

    def getMemberTransactions(self, userID):
        self.checkOnlineUser(userID)
        member = self.getMembers().get(userID)
        if member is None:
            raise NoSuchMemberException("user: " + str(userID) + "is not a member")
        return member.getMemberTransactions()
