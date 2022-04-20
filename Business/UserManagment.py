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


    def memberLogin(self,userID, password):
        try:
            i : Member = Member(None,None,None,None,None)
            check = False
            for i in self.__members:
                if (i.getUserName() == userID):
                    if (self.__market.getActiveUsers().get(i) != None):
                        self.__market.getActiveUsers()[i] = i
                        check = True
                        i.setLoggedIn(True)
                        i.setMemberCheck(True)
                    else:
                        raise Exception("member allready login")
            if (check == False):
                raise Exception("The user ID "+ userID  + " not available!")
            self.checkPassword(userID,password)
        except Exception as e:
            return e

    def logoutMember(self,userID):
        self.__market.getActiveUsers().pop(userID)
        self.__members.get(userID).setLoggedIn(False)
        self.__members.get(userID).setMemberCheck(False)
        return self.guestLogin()

    def checkPassword(self,userID ,password):
        try:
            if(self.__members.get(userID).getPassword() == password):
                return True
            else:
                raise Exception("problem with password")
        except Exception as e:
            return e
    def checkOnlineUser(self,userID):
        if (self.__market.getActiveUsers().get(userID)):
           return True
        else:
           return False

    def checkAssigners(self, assignerID, assigneID):
        try:
            if (self.__members.get(assignerID) == None):
                raise Exception("assigner " + assignerID + " name not good!")
            if (self.__members.get(assigneID) == None):
                raise Exception("assigne " + assigneID + " name not good!")
        except Exception as e:
            return e

    def saveProducts(self,assignerID,store):
        if (self.checkOnlineUser(assignerID)):
            self.__market.getActiveUsers().get(assignerID).getShoppingCart().addBag(store.getStoreId())

    def appointManagerToStore(self,storeID, assignerID , assigneID ): # check if the asssigne he member and assignerID!!
        try:
            self.checkAssigners(assignerID, assigneID)
            self.__market.appointManagerToStore(storeID,assignerID,assigneID)
        except Exception as e:
            return e
    def appointOwnerToStore(self,storeID, assignerID , assigneID):# check if the asssigne he member and assignerID!!
        try:
            self.checkAssigners(assignerID,assigneID)
            self.__market.appointOwnerToStore(storeID, assignerID, assigneID)
        except Exception as e:
            return e

    def setStockManagementPermission(self,storeID, assignerID, assigneID):
        try:
            self.checkAssigners(assignerID, assigneID)
            self.__market.setStockManagerPermission(storeID, assignerID, assigneID)
        except Exception as e:
            return e

    def setAppointManagerPermission(self,storeID ,assignerID, assigneID):
        try:
            self.checkAssigners(assignerID, assigneID)
            self.__market.setAppointOwnerPermission(storeID, assignerID, assigneID)
        except Exception as e:
            return e

    def setAppointOwnerPermission(self,storeID ,assignerID, assigneID):
        try:
            self.checkAssigners(assignerID, assigneID)
            self.__market.setAppointOwnerPermission(storeID, assignerID, assigneID)
        except Exception as e:
            return e

    def setChangePermission(self,storeID ,assignerID, assigneID):
        try:
            self.checkAssigners(assignerID, assigneID)
            self.__market.setChangePermission(storeID, assignerID, assigneID)
        except Exception as e:
            return e

    def setRolesInformationPermission(self,storeID, assignerID, assigneID):
        try:
            self.checkAssigners(assignerID, assigneID)
            self.__market.setRolesInformationPermission(storeID, assignerID, assigneID)
        except Exception as e:
            return e

    def setPurchaseHistoryInformationPermission(self,storeID, assignerID, assigneID):
        try:
            self.checkAssigners(assignerID, assigneID)
            self.__market.setPurchaseHistoryInformationPermission(storeID, assignerID, assigneID)
        except Exception as e:
            return e



