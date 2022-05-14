import sys
from datetime import datetime

from Business.DiscountPackage.DiscountInfo import DiscountInfo
from Business.DiscountPackage.DiscountManagement import DiscountManagement
from Business.DiscountRules import DiscountRules, ruleType
from Business.Managment.MemberManagment import MemberManagment
from Business.Managment.RoleManagment import RoleManagment
from Business.Managment.GetterManagment import GetterManagment
from Exceptions.CustomExceptions import NoSuchStoreException
from Service.Response import Response
from Service.DTO.storeTransactionDTO import storeTransactionDTO
from Service.DTO.StorePermissionDTO import StorePermissionDTO
from Service.DTO.userTransactionDTO import userTransactionDTO
from Service.DTO.StoreDTO import StoreDTO
from Service.DTO.ProductDTO import ProductDTO
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

    def addProductToStore(self, storeID, userID, name, price, category, keywords):
        try:
            product = self.__roleManagment.createProduct(userID, storeID, name, price, category, keywords)
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
            transactions = self.__roleManagment.printPurchaseHistoryInformation(storeID, userID)
            logging.info("success to get purchase history info from store" + str(storeID))

            transactionsDTOs = []
            for transaction in transactions:
                transactionsDTOs.append(storeTransactionDTO(transaction))
            return Response(transactionsDTOs)
        except Exception as e:
            logging.error("Failed to print purchase history information for store " + str(storeID))
            return Response(e.__str__())

    def updateProductPrice(self, storeID, userID, productId, newPrice):
        try:
            product = self.__roleManagment.updateProductPrice(storeID, userID, productId, newPrice)
            logging.info("success to update product " + str(productId) + "to price " + str(newPrice))
            return Response(ProductDTO(product))
        except Exception as e:
            logging.error("Failed to update price for product " + str(productId) + "in store " + str(storeID))
            return Response(e.__str__())

    def updateProductName(self, userID, storeID, productID, newName):
        try:
            product = self.__roleManagment.updateProductPrice(storeID, userID, productID, newName)
            logging.info("success to update product " + str(productID) + "to name " + newName)
            return Response(ProductDTO(product))
        except Exception as e:
            logging.error("Failed to update name for product " + str(productID) + "in store " + str(storeID))
            return Response(e.__str__())

    def updateProductCategory(self, userID, storeID, productID, newCategory):
        try:
            product = self.__roleManagment.updateProductPrice(storeID, userID, productID, newCategory)
            logging.info("success to update product " + str(productID) + "to category " + newCategory)
            return Response(ProductDTO(product))
        except Exception as e:
            logging.error("Failed to update category for product " + str(productID) + "in store " + str(storeID))
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

    def addSimpleDiscount(self, userId,storeId,ruleContext,discountPercentage, catagory, productId):
        try:
            discount = self.__roleManagment.addSimpleDiscount(userId,self.getStore(storeId).getData(), ruleContext , discountPercentage,catagory,productId)
            logging.info("success to get user Transaction " + str(discount))
            return Response(discount)
        except Exception as e:
            logging.error("Failed to make discount! ")
            return Response(e.__str__())

    def updateDiscount(self,existsDiscount,userId,storeId,ruleContext,discountPercentage, catagory, productId):
        try:

            discountId = self.__roleManagment.updateDiscount(existsDiscount,userId, self.getStore(storeId).getData(), ruleContext,
                                                                discountPercentage, catagory, productId)
            logging.info("success to get user Transaction " + str(discountId))
            return Response(discountId)
        except Exception as e:
            logging.error("Failed to make discount! ")
            return Response(e.__str__())

    def removeDiscount(self,userId, storeId, discountId):
        try:
            discountId = self.__roleManagment.removeDiscount(userId, storeId, discountId)
            logging.info("success to get user Transaction " + str(discountId))
            return Response(discountId)
        except Exception as e:
            logging.error("Failed to make discount! ")
            return Response(e.__str__())
