import os
import threading
import django

from ModelsBackend.models import MemberModel, UserModel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frontend.settings')
django.setup()
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
from django.contrib.auth.hashers import make_password, check_password


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
        self.__activeUsers = None # <userId,User> should check how to initial all the activeStores into
        # dictionary
        self.__guests= None
        self.__members = None
        self.__systemManager = None
        self.__memberslock = threading.Lock()
        if UserManagment.__instance is None:
            UserManagment.__instance = self

    def checkOnlineUser(self, userId):
        self._initializeDict()
        self.thereIsSystemManger()
        if (self.__activeUsers.get(userId)) is None:
            raise NotOnlineException("The member " + str(userId) + " not online!")
        else:
            return True

    def getActiveUsers(self):
        self._initializeDict()
        self.thereIsSystemManger()
        return self.__activeUsers

    def getMembers(self):
        self._initializeDict()
        self.thereIsSystemManger()
        return self.__members

    def getActiveUser(self):
        self._initializeDict()
        self.thereIsSystemManger()
        return self.__activeUsers

    def getSystemManagers(self):
        self._initializeDict()
        self.thereIsSystemManger()
        return self.__systemManager

    def removeFromActiveUsers(self, userId):
        self._initializeDict()
        self.thereIsSystemManger()
        self.checkOnlineUser(userId)
        self.__activeUsers.pop(userId)

    def removeFromMembers(self, memberId):
        self._initializeDict()
        self.thereIsSystemManger()
        if memberId not in self.__members.keys():
            raise Exception("member: " + str(memberId) + " not exists")
        self.__members.pop(memberId)

    def enterSystem(self):
        self._initializeDict()
        self.thereIsSystemManger()
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
        self._initializeDict()
        self.thereIsSystemManger()
        self.checkOnlineUser(guestID)
        guest = self.__guests.get(guestID)
        self.__guests.pop(guestID)
        self.__activeUsers.pop(guestID)
        guest.removeUser()
        return True

    def memberSignUp(self, userName, password, phone, address, bank):  # Tested
        self._initializeDict()
        self.thereIsSystemManger()
        with self.__memberslock:
            if self.__isMemberExists(userName) is None:
                member = Member(userName, password, phone, address, bank)
                self.__members[member.getUserID()] = member
                # if User.get_user(userName) is None:
                #     User.save(username=userName, password=password)
                return True
        raise MemberAllReadyLoggedIn("user: " + userName + "is all ready loggedIn")

    def memberLogin(self, oldUserId, userName, password):  # Tested
        self._initializeDict()
        self.thereIsSystemManger()
        try:
            system_manager: SystemManager = self.__systemManager.get(userName)
            member: Member = self.__isMemberExists(userName)
            if member is None and system_manager is None:
                raise NoSuchUserException("The user ID " + userName + " not registered!")
            if system_manager is not None:
                if (self.__activeUsers.get(system_manager.getUserID())) is not None:
                    raise Exception("user is already logged-in!")
                if check_password(password, system_manager.getPassword()):
                    self.__activeUsers[system_manager.getUserID()] = system_manager
                    system_manager.setLoggedIn(True)
                    system_manager.setMemberCheck(True)
                    system_manager.loginUpdates()
                    system_manager.updateCart(self.__getUserCart(oldUserId))
                    return system_manager
            elif member is not None:
                if (self.__activeUsers.get(member.getUserID())) is not None:
                    raise Exception("user is already logged-in!")
                if check_password(password, member.getPassword()):
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
        self._initializeDict()
        self.thereIsSystemManger()
        for member in self.__members.values():
            if member.getMemberName() == userName:
                return member
        return None

    def systemManagerSignUp(self, userName, password, phone, address, bank):
        self._initializeDict()
        member = self.getUserByUserName(userName)
        if member is None:
            systemManager: SystemManager = SystemManager(userName, password, phone, address, bank)
        else:
            member.getModel().is_admin = True
            member.getModel().save()
            systemManager: SystemManager = SystemManager(model=member.getModel())
        if systemManager:
            self.__systemManager[userName] = systemManager
            return systemManager

    def removeSystemManger_forTests(self, systemMangerName):
        self._initializeDict()
        self.thereIsSystemManger()
        if self.__systemManager.get(systemMangerName) is None:
            raise Exception("user : " + systemMangerName + " is not a system manager")
        systemManger = self.__systemManager.get(systemMangerName)
        self.__systemManager.pop(systemMangerName)
        systemManger.removeUser()
        return True

    # from here is to move to user class
    def addProductToCart(self, userID, storeID, product, quantity):
        self._initializeDict()
        self.thereIsSystemManger()
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).addProductToCart(storeID, product, quantity)
        except Exception as e:
            raise Exception(e)

    def addProductToCartWithoutStore(self, userID, productID, quantity):
        self._initializeDict()
        self.thereIsSystemManger()
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).addProductToCartWithoutStore(productID, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromCart(self, userID, storeID, productId):
        self._initializeDict()
        self.thereIsSystemManger()
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).removeProductFromCart(storeID, productId)
        except Exception as e:
            raise Exception(e)

    def updateProductFromCart(self, userID, storeID, productId, quantity):
        self._initializeDict()
        self.thereIsSystemManger()
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).updateProductFromCart(storeID, productId, quantity)
        except Exception as e:
            raise Exception(e)

    def purchaseCart(self, userID, cardNumber, month, year, holderCardName, cvv, holderID, address=None):
        self._initializeDict()
        self.thereIsSystemManger()
        try:
            self.checkOnlineUser(userID)
            if address is not None:
                return self.__activeUsers.get(userID).purchaseCart(cardNumber, month, year, holderCardName, cvv,
                                                                   holderID, address)
            else:
                member = self.__members.get(userID)
                if member is None:
                    raise Exception("cannot purchase without an address!")
                return self.__activeUsers.get(userID).purchaseCart(cardNumber, month, year, holderCardName, cvv,
                                                                   holderID, member.getAddress())

        except Exception as e:
            raise Exception(e)

    def getCart(self, userID):
        self._initializeDict()
        self.thereIsSystemManger()
        try:
            self.checkOnlineUser(userID)
            return self.__activeUsers.get(userID).getCart()
        except Exception as e:
            raise Exception(e)

    def getSumAfterDiscount(self, userId):
        self._initializeDict()
        self.thereIsSystemManger()
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
        self._initializeDict()
        self.thereIsSystemManger()
        if userId not in self.__guests.keys():
            raise NoSuchUserException("user: " + str(userId) + "is not exists")
        return self.__guests.get(userId).getCart()

    def removeUserByUsername(self, username):
        self._initializeDict()
        self.thereIsSystemManger()
        for user in self.__members.values():
            if user.getMemberName() == username:
                user.removeUser()

    def getUser(self,uid):
        self._initializeDict()
        self.thereIsSystemManger()
        if uid not in self.__activeUsers:
            raise NoSuchUserException("user: " + str(uid) + "is not exists")
        return self.__activeUsers.get(uid)

    def getUserByUserName(self, username):
        self._initializeDict()
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

    def _buildMember(self, model):
        return Member(model=model)

    def _buildGuest(self, model):
        return Guest(model=model)

    def _buildSystemManager(self, model):
        return SystemManager(model=model)

    def thereIsSystemManger(self):
        if self.__systemManager != {} and self.__systemManager is not None:
            return True
        raise Exception("there is not system manger in this market!!")

    def _initializeDict(self):
        if self.__guests is None:
            self.__guests: Dict[str: User] = {}
            for guest_model in UserModel.objects.all():
                guest = self._buildGuest(guest_model)
                self.__guests.update({guest.getUserID() : guest})
        if self.__activeUsers is None:
            self.__activeUsers: Dict[str, User] = {}  # <userId,User> should check how to initial all the activeStores into dictionary
            for member_model in MemberModel.objects.filter(isLoggedIn=True):
                member = self._buildMember(member_model)
                self.__activeUsers.update({member.getUserID() : member})
        if self.__members is None:
            self.__members: Dict[str, Member] = {}
            for member_model in MemberModel.objects.all():
                member = self._buildMember(member_model)
                self.__members.update({member.getUserID() : member})
        if self.__systemManager is None:
            self.__systemManager: Dict[str, SystemManager] = {}
            for member_model in MemberModel.objects.filter(is_admin=True):
                member = self._buildSystemManager(member_model)
                self.__systemManager.update({member.getMemberName() : member})

    def removeAllUsers(self):
        UserModel.objects.all().delete()
        MemberModel.objects.all().delete()

    def resetManagement(self):
        self._initializeDict()
        # for guest in self.__guests.values():
        #     guest.getModel().delete()
        # for member in self.__activeUsers.values():
        #     member.getModel().delete()
        # for member in self.__members.values():
        #     member.getModel().delete()
        # for member in self.__systemManager.values():
        #     member.getModel().delete()

        self.__guests = None
        self.__activeUsers = None
        self.__members = None
        self.__systemManager = None


