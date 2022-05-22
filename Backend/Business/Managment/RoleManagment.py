import sys
from datetime import datetime

from Backend.Business.DiscountPackage.DiscountInfo import DiscountInfo
from Backend.Business.DiscountPackage.DiscountManagement import DiscountManagement
from Backend.Business.DiscountRules import DiscountRules, ruleType
from Backend.Business.Rules.ruleCreator import ruleCreator
from Backend.Business.DiscountPackage.Discount import Discount
from Backend.Business.Managment.UserManagment import UserManagment
from Backend.Business.UserPackage.Member import Member
from Backend.Business.Managment.MemberManagment import MemberManagment
from Backend.Exceptions.CustomExceptions import NoSuchMemberException, NoSuchStoreException, ComplexDiscountException
from Backend.Business.StorePackage.Product import Product
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
        self.__discountRules = DiscountRules()
        self.__discountManager = DiscountManagement()
        self.__memberManagement = MemberManagment.getInstance()
        self.rule_creator = ruleCreator.getInstance()
        self.__rules = {}
        self.__productId = 0
        self.__discountId = 0
        self.__ruleId = 0
        self.__productId_lock = threading.Lock()
        self.__discountId_lock = threading.Lock()
        self.__ruleId_lock = threading.Lock()
        if RoleManagment.__instance is None:
            RoleManagment.__instance = self

    def appointManagerToStore(self, storeID, assignerID,
                              assigneeName):  # check if the asssignee he member and assignerID!!
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

    def updateProductWeight(self, userID, storeID, productID, newWeight):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userID)
            member = self.__memberManagement.getMembersFromUser().get(userID)
            if userID not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userID) + "is not a member")
            return member.updateProductWeight(storeID, productID, newWeight)
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

    def createProduct(self, userId, storeId, name, price, category, weight, keywords):
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
        self.__memberManagement.checkOnlineUserFromUser(userId)
        member = self.__memberManagement.getMembersFromUser().get(userId)
        if userId not in self.__memberManagement.getMembersFromUser().keys():
            raise NoSuchMemberException("user: " + str(userId) + "is not a member")
        try:
            return member.getUserStores()
        except Exception as e:
            raise Exception(e)

    def removeStoreOwner(self, storeId, assignerId, assigneeName):
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
            return True
        except Exception as e:
            raise Exception(e)

    def getAllStoreTransactions(self, systemManagerName):
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getAllStoreTransactions()
        except Exception as e:
            raise Exception(e)

    def getAllUserTransactions(self, systemManagerName):
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getAllUserTransactions()
        except Exception as e:
            raise Exception(e)

    def getStoreTransaction(self, systemManagerName, transactionId):
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getStoreTransaction(transactionId)
        except Exception as e:
            raise Exception(e)

    def getUserTransaction(self, systemManagerName, transactionId):
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getUserTransaction(transactionId)
        except Exception as e:
            raise Exception(e)

    def getStoreTransactionByStoreId(self, systemManagerName, storeId):
        try:
            system_manager = self.__memberManagement.getSystemManagers().get(systemManagerName)
            self.__memberManagement.checkOnlineUserFromUser(system_manager.getUserID())
            if system_manager is None:
                raise Exception("user: " + str(systemManagerName) + " is not a system manager")
            return system_manager.getStoreTransactionByStoreId(storeId)
        except Exception as e:
            raise Exception(e)

    def addSimpleDiscount(self, userId, storeId, ruleContext, ruleType, precent, category, productId,
                          value_less_than, value_grather_than):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            discountId = self.__getDiscountId()
            discount = self.__discountRules.createSimpleDiscount(discountId, ruleContext, precent,
                                                                 category, productId)

            discountInfo = DiscountInfo(discountId, userId, storeId, ruleContext, ruleType, precent, category,
                                        productId, value_less_than, value_grather_than)
            self.__discountManager.addDiscount(discountInfo)

            member.addDiscount(storeId, discount)
            return discountId

        except Exception as e:
            raise Exception(e)

    def addSimpleCondDiscount(self, userId, storeId, ruleContext, ruleType, precent, category, productId,
                          value_less_than, value_grather_than):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            discountId = self.__getDiscountId()
            rId = self.__getRuleId()
            discount = self.__discountRules.createConditionalDiscount(rId, storeId, discountId, ruleContext, ruleType, precent,
                                                                        category, productId, value_less_than, value_grather_than)

            discountInfo = DiscountInfo(discountId, userId, storeId, ruleContext, ruleType, precent, category,
                                        productId, value_less_than, value_grather_than)
            self.__discountManager.addDiscount(discountInfo)

            member.addDiscount(storeId, discount)
            return discountId

        except Exception as e:
            raise Exception(e)

    def removeDiscount(self, userId, storeId, discountId):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            member.removeDiscount(storeId, discountId)
            return True

        except Exception as e:
            raise Exception(e)

    def addConditionDiscountAdd(self, userId, storeId, dId1, dId2):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            discountId = self.__getDiscountId()
            member.addConditionDiscountAdd(storeId, discountId, dId1, dId2)

            return discountId

        except Exception as e:
            raise Exception(e)

    def addConditionDiscountMax(self, userId, storeId, dId1, dId2):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            discountId = self.__getDiscountId()
            member.addConditionDiscountMax(storeId, discountId, dId1, dId2)

            return discountId

        except Exception as e:
            raise Exception(e)

    def addConditionDiscountXor(self, userId, storeId, dId, pred1_id, pred2_id, decide):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            discountId = self.__getDiscountId()
            pred1 = self.__rules.get(pred1_id)
            pred2 = self.__rules.get(pred2_id)
            if pred1 is None:
                raise Exception("first rule doesnt exists")
            if pred2 is None:
                raise Exception("second rule doesnt exists")
            member.addConditionDiscountXor(storeId, discountId, dId, pred1, pred2, decide)

            return discountId

        except Exception as e:
            raise Exception(e)

    def addConditionDiscountAnd(self, userId, storeId, dId, pred1_id, pred2_id):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            discountId = self.__getDiscountId()
            pred1 = self.__rules.get(pred1_id)
            pred2 = self.__rules.get(pred2_id)
            if pred1 is None:
                raise Exception("first rule doesnt exists")
            if pred2 is None:
                raise Exception("second rule doesnt exists")
            member.addConditionDiscountAnd(storeId, discountId, dId, pred1, pred2)

            return discountId

        except Exception as e:
            raise Exception(e)

    def addConditionDiscountOr(self, userId, storeId, dId, pred1_id, pred2_id):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            discountId = self.__getDiscountId()
            pred1 = self.__rules.get(pred1_id)
            pred2 = self.__rules.get(pred2_id)
            if pred1 is None:
                raise Exception("first rule doesnt exists")
            if pred2 is None:
                raise Exception("second rule doesnt exists")
            member.addConditionDiscountOr(storeId, discountId, dId, pred1, pred2)

            return discountId

        except Exception as e:
            raise Exception(e)

    def __getProductId(self):
        with self.__productId_lock:
            pId = self.__productId
            self.__productId += 1
            return pId

    def __getDiscountId(self):
        with self.__discountId_lock:
            dId = self.__discountId
            self.__discountId += 1
            return dId

    def __getRuleId(self):
        with self.__ruleId_lock:
            rId = self.__ruleId
            self.__ruleId += 1
            return rId

    def createStoreWeightRule(self, userId, storeId, less_than, bigger_than):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            if member.hasDiscountPermission(storeId):
                rId = self.__getRuleId()
                rule = self.rule_creator.createStoreWeightRule(rId, storeId, less_than, bigger_than)
                self.__rules[rId] = rule
                return [rId, rule]
            else:
                raise Exception("user: " + member.getUserID() + " doesnt have the permission to add a rule")
        except Exception as e:
            raise Exception(e)

    def createProductWeightRule(self, userId, storeId, pid, less_than, bigger_than):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            if member.hasDiscountPermission(storeId):
                rId = self.__getRuleId()
                rule = self.rule_creator.createProductWeightRule(rId, pid, storeId, less_than, bigger_than)
                self.__rules[rId] = rule
                return [rId, rule]
            else:
                raise Exception("user: " + member.getUserID() + " doesnt have the permission to add a rule")
        except Exception as e:
            raise Exception(e)

    def createStoreQuantityRule(self, userId, storeId, less_than, bigger_than):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            if member.hasDiscountPermission(storeId):
                rId = self.__getRuleId()
                rule = self.rule_creator.createStoreQuantityRule(rId, storeId, less_than, bigger_than)
                self.__rules[rId] = rule
                return [rId, rule]
            else:
                raise Exception("user: " + member.getUserID() + " doesnt have the permission to add a rule")
        except Exception as e:
            raise Exception(e)

    def createCategoryRule(self, userId, storeId, category, less_than, bigger_than):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            if member.hasDiscountPermission(storeId):
                rId = self.__getRuleId()
                rule = self.rule_creator.createCategoryRule(rId, storeId, category, less_than, bigger_than)
                self.__rules[rId] = rule
                return [rId, rule]
            else:
                raise Exception("user: " + member.getUserID() + " doesnt have the permission to add a rule")
        except Exception as e:
            raise Exception(e)

    def createProductRule(self, userId, storeId, pid, less_than, bigger_than):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            if member.hasDiscountPermission(storeId):
                rId = self.__getRuleId()
                rule = self.rule_creator.createProductRule(rId, storeId, pid, less_than, bigger_than)
                self.__rules[rId] = rule
                return [rId, rule]
            else:
                raise Exception("user: " + member.getUserID() + " doesnt have the permission to add a rule")
        except Exception as e:
            raise Exception(e)

    def createStoreTotalAmountRule(self, userId, storeId, less_than, bigger_than):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            if member.hasDiscountPermission(storeId):
                rId = self.__getRuleId()
                rule = self.rule_creator.createStorePriceRule(rId, storeId, less_than, bigger_than)
                self.__rules[rId] = rule
                return [rId, rule]
            else:
                raise Exception("user: " + member.getUserID() + " doesnt have the permission to add a rule")
        except Exception as e:
            raise Exception(e)

    def getAllRules(self, userId, storeId):
        try:
            self.__memberManagement.checkOnlineUserFromUser(userId)
            member = self.__memberManagement.getMembersFromUser().get(userId)
            if userId not in self.__memberManagement.getMembersFromUser().keys():
                raise NoSuchMemberException("user: " + str(userId) + "is not a member")
            if not member.isStoreExists(storeId):
                raise NoSuchStoreException("store: " + str(storeId) + "is not exists in the market")

            if member.hasDiscountPermission(storeId):
                return self.__rules
            else:
                raise Exception("user: " + member.getUserID() + " doesnt have the permission to add a rule")
        except Exception as e:
            raise Exception(e)