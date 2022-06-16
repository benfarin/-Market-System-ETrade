import os, django
import sys
import datetime

from django.db.models import Max
from Backend.Business.Market import Market
from Backend.Interfaces.IMarket import IMarket

from ModelsBackend.models import ProductModel, DiscountModel, RuleModel, LoginDateModel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frontend.settings')
django.setup()

from Backend.Business.Discounts.CategoryDiscount import CategoryDiscount
from Backend.Business.Discounts.DiscountComposite import DiscountComposite
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.Discounts.StoreDiscount import StoreDiscount
from Backend.Business.Managment.UserManagment import UserManagment
from Backend.Business.UserPackage.Member import Member
from Backend.Business.Managment.MemberManagment import MemberManagment
from Backend.Exceptions.CustomExceptions import NoSuchMemberException, NoSuchStoreException, ComplexDiscountException
from Backend.Business.StorePackage.Product import Product
from Backend.Business.Rules.PriceRule import PriceRule
from Backend.Business.Rules.WeightRule import weightRule
from Backend.Business.Rules.QuantityRule import quantityRule
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
        self.__market: IMarket = Market().getInstance()
        self.__memberManagement = MemberManagment.getInstance()
        self.__productId = None
        self.__discountId = None
        self.__ruleId = None
        self.__productId_lock = threading.Lock()
        self.__discountId_lock = threading.Lock()
        self.__ruleId_lock = threading.Lock()
        if RoleManagment.__instance is None:
            RoleManagment.__instance = self

    def appointManagerToStore(self, storeID, assignerID,
                              assigneeName):  # check if the asssignee he member and assignerID!!
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembers().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.appointManagerToStore(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def appointOwnerToStore(self, storeID, assignerID,
                            assigneeName):  # check if the assignee he member and assignerID!!
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.appointOwnerToStore(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setStockManagerPermission(self, storeID, assignerID, assigneeName):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.setStockManagerPermission(storeID, assignee)
        except Exception as e:
            return e

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeName):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.setAppointOwnerPermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setChangePermission(self, storeID, assignerID, assigneeName):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.setChangePermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setRolesInformationPermission(self, storeID, assignerID, assigneeName):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.setRolesInformationPermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeName):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.setRolesInformationPermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def setDiscountPermission(self, storeID, assignerID, assigneeName):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerID)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerID)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(assignerID) + "is not a member")
            return assigner.setDiscountPermission(storeID, assignee)
        except Exception as e:
            raise Exception(e)

    def addProductToStore(self, storeID, userID, product):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if storeID < 0:
                raise NoSuchStoreException("The store id " + storeID + " is not illegal!")
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            member.addProductToStore(storeID, product)
            return product.getProductId()
        except Exception as e:
            raise Exception(e)

    def addProductQuantityToStore(self, storeID, userID, productId, quantity):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.addProductQuantityToStore(storeID, productId, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromStore(self, storeID, userID, product):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.removeProductFromStore(storeID, product)
        except Exception as e:
            raise Exception(e)

    def updateProductPrice(self, userID, storeID, productId, newPrice):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.updateProductPrice(storeID, productId, newPrice)
        except Exception as e:
            raise Exception(e)

    def updateProductName(self, userID, storeID, productID, newName):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.updateProductName(storeID, productID, newName)
        except Exception as e:
            raise Exception(e)

    def updateProductCategory(self, userID, storeID, productID, newCategory):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.updateProductCategory(storeID, productID, newCategory)
        except Exception as e:
            raise Exception(e)

    def updateProductWeight(self, userID, storeID, productID, newWeight):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.updateProductWeight(storeID, productID, newWeight)
        except Exception as e:
            raise Exception(e)

    def getRolesInformation(self, storeID, userID):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.getRolesInformation(storeID)
        except Exception as e:
            raise Exception(e)

    def getPurchaseHistoryInformation(self, storeID, userID):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.getPurchaseHistoryInformation(storeID)
        except Exception as e:
            raise Exception(e)

    def createProduct(self, userId, storeId, name, price, category, weight, keywords):
        self.__memberManagement.thereIsSystemManger()
        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if name is None:
            raise Exception("product name cannot be None")
        if price < 0:
            raise Exception("product cannot have a non positive price")
        if category is None:
            raise Exception("product category cannot be None")
        if weight < 0:
            raise Exception("product cannot have a non positive weight")
        return Product(self.__getProductId(), storeId, name, price, category, weight, keywords)

    def getUserStores(self, userId):
        self.__memberManagement.thereIsSystemManger()
        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        try:
            return member.getUserStores()
        except Exception as e:
            raise Exception(e)

    def removeStoreOwner(self, storeId, assignerId, assigneeName):
        self.__memberManagement.thereIsSystemManger()
        try:
            self.__memberManagement.checkOnlineUserFromUser(assignerId)
            assigner = self.__memberManagement.getMembersFromUser().get(assignerId)
            assignee = self.__memberManagement.getMemberByName(assigneeName)
            if assignerId not in self.__memberManagement.getMembers().keys():
                raise NoSuchMemberException("user: " + str(assignerId) + "is not a member")
            return assigner.removeStoreOwner(storeId, assignee)
        except Exception as e:
            raise Exception(e)

    def removeMember(self, systemManagerName, memberName):
        self.__memberManagement.thereIsSystemManger()
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            member = self.__memberManagement.getMemberByName(memberName)
            if member not in self.__memberManagement.getMembers().values():
                raise NoSuchMemberException("user: " + str(member.getUserID()) + "is not a member")
            if member.hasRole():
                raise Exception("cannot remove member with a role")
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")

            if self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID()):
                self.__memberManagement.removeFromMembers(member.getUserID())
                member.removeUser()
                for memberLogIn in LoginDateModel.objects.filter(username=memberName):
                    memberLogIn.delete()
            return True
        except Exception as e:
            raise Exception(e)

    def getAllActiveUsers(self, systemManagerName):
        self.__memberManagement.thereIsSystemManger()
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            return self.__memberManagement.getActiveUsers().values()
        except Exception as e:
            raise Exception(e)

    def getAllStoreTransactions(self, systemManagerName):
        self.__memberManagement.thereIsSystemManger()
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getAllStoreTransactions()
        except Exception as e:
            raise Exception(e)

    def getAllUserTransactions(self, systemManagerName):
        self.__memberManagement.thereIsSystemManger()
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getAllUserTransactions()
        except Exception as e:
            raise Exception(e)

    def getStoreTransaction(self, systemManagerName, transactionId):
        self.__memberManagement.thereIsSystemManger()
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getStoreTransaction(transactionId)
        except Exception as e:
            raise Exception(e)

    def getUserTransaction(self, systemManagerName, transactionId):
        self.__memberManagement.thereIsSystemManger()
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getUserTransaction(transactionId)
        except Exception as e:
            raise Exception(e)

    def getStoreTransactionByStoreId(self, systemManagerName, storeId):
        self.__memberManagement.thereIsSystemManger()
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getStoreTransactionByStoreId(storeId)
        except Exception as e:
            raise Exception(e)

    def addStoreDiscount(self, userId, storeId, percent):
        self.__memberManagement.thereIsSystemManger()

        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add disconts")
        discount = StoreDiscount(self.__getDiscountId(), percent)
        member.addSimpleDiscount(storeId, discount)
        return discount

    def addProductDiscount(self, userId, storeId, productId, percent):
        self.__memberManagement.thereIsSystemManger()

        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add disconts")
        discount = ProductDiscount(self.__getDiscountId(), productId, percent)
        member.addSimpleDiscount(storeId, discount)
        return discount

    def addCategoryDiscount(self, userId, storeId, category, percent):
        self.__memberManagement.thereIsSystemManger()

        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add disconts")
        discount = CategoryDiscount(self.__getDiscountId(), category, percent)
        member.addSimpleDiscount(storeId, discount)
        return discount

    def addCompositeDiscount(self, userId, storeId, dId1, dId2, discountType, decide):
        self.__memberManagement.thereIsSystemManger()

        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add disconts")
        return member.addCompositeDiscount(storeId, self.__getDiscountId(), dId1, dId2, discountType, decide)

    def removeDiscount(self, userId, storeId, discountId):
        self.__memberManagement.thereIsSystemManger()

        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add disconts")
        return member.removeDiscount(storeId, discountId)

    def addPriceRule(self, userId, storeId, discountId, atLeast, atMost, ruleKind):
        self.__memberManagement.thereIsSystemManger()

        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add disconts")

        rule = PriceRule(self.__getRuleId(), 'Store', None, atLeast, atMost, ruleKind)
        member.addSimpleRule(storeId, discountId, rule)
        return rule

    def addQuantityRule(self, userId, storeId, discountId, ruleType, filterType, atLeast, atMost, ruleKind):
        self.__memberManagement.thereIsSystemManger()

        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add disconts")

        rule = quantityRule(self.__getRuleId(), ruleType, filterType, atLeast, atMost, ruleKind)
        member.addSimpleRule(storeId, discountId, rule)
        return rule

    def addWeightRule(self, userId, storeId, discountId, ruleType, filterType, atLeast, atMost, ruleKind):
        self.__memberManagement.thereIsSystemManger()

        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add disconts")

        rule = weightRule(self.__getRuleId(), ruleType, filterType, atLeast, atMost, ruleKind)
        member.addSimpleRule(storeId, discountId, rule)
        return rule

    def addCompositeRule(self, userId, storeId, dId, rId1, rId2, ruleType, ruleKind):
        self.__memberManagement.thereIsSystemManger()

        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add discuonts")
        return member.addCompositeRule(storeId, dId, self.__getRuleId(), rId1, rId2, ruleType, ruleKind)

    def removeRule(self, userId, storeId, dId, rId, ruleKind):
        self.__memberManagement.thereIsSystemManger()

        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add discounts")
        return member.removeRule(storeId, dId, rId, ruleKind)

    def getAllDiscountOfStore(self, userId, storeId, isComp):
        self.__memberManagement.thereIsSystemManger()
        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add discounts")
        return member.getAllDiscountOfStore(storeId, isComp)

    def getAllPurchaseRulesOfStore(self, userId, storeId, isComp):
        self.__memberManagement.thereIsSystemManger()
        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add discounts")
        return member.getAllPurchaseRulesOfStore(storeId, isComp)

    def getAllRulesOfDiscount(self, userId, storeId, discountId, isComp):
        self.__memberManagement.thereIsSystemManger()
        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        if not member.isStoreExists(storeId):
            raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")
        if not member.hasDiscountPermission(storeId):
            raise Exception("member does not have the permission to add discounts")
        return member.getAllRulesOfDiscount(storeId, discountId, isComp)

    def acceptBidOffer(self, userID, storeID, bID):
        self.__memberManagement.thereIsSystemManger()
        self.__memberManagement.checkOnlineUserFromUser(userID)
        try:
            return self.__memberManagement.getMembersFromUser().get(userID).acceptBidOffer(storeID, bID)
        except Exception as e:
            raise Exception(e)

    def rejectOffer(self, userID, storeID, bID):
        self.__memberManagement.thereIsSystemManger()
        self.__memberManagement.checkOnlineUserFromUser(userID)
        try:
            return self.__memberManagement.getMembersFromUser().get(userID).rejectOffer(storeID, bID)
        except Exception as e:
            raise Exception(e)

    def offerAlternatePrice(self, userID, storeID, bID, new_price):
        self.__memberManagement.thereIsSystemManger()
        self.__memberManagement.checkOnlineUserFromUser(userID)
        try:
            return self.__memberManagement.getMembersFromUser().get(userID).offerAlternatePrice(storeID, bID, new_price)
        except Exception as e:
            raise Exception(e)

    def __getAllMembersByDates(self, fromDate, untilDate):
        members = []
        for userLogInModel in LoginDateModel.objects.filter(username__isnull=False,
                                                            date__gte=fromDate, date__lte=untilDate):
            member = self.__memberManagement.getMemberByName(userLogInModel.username)
            if member is None:  # the member can be system managers
                member = self.__memberManagement.getSystemManagers().get(userLogInModel.username)
            members.append(member)
        return members

    def __getAllGuestByDates(self, fromDate, untilDate):
        guests = []
        for userLogInModel in LoginDateModel.objects.filter(username=None,
                                                            date__gte=fromDate, date__lte=untilDate):
            guests.append(userLogInModel.userID)
        return guests

    def getUsersByDates(self, systemMangerName, fromDate, untilDate):
        self.__memberManagement.thereIsSystemManger()
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemMangerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())

            datesForGraph = {}
            fromDate = datetime.datetime(fromDate.year, fromDate.month, fromDate.day)
            untilDate = datetime.datetime(untilDate.year, untilDate.month, untilDate.day)
            while fromDate <= untilDate:
                loginDateRecords = {}
                guests = self.__getAllGuestByDates(fromDate, fromDate + datetime.timedelta(days=1))
                members = self.__getAllMembersByDates(fromDate, fromDate + datetime.timedelta(days=1))

                loginDateRecords[0] = guests  # guests
                loginDateRecords[1] = []      # regular members
                loginDateRecords[2] = []      # just managers
                loginDateRecords[3] = []      # just owners
                loginDateRecords[4] = []      # system managers

                for member in members:
                    if self.__memberManagement.getSystemManagers().get(member.getMemberName()) is not None:
                        loginDateRecords[4].append(member.getMemberName())
                    elif member.getCheckNoOwnerNoManage():
                        loginDateRecords[1].append(member.getMemberName())
                    elif member.getCheckNoOwnerYesManage():
                        loginDateRecords[2].append(member.getMemberName())
                    elif member.getCheckOwner():
                        loginDateRecords[3].append(member.getMemberName())

                datesForGraph[fromDate] = loginDateRecords
                fromDate += datetime.timedelta(days=1)
            return datesForGraph
        except Exception as e:
            raise Exception(e)

    def changeExternalPayment(self, systemManagerName, paymentSystem):
        self.__memberManagement.thereIsSystemManger()
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return self.__market.changeExternalPayment(paymentSystem)
        except Exception as e:
            raise Exception(e)

    def changeExternalDelivery(self,systemManagerName ,deliverySystem):
        self.__memberManagement.thereIsSystemManger()
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return self.__market.changeExternalDelivery(deliverySystem)
        except Exception as e:
            raise Exception(e)

    def __getProductId(self):
        if self.__productId is None:
            self.__productId = ProductModel.objects.aggregate(Max('product_id'))['product_id__max']
            if self.__productId is None:
                self.__productId = 0
            else:
                self.__productId += 1
        pId = self.__productId
        self.__productId += 1
        return pId

    def __getDiscountId(self):
        if self.__discountId is None:
            self.__discountId = DiscountModel.objects.aggregate(Max('discountID'))[
                'discountID__max']
            if self.__discountId is None:
                self.__discountId = 0
            else:
                self.__discountId += 1
        dId = self.__discountId
        self.__discountId += 1
        return dId

    def __getRuleId(self):
        if self.__ruleId is None:
            self.__ruleId = RuleModel.objects.aggregate(Max('ruleID'))[
                'ruleID__max']
            if self.__ruleId is None:
                self.__ruleId = 0
            else:
                self.__ruleId += 1
        rId = self.__ruleId
        self.__ruleId += 1
        return rId
