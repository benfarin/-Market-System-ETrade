from Business.Managment.UserManagment import UserManagment
from Exceptions.CustomExceptions import NoSuchMemberException
import threading
from concurrent.futures import Future


def call_with_future(fn, future, args, kwargs):
    try:
        result = fn(*args, **kwargs)
        future.set_result(result)
    except Exception as exc:
        future.set_exception(exc)


def threaded(fn):
    def wrapper(*args, **kwargs):
        future = Future()
        threading.Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
        return future.result()

    return wrapper


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

    def removeStore(self, userID, storeId):
        try:
            self.checkOnlineUser(userID)
            member = self.getMembers().get(userID)
            if member is None:
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")

            # need somehow to lock all function that trying to get to the store
            member.removeStore(storeId)
            for user in self.getActiveUser().values():
                user.getCart().removeBag(storeId)

            return True
        except Exception as e:
            raise Exception(e)

    def logoutMember(self, userName):
        try:
            user = self.getMembers().get(userName)
            system_manager = self.getSystemManagers().get(userName)
            if user is not None:
                self.checkOnlineUser(user.getUserID())
                self.getMembers().get(userName).setLoggedIn(False)
                self.getMembers().get(userName).setMemberCheck(False)
                self.__activeUsers.pop(user.getUserID())
            if system_manager is not None:
                self.__systemManager.get(userName).setLoggedIn(False)
                self.__systemManager.get(userName).setMemberCheck(False)
                self.__activeUsers.pop(system_manager.getUserID())
            return True
        except Exception as e:
            raise Exception(e)

    def getMemberTransactions(self, userID):
        self.checkOnlineUser(userID)
        member = self.getMembers().get(userID)
        if member is None:
            raise NoSuchMemberException("user: " + str(userID) + "is not a member")
        return member.getMemberTransactions()
