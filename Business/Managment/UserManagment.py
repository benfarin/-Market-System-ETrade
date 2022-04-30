from Business.Address import Address
from Business.Bank import Bank
from Business.Market import Market
from Business.UserPackage.User import User
from Exceptions.CustomExceptions import NoSuchUserException, PasswordException, NotOnlineException, \
    SystemManagerException
from interfaces import IMarket
from typing import Dict
from Business.UserPackage.Member import Member
from interface import implements
from interfaces.IUser import IUser
from Business.UserPackage.SystemManager import SystemManager
import bcrypt


class UserManagment(implements(IUser)):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if UserManagment.__instance is None:
            UserManagment()
        return UserManagment.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.__market: IMarket = Market().getInstance()
        self.__members: Dict[str, Member] = {}
        self.__systemManager: Dict[str, SystemManager] = {}
        if UserManagment.__instance is None:
            UserManagment.__instance = self

    def getMembers(self):
        return self.__members

    def guestLogin(self):
        try:
            if len(self.__systemManager) > 0:
                return self.__market.addGuest()
            else:
                raise SystemManagerException("There no system manager!")
        except Exception as e:
            raise Exception(e)


    def guestLogOut(self, guestID):  # need to remove cart!
        self.__market.getActiveUsers().pop(guestID)
        return True


    def memberSignUp(self, userName, password, phone, address, bank):  # Tested
        if self.__members.get(userName) is None:
            member = Member(userName, password, phone, address, bank)
            self.__members[userName] = member
            # if icart is not None:
            #       member.setICart(icart)
            return member.getUserID()
        return None



    def memberLogin(self, userName, password): #Tested
        try:
            if len(self.__systemManager) > 0:
                i : Member = self.__members.get(userName)
                if i is None:
                    raise NoSuchUserException("The user ID " + userName + " not registered!")
                if self.__market.getActiveUsers().get(i.getUserID()) is None:
                    if bcrypt.checkpw(password.encode('utf-8'), i.getPassword()):
                        self.__market.addActiveUser(i)
                        i.setLoggedIn(True)
                        i.setMemberCheck(True)
                        self.__market.loginUpdates(i.getUserID())
                        return i.getUserID()
                    else:
                        raise PasswordException("password not good!")
                else:
                    raise NotOnlineException("member already login")
            else:
                raise SystemManagerException("There no system manager!")
        except Exception as e:
            raise Exception(e)

    def logoutMember(self, userName):
        user = self.__members.get(userName)
        self.__members.get(userName).setLoggedIn(False)
        self.__members.get(userName).setMemberCheck(False)
        self.__market.getActiveUsers().pop(user.getUserID())
        return self.guestLogin()

    def systemManagerSignUp(self, userName, password, phone, address, bank):
        if self.__members.get(userName) is None:
            systemManager: SystemManager = SystemManager(userName, password, phone, address, bank)
            if systemManager:
                self.__systemManager[userName] = systemManager
                return systemManager.getUserID()
        return None


    def createBankAcount(self, accountNumber, branch):
        return Bank(accountNumber, branch)

    def createAddress(self, country, city, street, apartmentNum, zipCode):
        return Address(country, city, street, apartmentNum, zipCode)

    def removeMember(self,userName,password):
        pass