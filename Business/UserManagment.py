from Business.MarketManage import MarketManage
from interfaces import IMarket
from typing import Dict
from Business.UserPackage.Member import Member
from interface import implements
from interfaces import IUser
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
        self.__market : IMarket = MarketManage()
        self.__members : Dict [str, Member] ={}

    def guestLogin(self):
        return self.__market.addGuest()

    def guestLogOut(self, guestID): #need to remove cart!
        self.__market.getActiveUsers().pop(guestID)
        return True

    def memberSignUp(self,userName, password, phone, address, bank , icart): #address is an object of "Adress"
        if(self.__members.get(userName) == None):
            member =  self.__market.addMember(userName, password, phone, address, bank)
            if(member):
                self.__members[userName] = member
                if icart != None:
                    member.setICart(icart)
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
                        i.setMemberCheck(True)
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
        self.__members.get(userName).setMemberCheck(False)
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

    def checkAssigners(self, assignerName, assigneName):
        try:
            if (self.__members.get(assignerName) == None):
                raise Exception("assigner " + assignerName + " name not good!")
            if (self.__members.get(assigneName) == None):
                raise Exception("assigne " + assigneName + " name not good!")
        except Exception as e:
            return e

    def saveProducts(self,userName,store):
        if (self.checkOnlineUser(userName)):
            self.__market.getActiveUsers().get(userName).getShoppingCart().addBag(store.getStoreId())

    def appointManagerToStore(self,storeID, assignerName , assigneName ): # check if the asssigne he member and assignerID!!
        try:
            self.checkAssigners(assignerName, assigneName)
            self.__market.appointManagerToStore(storeID,assignerName,assigneName)
        except Exception as e:
            return e
    def appointOwnerToStore(self,storeID, assignerName , assigneName):# check if the asssigne he member and assignerID!!
        try:
            self.checkAssigners(assignerName,assigneName)
            self.__market.appointOwnerToStore(storeID, assignerName, assigneName)
        except Exception as e:
            return e

    def setStockManagementPermission(self,storeID, assignerName, assigneName):
        try:
            self.checkAssigners(assignerName, assigneName)
            self.__market.setStockManagerPermission(storeID, assignerName, assigneName)
        except Exception as e:
            return e

    def setAppointManagerPermission(self,storeID ,assignerName, assigneName):
        try:
            self.checkAssigners(assignerName, assigneName)
            self.__market.setAppointOwnerPermission(storeID, assignerName, assigneName)
        except Exception as e:
            return e

    def setAppointOwnerPermission(self,storeID ,assignerName, assigneName):
        try:
            self.checkAssigners(assignerName, assigneName)
            self.__market.setAppointOwnerPermission(storeID, assignerName, assigneName)
        except Exception as e:
            return e

    def setChangePermission(self,storeID ,assignerName, assigneName):
        try:
            self.checkAssigners(assignerName, assigneName)
            self.__market.setChangePermission(storeID, assignerName, assigneName)
        except Exception as e:
            return e

    def setRolesInformationPermission(self,storeID, assignerName, assigneName):
        try:
            self.checkAssigners(assignerName, assigneName)
            self.__market.setRolesInformationPermission(storeID, assignerName, assigneName)
        except Exception as e:
            return e

    def setPurchaseHistoryInformationPermission(self,storeID, assignerName, assigneName):
        try:
            self.checkAssigners(assignerName, assigneName)
            self.__market.setPurchaseHistoryInformationPermission(storeID, assignerName, assigneName)
        except Exception as e:
            return e



