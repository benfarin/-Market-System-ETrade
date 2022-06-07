import sys
from datetime import datetime
import django, os

from Backend.Service.DTO.GuestDTO import GuestDTO

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frontend.settings')
django.setup()
from Backend.Business.Managment.MemberManagment import MemberManagment
from Backend.Business.Managment.RoleManagment import RoleManagment
from Backend.Business.Managment.GetterManagment import GetterManagment
from Backend.Exceptions.CustomExceptions import NoSuchStoreException
from Backend.Service.DTO.CompositeDiscountDTO import compositeDiscountDTO
from Backend.Service.DTO.CompositeRuleDTO import CompositeRuleDTO
from Backend.Service.DTO.SimpleDiscountDTO import simpleDiscountDTO
from Backend.Service.Response import Response
from Backend.Service.DTO.StoreTransactionDTO import storeTransactionDTO
from Backend.Service.DTO.StorePermissionDTO import StorePermissionDTO
from Backend.Service.DTO.UserTransactionDTO import userTransactionDTO
from Backend.Service.DTO.StoreDTO import StoreDTO
from Backend.Service.DTO.ProductDTO import ProductDTO
from Backend.Service.DTO.RuleDTO import RuleDTO
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class RoleService:

    def __init__(self):

        self.__marketManage = MemberManagment.getInstance()
        self.__roleManagment = RoleManagment.getInstance()
        self.__getterManagment = GetterManagment.getInstance()

    def appointManagerToStore(self, storeID, assignerID,
                              assigneeName):  # check if the asssigne he member and assignerID!!
        try:
            isAppointed = self.__roleManagment.appointManagerToStore(storeID, assignerID, assigneeName)
            logging.info("success to appoint manager to store " + str(storeID))
            return Response(isAppointed)
        except Exception as e:
            logging.error("Failed to appoint " + str(assigneeName) + " as manager")
            return Response(e.__str__())

    def appointOwnerToStore(self, storeID, assignerID,
                            assigneeName):  # check if the asssigne he member and assignerID!!
        try:
            isAppointed = self.__roleManagment.appointOwnerToStore(storeID, assignerID, assigneeName)
            logging.info("success to appoint owner to store " + str(storeID))
            return Response(isAppointed)
        except Exception as e:
            logging.error("Failed to appoint " + str(assigneeName) + " as owner")
            return Response(e.__str__())

    def setStockManagerPermission(self, storeID, assignerID, assigneeName):
        try:
            isSet = self.__roleManagment.setStockManagerPermission(storeID, assignerID, assigneeName)
            logging.info("success to set stock manager permission in store " + str(storeID))
            return Response(isSet)
        except Exception as e:
            logging.error("Failed to set permissions to user " + str(assigneeName))
            return Response(e.__str__())

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeName):
        try:
            isSet = self.__roleManagment.setAppointOwnerPermission(storeID, assignerID, assigneeName)
            logging.info("success to set owner permission in store " + str(storeID))
            return Response(isSet)
        except Exception as e:
            logging.error("Failed to set permissions to user " + str(assigneeName))
            return Response(e.__str__())

    def setChangePermission(self, storeID, assignerID, assigneeName):
        try:
            isSet = self.__roleManagment.setChangePermission(storeID, assignerID, assigneeName)
            logging.info("success to change permission in store " + str(storeID) + "for user " + str(assigneeName))
            return Response(isSet)
        except Exception as e:
            logging.error("Failed to set permissions to user " + str(assigneeName))
            return Response(e.__str__())

    def setRolesInformationPermission(self, storeID, assignerID, assigneeName):
        try:
            isSet = self.__roleManagment.setRolesInformationPermission(storeID, assignerID, assigneeName)
            logging.info(
                "success to set role info permission in store " + str(storeID) + "for user " + str(assigneeName))
            return Response(isSet)
        except Exception as e:
            logging.error("Failed to set permissions to user " + str(assigneeName))
            return Response(e.__str__())

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeName):
        try:
            isSet = self.__roleManagment.setPurchaseHistoryInformationPermission(storeID, assignerID, assigneeName)
            logging.info("success to set purchase history info permission in store " + str(storeID) +
                         "for user " + str(assigneeName))
            return Response(isSet)
        except Exception as e:
            logging.error("Failed to set permissions to user " + str(assigneeName))
            return Response(e.__str__())

    def setDiscountPermission(self, storeID, assignerID, assigneeName):
        try:
            isSet = self.__roleManagment.setDiscountPermission(storeID, assignerID, assigneeName)
            logging.info("success to set discount permission in store " + str(storeID) +
                         "for user " + str(assigneeName))
            return Response(isSet)
        except Exception as e:
            logging.error("Failed to set discount permission to user " + str(assigneeName))
            return Response(e.__str__())

    def addProductToStore(self, storeID, userID, name, price, category, weight, keywords):
        try:
            product = self.__roleManagment.createProduct(userID, storeID, name, price, category, weight, keywords)
            self.__roleManagment.addProductToStore(storeID, userID, product)
            logging.info("success to add product " + name + "to store " + str(storeID))
            return Response(ProductDTO(product))
        except Exception as e:
            logging.error("Failed to add new product to store " + str(storeID))
            return Response(e.__str__())

    def addProductQuantityToStore(self, storeID, userID, productId, quantity):
        try:
            isAdded = self.__roleManagment.addProductQuantityToStore(storeID, userID, productId, quantity)
            logging.info(
                "success to add " + str(quantity) + "units for product " + str(productId) + "to store " + str(storeID))
            return Response(isAdded)
        except Exception as e:
            logging.error("Failed to add product quantity in store " + str(storeID))
            return Response(e.__str__())

    def removeProductFromStore(self, storeID, userID, productId):
        try:
            isRemoved = self.__roleManagment.removeProductFromStore(storeID, userID, productId)
            logging.info("success to remove product " + str(productId) + "from store " + str(storeID))
            return Response(isRemoved)
        except Exception as e:
            logging.error("Failed to remove product " + str(productId) + " in store " + str(storeID))
            return Response(e.__str__())

    def getRolesInformation(self, storeID, userID):
        try:
            permissions = self.__roleManagment.getRolesInformation(storeID, userID)
            logging.info("success to get role info from store" + str(storeID))
            permissionsDTOs = []
            for permission in permissions:
                permissionsDTOs.append(StorePermissionDTO(permission))
            return Response(permissionsDTOs)
        except Exception as e:
            logging.error("Failed to print roles information for store " + str(storeID))
            return Response(e.__str__())

    def getPurchaseHistoryInformation(self, storeID, userID):
        try:
            transactions = self.__roleManagment.getPurchaseHistoryInformation(storeID, userID)
            logging.info("success to get purchase history info from store" + str(storeID))

            transactionsDTOs = []
            for transaction in transactions.values():
                transactionsDTOs.append(storeTransactionDTO(transaction))
            return Response(transactionsDTOs)
        except Exception as e:
            logging.error("Failed to print purchase history information for store " + str(storeID))
            return Response(e.__str__())

    def updateProductPrice(self, userID, storeID, productId, newPrice):
        try:
            product = self.__roleManagment.updateProductPrice(userID, storeID, productId, newPrice)
            logging.info("success to update product " + str(productId) + "to price " + str(newPrice))
            return Response(ProductDTO(product))
        except Exception as e:
            logging.error("Failed to update price for product " + str(productId) + "in store " + str(storeID))
            return Response(e.__str__())

    def updateProductName(self, userID, storeID, productID, newName):
        try:
            product = self.__roleManagment.updateProductName(userID, storeID, productID, newName)
            logging.info("success to update product " + str(productID) + "to name " + newName)
            return Response(ProductDTO(product))
        except Exception as e:
            logging.error("Failed to update name for product " + str(productID) + "in store " + str(storeID))
            return Response(e.__str__())

    def updateProductCategory(self, userID, storeID, productID, newCategory):
        try:
            product = self.__roleManagment.updateProductCategory(userID, storeID, productID, newCategory)
            logging.info("success to update product " + str(productID) + "to category " + newCategory)
            return Response(ProductDTO(product))
        except Exception as e:
            logging.error("Failed to update category for product " + str(productID) + "in store " + str(storeID))
            return Response(e.__str__())

    def updateProductWeight(self, userID, storeID, productID, newWeight):
        try:
            product = self.__roleManagment.updateProductWeight(userID, storeID, productID, newWeight)
            logging.info("success to update product " + str(productID) + "to weight " + str(newWeight))
            return Response(ProductDTO(product))
        except Exception as e:
            logging.error("Failed to update weight for product " + str(productID) + "in store " + str(storeID))
            return Response(e.__str__())

    def getStore(self, storeId):
        try:
            if storeId < 0:
                raise NoSuchStoreException("There no store id: " + str(storeId))
            store = self.__getterManagment.getStore(storeId)
            logging.info("get store " + str(storeId))
            return Response(StoreDTO(store))
        except Exception as e:
            logging.error("Failed to get store " + str(storeId))
            return Response(e.__str__())

    def getUserStores(self, userId):
        try:
            stores = self.__roleManagment.getUserStores(userId)
            logging.info("get all stores of user")

            allUserStoresDTO = []
            for store in stores:
                allUserStoresDTO.append(StoreDTO(store))

            return Response(allUserStoresDTO)
        except Exception as e:
            logging.error("Failed to get all stores of user")
            return Response(e.__str__())

    def getAllStores(self):
        try:
            stores = self.__getterManagment.getAllStores()
            logging.info("get all stores ")

            allStoresDTO = []
            for store in stores:
                allStoresDTO.append(StoreDTO(store))

            return Response(allStoresDTO)
        except Exception as e:
            logging.error("Failed to get all stores ")
            return Response(e.__str__())

    def removeStoreOwner(self, storeId, assignerId, assigneeName):
        try:
            isRemoved = self.__roleManagment.removeStoreOwner(storeId, assignerId, assigneeName)
            logging.info("success to remove owner to store " + str(storeId))
            return Response(isRemoved)
        except Exception as e:
            logging.error("Failed to remove " + str(assigneeName) + " as owner")
            return Response(e.__str__())

    # actions of system manager
    def removeMember(self, systemManagerName, memberName):
        try:
            isRemoved = self.__roleManagment.removeMember(systemManagerName, memberName)
            logging.info("success to remove member " + str(memberName))
            return Response(isRemoved)
        except Exception as e:
            logging.error("Failed to remove member" + str(memberName))
            return Response(e.__str__())

    def getAllActiveUsers(self, systemManagerName):
        try:
            allActiveUsers = self.__roleManagment.getAllActiveUsers(systemManagerName)
            logging.info("success to get all active users ")
            users = []
            for user in allActiveUsers:
                users.append(GuestDTO(user))
            return Response(users)
        except Exception as e:
            logging.error("Failed  to get all active users ")
            return Response(e.__str__())

    def getAllStoreTransactions(self, systemManagerName):
        try:
            storeTransactions = self.__roleManagment.getAllStoreTransactions(systemManagerName)
            logging.info("success to get all store transactions " + str(systemManagerName))

            DTOstoreTransactuions = []
            for st in storeTransactions:
                DTOstoreTransactuions.append(storeTransactionDTO(st))

            return Response(DTOstoreTransactuions)
        except Exception as e:
            logging.error("Failed to get all store transactions" + str(systemManagerName))
            return Response(e.__str__())

    def getAllUserTransactions(self, systemManagerName):
        try:
            userTransactions = self.__roleManagment.getAllUserTransactions(systemManagerName)
            logging.info("success to get all store transactions " + str(systemManagerName))

            DTOuserTransactuions = []
            for ut in userTransactions:
                DTOuserTransactuions.append(userTransactionDTO(ut))

            return Response(DTOuserTransactuions)
        except Exception as e:
            logging.error("Failed to get all store transactions" + str(systemManagerName))
            return Response(e.__str__())

    def getStoreTransaction(self, systemManagerName, transactionId):
        try:
            storeTransaction = self.__roleManagment.getStoreTransaction(systemManagerName, transactionId)
            logging.info("success to get store Transaction " + str(transactionId))
            return Response(storeTransactionDTO(storeTransaction))
        except Exception as e:
            logging.error("Failed to get store transaction " + str(transactionId))
            return Response(e.__str__())

    def getUserTransaction(self, systemManagerName, transactionId):
        try:
            userTransaction = self.__roleManagment.getUserTransaction(systemManagerName, transactionId)
            logging.info("success to get user Transaction " + str(transactionId))
            return Response(userTransactionDTO(userTransaction))
        except Exception as e:
            logging.error("Failed to get user transaction " + str(transactionId))
            return Response(e.__str__())

    def getStoreTransactionByStoreId(self, systemManagerName, storeId):
        try:
            storeTransactions = self.__roleManagment.getStoreTransactionByStoreId(systemManagerName, storeId)
            logging.info("success to get store Transaction by store id" + str(storeId))

            DTOstoreTransactions = []
            for st in storeTransactions:
                DTOstoreTransactions.append(storeTransactionDTO(st))

            return Response(DTOstoreTransactions)
        except Exception as e:
            logging.error("Failed to get store transaction by id " + str(self))
            return Response(e.__str__())

    def addStoreDiscount(self, userId, storeId, percent):
        try:
            simpleDis = self.__roleManagment.addStoreDiscount(userId, storeId, percent)
            logging.info("success to create store discount to store id " + str(storeId))
            return Response(simpleDiscountDTO(simpleDis))
        except Exception as e:
            logging.error("Failed to make store discount to store id " + str(storeId))
            return Response(e.__str__())

    def addProductDiscount(self, userId, storeId, productId, percent):
        try:
            simpleDis = self.__roleManagment.addProductDiscount(userId, storeId, productId, percent)
            logging.info("success to create product discount to product id " + str(productId))
            return Response(simpleDiscountDTO(simpleDis))
        except Exception as e:
            logging.error("Failed to make product discount to product id " + str(productId))
            return Response(e.__str__())

    def addCategoryDiscount(self, userId, storeId, category, percent):
        try:
            simpleDis = self.__roleManagment.addCategoryDiscount(userId, storeId, category, percent)
            logging.info("success to create category discount to category id " + str(category))
            return Response(simpleDiscountDTO(simpleDis))
        except Exception as e:
            logging.error("Failed to make category discount to category id " + str(category))
            return Response(e.__str__())

    def addCompositeDiscountMax(self, userId, storeId, dId1, dId2):
        try:
            simpleDis = self.__roleManagment.addCompositeDiscount(userId, storeId, dId1, dId2, 'Max', None)
            logging.info(
                "success to create MAX discount to discount id " + str(dId1) + " and to discount id " + str(dId2))
            return Response(compositeDiscountDTO(simpleDis))
        except Exception as e:
            logging.error(
                "Failed to make MAX discount to discount id " + str(dId1) + " and to discount id " + str(dId2))
            return Response(e.__str__())

    def addCompositeDiscountAdd(self, userId, storeId, dId1, dId2):
        try:
            simpleDis = self.__roleManagment.addCompositeDiscount(userId, storeId, dId1, dId2, 'Add', None)
            logging.info(
                "success to create ADD discount to discount id " + str(dId1) + " and to discount id " + str(dId2))
            return Response(compositeDiscountDTO(simpleDis))
        except Exception as e:
            logging.error(
                "Failed to make ADD discount to discount id " + str(dId1) + " and to discount id " + str(dId2))
            return Response(e.__str__())

    # if both of the discount are valid, the decide is the tie-breaker
    # decide = 1 -> dId1, decide = 2 -> dId2
    def addCompositeDiscountXor(self, userId, storeId, dId1, dId2, decide):
        try:
            simpleDis = self.__roleManagment.addCompositeDiscount(userId, storeId, dId1, dId2, 'XOR', decide)
            logging.info(
                "success to create XOR discount to discount id " + str(dId1) + " and to discount id " + str(dId2))
            return Response(compositeDiscountDTO(simpleDis))
        except Exception as e:
            logging.error(
                "Failed to make XOR discount to discount id " + str(dId1) + " and to discount id " + str(dId2))
            return Response(e.__str__())

    def removeDiscount(self, userId, storeId, discountId):
        try:
            isRemoved = self.__roleManagment.removeDiscount(userId, storeId, discountId)
            logging.info("success to remove discount id " + str(discountId))
            return Response(isRemoved)
        except Exception as e:
            logging.error("Failed to remove discount id " + str(discountId))
            return Response(e.__str__())

    # discount rules
    def addStoreTotalAmountDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        try:
            rule = self.__roleManagment.addPriceRule(userId, storeId, discountId, atLeast, atMost, 'Discount')
            logging.info("success to add price rule to store, with discount id " + str(discountId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add price rule to store, with discount id " + str(discountId))
            return Response(e.__str__())

    def addStoreQuantityDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        try:
            rule = self.__roleManagment.addQuantityRule(userId, storeId, discountId, 'Store', None, atLeast,
                                                        atMost, 'Discount')
            logging.info("success to add quantity store rule, with discount id " + str(discountId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add price quantity store rule, with discount id " + str(discountId))
            return Response(e.__str__())

    def addCategoryQuantityDiscountRule(self, userId, storeId, discountId, category, atLeast, atMost):
        try:
            rule = self.__roleManagment.addQuantityRule(userId, storeId, discountId, 'Category', category, atLeast,
                                                        atMost, 'Discount')
            logging.info("success to add quantity category rule, with discount id " + str(discountId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add price quantity category store, with discount id " + str(discountId))
            return Response(e.__str__())

    def addProductQuantityDiscountRule(self, userId, storeId, discountId, productId, atLeast, atMost):
        try:
            rule = self.__roleManagment.addQuantityRule(userId, storeId, discountId, 'Product', productId, atLeast,
                                                        atMost, 'Discount')
            logging.info("success to add quantity product rule, with discount id " + str(discountId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add price quantity product store, with discount id " + str(discountId))
            return Response(e.__str__())

    def addStoreWeightDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        try:
            rule = self.__roleManagment.addWeightRule(userId, storeId, discountId, 'Store', None, atLeast,
                                                      atMost, 'Discount')
            logging.info("success to add weight store rule, with discount id " + str(discountId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add weight store  product store, with discount id " + str(discountId))
            return Response(e.__str__())

    def addCategoryWeightDiscountRule(self, userId, storeId, discountId, category, atLeast, atMost):
        try:
            rule = self.__roleManagment.addWeightRule(userId, storeId, discountId, 'Category', category, atLeast,
                                                      atMost, 'Discount')
            logging.info("success to add weight category rule, with discount id " + str(discountId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add weight category product store, with discount id " + str(discountId))
            return Response(e.__str__())

    def addProductWeightDiscountRule(self, userId, storeId, discountId, productId, atLeast, atMost):
        try:
            rule = self.__roleManagment.addWeightRule(userId, storeId, discountId, 'Product', productId, atLeast,
                                                      atMost, 'Discount')
            logging.info("success to add weight product rule, with discount id " + str(discountId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add weight product product store, with discount id " + str(discountId))
            return Response(e.__str__())

    def addCompositeRuleDiscountAnd(self, userId, storeId, dId, rId1, rId2):
        try:
            rule = self.__roleManagment.addCompositeRule(userId, storeId, dId, rId1, rId2, 'And', 'Discount')
            logging.info("success to add composite AND rule, with discount id " + str(dId))
            return Response(CompositeRuleDTO(rule))
        except Exception as e:
            logging.info("failed to add composite AND rule, with discount id " + str(dId))
            return Response(e.__str__())

    def addCompositeRuleDiscountOr(self, userId, storeId, dId, rId1, rId2):
        try:
            rule = self.__roleManagment.addCompositeRule(userId, storeId, dId, rId1, rId2, 'Or', 'Discount')
            logging.info("success to add composite OR rule, with discount id " + str(dId))
            return Response(CompositeRuleDTO(rule))
        except Exception as e:
            logging.info("failed to add composite OR rule, with discount id " + str(dId))
            return Response(e.__str__())

    def removeRuleDiscount(self, userId, storeId, dId, rId):
        try:
            isRemoved = self.__roleManagment.removeRule(userId, storeId, dId, rId, 'Discount')
            logging.info("success to remove rule, with rule id " + str(rId))
            return Response(isRemoved)
        except Exception as e:
            logging.info("failed to remove rule, with rule id " + str(rId))
            return Response(e.__str__())

    # purchase rules
    def addStoreTotalAmountPurchaseRule(self, userId, storeId, atLeast, atMost):
        try:
            rule = self.__roleManagment.addPriceRule(userId, storeId, None, atLeast, atMost, 'Purchase')
            logging.info("success to add purchase price rule to store: " + str(storeId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("Failed to add purchase price rule to store: " + str(storeId))
            return Response(e.__str__())

    def addStoreQuantityPurchaseRule(self, userId, storeId, atLeast, atMost):
        try:
            rule = self.__roleManagment.addQuantityRule(userId, storeId, None, 'Store', None, atLeast,
                                                        atMost, 'Purchase')
            logging.info("success to add store purchase quantity rule to store: " + str(storeId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add store purchase quantity rule to store: " + str(storeId))
            return Response(e.__str__())

    def addCategoryQuantityPurchaseRule(self, userId, storeId, category, atLeast, atMost):
        try:
            rule = self.__roleManagment.addQuantityRule(userId, storeId, None, 'Category', category, atLeast,
                                                        atMost, 'Purchase')
            logging.info("success to add category purchase quantity rule to store: " + str(storeId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add category purchase quantity rule to store: " + str(storeId))
            return Response(e.__str__())

    def addProductQuantityPurchaseRule(self, userId, storeId, productId, atLeast, atMost):
        try:
            rule = self.__roleManagment.addQuantityRule(userId, storeId, None, 'Product', productId, atLeast,
                                                        atMost, 'Purchase')
            logging.info("success to add product purchase quantity rule to store: " + str(storeId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add product purchase quantity rule to store: " + str(storeId))
            return Response(e.__str__())

    def addStoreWeightPurchaseRule(self, userId, storeId, atLeast, atMost):
        try:
            rule = self.__roleManagment.addWeightRule(userId, storeId, None, 'Store', None, atLeast,
                                                      atMost, 'Purchase')
            logging.info("success to add store purchase weight rule to store: " + str(storeId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add store purchase weight rule to store: " + str(storeId))
            return Response(e.__str__())

    def addCategoryWeightPurchaseRule(self, userId, storeId, category, atLeast, atMost):
        try:
            rule = self.__roleManagment.addWeightRule(userId, storeId, None, 'Category', category, atLeast,
                                                      atMost, 'Purchase')
            logging.info("success to add category purchase weight rule to store: " + str(storeId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add category purchase weight rule to store: " + str(storeId))
            return Response(e.__str__())

    def addProductWeightPurchaseRule(self, userId, storeId, productId, atLeast, atMost):
        try:
            rule = self.__roleManagment.addWeightRule(userId, storeId, None, 'Product', productId, atLeast,
                                                      atMost, 'Purchase')
            logging.info("success to add product purchase weight rule to store: " + str(storeId))
            return Response(RuleDTO(rule.getRuleId()))
        except Exception as e:
            logging.info("failed to add product purchase weight rule to store: " + str(storeId))
            return Response(e.__str__())

    def addCompositeRulePurchaseAnd(self, userId, storeId, rId1, rId2):
        try:
            rule = self.__roleManagment.addCompositeRule(userId, storeId, None, rId1, rId2, 'And', 'Purchase')
            logging.info("success to add composite purchase rule AND to store: " + str(storeId))
            return Response(CompositeRuleDTO(rule))
        except Exception as e:
            logging.info("failed to add composite purchase rule AND to store: " + str(storeId))
            return Response(e.__str__())

    def addCompositeRulePurchaseOr(self, userId, storeId, rId1, rId2):
        try:
            rule = self.__roleManagment.addCompositeRule(userId, storeId, None, rId1, rId2, 'Or', 'Purchase')
            logging.info("success to add composite purchase rule OR to store: " + str(storeId))
            return Response(CompositeRuleDTO(rule))
        except Exception as e:
            logging.info("failed to add composite purchase rule OR to store: " + str(storeId))
            return Response(e.__str__())

    def removeRulePurchase(self, userId, storeId, rId):
        try:
            isRemoved = self.__roleManagment.removeRule(userId, storeId, None, rId, 'Purchase')
            logging.info("success to remove purchase rule, with rule id " + str(rId))
            return Response(isRemoved)
        except Exception as e:
            logging.info("failed to remove purchase rule, with rule id " + str(rId))
            return Response(e.__str__())

    def getAllSimpleDiscountOfStore(self, userId, storeId):
        try:
            discounts = self.__roleManagment.getAllDiscountOfStore(userId, storeId, False)
            discountsDTOs = []
            for discount in discounts:
                discountsDTOs.append(simpleDiscountDTO(discount))
            logging.info("success to get all simple discounts of store: " + str(storeId))
            return Response(discountsDTOs)
        except Exception as e:
            logging.info("failed to get all composite discounts of store: " + str(storeId))
            return Response(e.__str__())

    def getAllCompositeDiscountOfStore(self, userId, storeId):
        try:
            discounts = self.__roleManagment.getAllDiscountOfStore(userId, storeId, True)
            discountsDTOs = []
            for discount in discounts:
                discountsDTOs.append(compositeDiscountDTO(discount))
            logging.info("success to get all composite discounts of store: " + str(storeId))
            return Response(discountsDTOs)
        except Exception as e:
            logging.info("failed to get all composite discounts of store: " + str(storeId))
            return Response(e.__str__())

    def getAllSimplePurchaseRulesOfStore(self, userId, storeId):
        try:
            rules = self.__roleManagment.getAllPurchaseRulesOfStore(userId, storeId, False)
            rulesDTOs = []
            for rule in rules:
                rulesDTOs.append(RuleDTO(rule))
            logging.info("success to get all simple purchase rules of store: " + str(storeId))
            return Response(rulesDTOs)
        except Exception as e:
            logging.info("failed to get all simple purchase rules of store: " + str(storeId))
            return Response(e.__str__())

    def getAllCompositePurchaseRulesOfStore(self, userId, storeId):
        try:
            rules = self.__roleManagment.getAllPurchaseRulesOfStore(userId, storeId, True)
            rulesDTOs = []
            for rule in rules:
                rulesDTOs.append(CompositeRuleDTO(rule))
            logging.info("success to get all composite purchase rules of store: " + str(storeId))
            return Response(rulesDTOs)
        except Exception as e:
            logging.info("failed to get all composite purchase rules of store: " + str(storeId))
            return Response(e.__str__())

    def getAllSimpleRulesOfDiscount(self, userId, storeId, discountId):
        try:
            rules = self.__roleManagment.getAllRulesOfDiscount(userId, storeId, discountId, False)
            rulesDTOs = []
            for rule in rules:
                rulesDTOs.append(RuleDTO(rule))
            logging.info("success to get all simple discount rules of store: " + str(storeId))
            return Response(rulesDTOs)
        except Exception as e:
            logging.info("failed to get all simple discount rules of store: " + str(storeId))
            return Response(e.__str__())

    def getAllCompositeRulesOfDiscount(self, userId, storeId, discountId):
        try:
            rules = self.__roleManagment.getAllRulesOfDiscount(userId, storeId, discountId, True)
            rulesDTOs = []
            for rule in rules:
                rulesDTOs.append(CompositeRuleDTO(rule))
            logging.info("success to get all simple discount rules of store: " + str(storeId))
            return Response(rulesDTOs)
        except Exception as e:
            logging.info("failed to get all simple discount rules of store: " + str(storeId))
            return Response(e.__str__())
