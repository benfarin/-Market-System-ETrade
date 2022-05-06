from Business.Managment.UserManagment import UserManagment
from Business.UserPackage.Member import Member
from Business.Managment.MemberManagment import MemberManagment
from Exceptions.CustomExceptions import NoSuchMemberException
from Business.StorePackage.Product import Product
import threading


class RoleManagment:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if RoleManagment.__instance is None:
            RoleManagment()
        return RoleManagment.__instance

    def __init__(self):
        """ Virtually private constructor. """
        super().__init__()
        self.__memberManagement = MemberManagment.getInstance()
        self.__productId = 0
        self.__productId_lock = threading.Lock()
        if RoleManagment.__instance is None:
            RoleManagment.__instance = self

    def appointManagerToStore(self, storeID, assignerID, assigneeID):  # check if the asssignee he member and assignerID!!
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMembersFromUser().get(assigneeID)
            if assignerID not in self.__memberManagement.__members.keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            if assigneeID not in self.__memberManagement.__members.keys():
                raise NoSuchMemberException("user: " + str(assigneeID) + "is not a member")
            return assigner.appointManagerToStore(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def appointOwnerToStore(self, storeID, assignerID, assigneeID):  # check if the assignee he member and assignerID!!
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMembersFromUser().get(assigneeID)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            if assigneeID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assigneeID) + "is not a member")
            return assigner.appointOwnerToStore(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setStockManagerPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMembersFromUser().get(assigneeID)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            if assigneeID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assigneeID) + "is not a member")
            return assigner.setStockManagerPermission(storeID, assignee)
        except Exception as e:
            return e

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMembersFromUser().get(assigneeID)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            if assigneeID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assigneeID) + "is not a member")
            return assigner.setAppointOwnerPermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setChangePermission(self, storeID, assignerID, assigneeID):
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMembersFromUser().get(assigneeID)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            if assigneeID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assigneeID) + "is not a member")
            return assigner.setChangePermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setRolesInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMembersFromUser().get(assigneeID)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            if assigneeID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assigneeID) + "is not a member")
            return assigner.setRolesInformationPermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMembersFromUser().get(assigneeID)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            if assigneeID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assigneeID) + "is not a member")
            return assigner.setRolesInformationPermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def addProductToStore(self, storeID, userID, product):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            member.addProductToStore(storeID, product)
            return product.getProductId()
        except Exception as e:
            raise Exception(e)

    def addProductQuantityToStore(self, storeID, userID, productId, quantity):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.addProductQuantityToStore(storeID, productId, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromStore(self, storeID, userID, product):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.removeProductFromStore(storeID, product)
        except Exception as e:
            raise Exception(e)

    def updateProductPrice(self, storeID, userID, productId, newPrice):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.updateProductPrice(storeID, productId, newPrice)
        except Exception as e:
            raise Exception(e)

    def updateProductName(self, userID, storeID, productID, newName):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.updateProductPrice(storeID, productID, newName)
        except Exception as e:
            raise Exception(e)

    def updateProductCategory(self, userID, storeID, productID, newCategory):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.updateProductPrice(storeID, productID, newCategory)
        except Exception as e:
            raise Exception(e)

    def getRolesInformation(self, storeID, userID):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.getRolesInformation(storeID)
        except Exception as e:
            raise Exception(e)

    def getPurchaseHistoryInformation(self, storeID, userID):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.getPurchaseHistoryInformation(storeID)
        except Exception as e:
            raise Exception(e)

    def createProduct(self, name, price, category, keywords):
        if name is None:
            raise Exception("product name cannot be None")
        if category is None:
            raise Exception("product category cannot be None")
        return Product(self.__getProductId(), name, price, category, keywords)

    def __getProductId(self):
        with self.__productId_lock:
            productId = self.__productId
            self.__productId += 1
            return productId
