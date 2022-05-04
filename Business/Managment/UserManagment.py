import zope

from Business.Address import Address
from Business.Bank import Bank
from Business.Market import Market
from Business.UserPackage.User import User
from Business.UserPackage.Guest import Guest
from Exceptions.CustomExceptions import NoSuchUserException, PasswordException, NotOnlineException, \
    SystemManagerException
from interfaces import IMarket
from typing import Dict
from Business.UserPackage.Member import Member
from zope.interface import Interface
from interfaces.IUser import IUser
from Business.UserPackage.SystemManager import SystemManager
import bcrypt



class UserManagment:
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
        self.__activeUsers: Dict[str, User] = {}  # <name,User> should check how to initial all the activeStores into
                                                  # dictionary
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

    def getSystemManagers(self):
        return self.__systemManager

    def enterSystem(self):
        try:
            guest = Guest()
            self.__activeUsers[guest.getUserID()] = guest
            return guest
        except Exception as e:
            raise Exception(e)

    def exitSystem(self, guestID):  # need to remove cart!
        self.checkOnlineUser(guestID)
        self.__activeUsers.pop(guestID)
        return True

    def memberSignUp(self, userName, password, phone, address, bank):  # Tested
        if self.__members.get(userName) is None:
            member = Member(userName, password, phone, address, bank)
            self.__members[userName] = member
            # if icart is not None:
            #       member.setICart(icart)
            return member.getUserID()
        return None

    def memberLogin(self, userName, password):  # Tested
        try:
            system_manager: SystemManager = self.__systemManager.get(userName)
            member: Member = self.__members.get(userName)
            if member and system_manager is None:
                raise NoSuchUserException("The user ID " + userName + " not registered!")
            if system_manager is not None:
                if bcrypt.checkpw(password.encode('utf-8'), system_manager.getPassword()):
                    self.__activeUsers[system_manager.getUserID()] = system_manager
                    system_manager.setLoggedIn(True)
                    system_manager.setMemberCheck(True)
                    self.__activeUsers.get(member.getUserID()).loginUpdates(system_manager.getUserID())
                    return system_manager.getUserID()
            if self.__getActiveUsers().get(member.getUserID()) is None:
                if bcrypt.checkpw(password.encode('utf-8'), member.getPassword()):
                    self.__activeUsers[member.getUserID()] = member
                    member.setLoggedIn(True)
                    member.setMemberCheck(True)
                    self.__activeUsers.get(member.getUserID()).loginUpdates(member.getUserID())
                    return member.getUserID()
                else:
                    raise PasswordException("password not good!")
            else:
                raise NotOnlineException("member already login")
        except Exception as e:
            raise Exception(e)

    def systemManagerSignUp(self, userName, password, phone, address, bank):
        if self.__members.get(userName) is None:
            systemManager: SystemManager = SystemManager(userName, password, phone, address, bank)
            if systemManager:
                self.__systemManager[userName] = systemManager
                return systemManager.getUserID()
        return None

    # from here is to move to user class
    def addProductToCart(self, userID, storeID, product, quantity):
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).addProductToCart(storeID, product, quantity)
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

    def getProductByCategory(self, category):
        try:
            return self.__market.getProductByCategory(category)
        except Exception as e:
            raise Exception(e)

    def getProductsByName(self, nameProduct):
        try:
            return self.__market.getProductsByName(nameProduct)
        except Exception as e:
            raise Exception(e)

    def getProductByKeyWord(self, keyword):
        try:
            return self.__market.getProductByKeyWord(keyword)
        except Exception as e:
            raise Exception(e)

    def getProductPriceRange(self, minPrice, highPrice):
        try:
            return self.__market.getProductByPriceRange(minPrice, highPrice)
        except Exception as e:
            raise Exception(e)

    def createBankAcount(self, accountNumber, branch):
        return Bank(accountNumber, branch)

    def createAddress(self, country, city, street, apartmentNum, zipCode):
        return Address(country, city, street, apartmentNum, zipCode)

    def removeMember(self, userName, password):
        pass
