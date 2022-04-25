from Business.Address import Address
from Business.Bank import Bank
from Business.Market import Market
from interfaces import IMarket
from typing import Dict
from Business.UserPackage.Member import Member
from interface import implements
from interfaces import IUser
from Business.UserPackage.SystemManager import SystemManager


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

    def systemManagerSignUp(self,userName, password, phone, address, bank):
        if self.__members.get(userName) is None:
            systemManager : SystemManager = SystemManager(userName, password, phone, address, bank)
            if systemManager:
                self.__systemManager[userName] = systemManager
                return systemManager
        return None


    def guestLogin(self):
        try:
            if len(self.__systemManager) > 0:
                return self.__market.addGuest()
            else:
                raise Exception("There no system manager!")
        except Exception as e:
            raise Exception(e)

    def guestLogOut(self, guestID):  # need to remove cart!
        self.__market.getActiveUsers().pop(guestID)
        return True

    def memberSignUp(self, userName, password, phone, address, bank, icart):  # address is an object of "Adress"
        if self.__members.get(userName) is None:
            member = Member(userName, password, phone, address, bank)
            self.__members[userName] = member
            if icart is not None:
                  member.setICart(icart)
            return member
        return None

    def memberLogin(self, userName, password):
        try:
            if len(self.__systemManager) > 0:
                i: Member = Member(None, None, None, None, None)
                check = False
                for i in self.__members:
                    if i.getUserName() == userName:
                        if self.__market.getActiveUsers().get(i) is not None:
                            self.__market.getActiveUsers()[i] = i
                            check = True
                            i.setLoggedIn(True)
                            i.setMemberCheck(True)
                        else:
                            raise Exception("member allready login")


                if not check:
                    raise Exception("The user ID " + userName + " not available!")
                self.checkPassword(userName, password)
            else:
                raise Exception("There no system manager!")
        except Exception as e:
            raise Exception(e)

    def logoutMember(self, userID):
        self.__market.getActiveUsers().pop(userID)
        self.__members.get(userID).setLoggedIn(False)
        self.__members.get(userID).setMemberCheck(False)
        return self.guestLogin()

    def createBankAcount(self, accountNumber, branch):
        return Bank(accountNumber, branch)

    def createAddress(self, country, city, street, apartmentNum, zipCode):
        return Address(country, city, street, apartmentNum, zipCode)

