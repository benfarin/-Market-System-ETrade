from Business.MarketManage import MarketManage
from interfaces import IMarket
from typing import Dict
from Business.UserPackage.Member import Member
class UserManagment:
    def __init__(self):
        self.__market : IMarket = MarketManage()
        self.__members : Dict [str, Member] ={}

    def guestLogin(self):
        return self.__market.addGuest()

    def guestLogOut(self, guestID): #need to remove cart!
        self.__market.getActiveUsers().pop(guestID)
        return True

    def memberSignUp(self,userName, password, phone, address, bank): #address is an object of "Adress"
        if(self.__members.get(userName) == None):
            member =  self.__market.addMember(userName, password, phone, address, bank)
            if(member):
                self.__members[userName] = member
                return member
        return None


    def memberLogin(self,userName, password):
        try:
            i : Member = Member(None,None,None,None,None)
            check = False
            for i in self.__members:
                if (i.getUserName() == userName):
                    if (self.__market.getActiveUsers().get(i) != None):
                        self.__market.getActiveUsers()[i] = i
                        check = True
                        i.setLoggedIn(True)
                    else:
                        raise Exception("member allready login")
            if (check == False):
                raise Exception("The user name "+ userName  + " not available!")
            self.checkPassword(userName,password)
        except Exception as e:
            return e

    def logoutMember(self,userName):
        self.__market.getActiveUsers().pop(userName)
        self.__members.get(userName).setLoggedIn(False)
        return self.guestLogin()

    def checkPassword(self,userName ,password):
        try:
            if(self.__members.get(userName).getPassword() == password):
                return True
            else:
                raise Exception("problem with password")
        except Exception as e:
            return e
    def checkOnlineUser(self,userName):
        if (self.__market.getActiveUsers().get(userName)):
           return True
        else:
           return False

    def saveProducts(self,userName,store):
        if (self.checkOnlineUser(userName)):
            self.__market.getActiveUsers().get(userName).getShoppingCart().addBag(store.getStoreId())



