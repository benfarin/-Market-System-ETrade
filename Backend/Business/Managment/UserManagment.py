import zope

from Backend.Business.Address import Address
from Backend.Business.Bank import Bank
from Backend.Business.Market import Market
from Backend.Business.UserPackage.User import User
from Backend.Business.UserPackage.Guest import Guest
from Backend.Exceptions.CustomExceptions import NoSuchUserException, PasswordException, NotOnlineException, \
    SystemManagerException, MemberAllReadyLoggedIn
from Backend.Interfaces import IMarket
from typing import Dict
from Backend.Business.UserPackage.Member import Member
from Backend.Business.UserPackage.SystemManager import SystemManager
import bcrypt


class UserManagment(object):
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if UserManagment.__instance is None:
            UserManagment()
        return UserManagment.__instance

    def __init__(self):
        """ Virtually private constructor. """
        super(UserManagment, self).__init__()
        self.__market: IMarket = Market().getInstance()
        self.__activeUsers: Dict[str, User] = {}  # <userId,User> should check how to initial all the activeStores into
        # dictionary
        self.__guests: Dict[str: User] = {}
        self.__members: Dict[str, Member] = {}
        self.__systemManager: Dict[str, SystemManager] = {}

        if UserManagment.__instance is None:
            UserManagment.__instance = self

    def checkOnlineUser(self, userId):
        if (self.__activeUsers.get(userId)) is None:
            raise NotOnlineException("The member " + userId + " not online!")
        else:
            return True

    def getMembers(self):
        return self.__members

    def getActiveUser(self):
        return self.__activeUsers

    def getSystemManagers(self):
        return self.__systemManager

    def removeFromActiveUsers(self, userId):
        self.checkOnlineUser(userId)
        self.__activeUsers.pop(userId)

    def removeFromMembers(self, memberId):
        if memberId not in self.__members.keys():
            raise Exception("member: " + str(memberId) + " not exists")
        self.__members.pop(memberId)

    def enterSystem(self):
        try:
            guest = Guest()
            self.__guests[guest.getUserID()] = guest
            self.__activeUsers[guest.getUserID()] = guest
            # if User.get_user("Guest") is None:
            #     User.save(username="Guest", password="")
            return guest
        except Exception as e:
            raise Exception(e)

    def exitSystem(self, guestID):  # need to remove cart!
        self.checkOnlineUser(guestID)
        self.__guests.pop(guestID)
        self.__activeUsers.pop(guestID)
        return True

    def memberSignUp(self, userName, password, phone, address, bank):  # Tested
        if self.__isMemberExists(userName) is None:
            member = Member(userName, password, phone, address, bank)
            self.__members[member.getUserID()] = member
            # if User.get_user(userName) is None:
            #     User.save(username=userName, password=password)
            return True
        raise MemberAllReadyLoggedIn("user: " + userName + "is all ready loggedIn")

    def memberLogin(self, oldUserId, userName, password):  # Tested
        try:
            system_manager: SystemManager = self.__systemManager.get(userName)
            member: Member = self.__isMemberExists(userName)
            if member is None and system_manager is None:
                raise NoSuchUserException("The user ID " + userName + " not registered!")
            if system_manager is not None:
                if bcrypt.checkpw(password.encode('utf-8'), system_manager.getPassword()):
                    self.__activeUsers[system_manager.getUserID()] = system_manager
                    system_manager.setLoggedIn(True)
                    system_manager.setMemberCheck(True)
                    system_manager.loginUpdates()
                    system_manager.updateCart(self.__getUserCart(oldUserId))
                    return system_manager
            elif member is not None:
                if bcrypt.checkpw(password.encode('utf-8'), member.getPassword()):
                    self.__activeUsers[member.getUserID()] = member
                    member.setLoggedIn(True)
                    member.setMemberCheck(True)
                    member.loginUpdates()

                    member.updateCart(self.__getUserCart(oldUserId))

                    # self.__activeUsers.pop(oldUserId)  # guest no longer active, deu to him be a member
                    # self.__guests.pop(oldUserId)  # we can delete the guest.

                    return member
                else:
                    raise PasswordException("password not good!")
            else:
                raise NotOnlineException("member already login")
        except Exception as e:
            raise Exception(e)

    def __isMemberExists(self, userName):
        for member in self.__members.values():
            if member.getMemberName() == userName:
                return member
        return None

    def systemManagerSignUp(self, userName, password, phone, address, bank):
        if self.__members.get(userName) is None:
            systemManager: SystemManager = SystemManager(userName, password, phone, address, bank)
            if systemManager:
                self.__systemManager[userName] = systemManager
                # if User.get_user(userName) is None:
                #     User.save_admin(username=userName, password=password)
                return systemManager
        return None

    # from here is to move to user class
    def addProductToCart(self, userID, storeID, product, quantity):
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).addProductToCart(storeID, product, quantity)
        except Exception as e:
            raise Exception(e)

    def addProductToCartWithoutStore(self, userID, productID, quantity):
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).addProductToCartWithoutStore(productID, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromCart(self, userID, storeID, productId):
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).removeProductFromCart(storeID, productId)
        except Exception as e:
            raise Exception(e)

    def updateProductFromCart(self, userID, storeID, productId, quantity):
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).updateProductFromCart(storeID, productId, quantity)
        except Exception as e:
            raise Exception(e)

    def purchaseCart(self, userID, bank):
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).purchaseCart(bank)
        except Exception as e:
            raise Exception(e)

    def getCart(self, userID):
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).getCart()
        except Exception as e:
            raise Exception(e)

    def getSumAfterDiscount(self, userId):
        try:
            self.checkOnlineUser(userId)
            return self.__activeUsers.get(userId).getCartSum()
        except Exception as e:
            raise Exception(e)

    def createBankAcount(self, accountNumber, branch):
        return Bank(accountNumber, branch)

    def createAddress(self, country, city, street, apartmentNum, zipCode):
        return Address(country, city, street, apartmentNum, zipCode)

    def __getUserCart(self, userId):
        if userId not in self.__guests.keys():
            raise NoSuchUserException("user: " + str(userId) + "is not exists")
        return self.__guests.get(userId).getCart()

    def getUser(self,uid):
        if uid not in self.__activeUsers:
            raise NoSuchUserException("user: " + str(uid) + "is not exists")
        return self.__activeUsers.get(uid)

    def getUserByUserName(self, username):
        for member in self.__members.values():
            if member.getMemberName() == username:
                return member
        for admin in self.__systemManager.values():
            if admin.getMemberName() == username:
                return admin
        if username == "Guest":
            lst = list(self.__guests.values())
            return lst[0]
        return None


