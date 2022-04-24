from Business.Market import Market
from interfaces import IMarket
from typing import Dict
from Business.UserPackage.Member import Member
from interface import implements
from interfaces import IUser
from Business.UserPackage.SystemManager import SystemManager


def singleton_dec(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton_dec
class UserManagment(implements(IUser)):
    def __init__(self):
        self.__market: IMarket = Market()
        self.__members: Dict[str, Member] = {}
        self.__systemManager: Dict[str, SystemManager] = {}

    def guestLogin(self):
        try:
            if len(self.__systemManager) > 0:
                return self.__market.addGuest()
            else:
                raise Exception("There no system manager!")
        except Exception as e:
            return e

    def guestLogOut(self, guestID):  # need to remove cart!
        self.__market.getActiveUsers().pop(guestID)
        return True

    def memberSignUp(self, userName, password, phone, address, bank, icart):  # address is an object of "Adress"
        if self.__members.get(userName) is None:
            member = self.__market.addMember(userName, password, phone, address, bank)
            if member:
                self.__members[userName] = member
                if icart is not None:
                    member.setICart(icart)
                return member
        return None

    def memberLogin(self, userID, password):
        try:
            if len(self.__systemManager) > 0:
                i: Member = Member(None, None, None, None, None)
                check = False
                for i in self.__members:
                    if i.getUserName() == userID:
                        if self.__market.getActiveUsers().get(i) is not None:
                            self.__market.getActiveUsers()[i] = i
                            check = True
                            i.setLoggedIn(True)
                            i.setMemberCheck(True)
                        else:
                            raise Exception("member allready login")
                if not check:
                    raise Exception("The user ID " + userID + " not available!")
                self.checkPassword(userID, password)
            else:
                raise Exception("There no system manager!")
        except Exception as e:
            return e

    def logoutMember(self, userID):
        self.__market.getActiveUsers().pop(userID)
        self.__members.get(userID).setLoggedIn(False)
        self.__members.get(userID).setMemberCheck(False)
        return self.guestLogin()
