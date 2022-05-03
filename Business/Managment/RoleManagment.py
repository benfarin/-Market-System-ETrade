from interfaces.IMarket import IMarket
from Business.Market import Market
from Business.StorePackage.Product import Product
import threading


class RoleManagment():
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if RoleManagment.__instance is None:
            RoleManagment()
        return RoleManagment.__instance

    def __init__(self):
        """ Virtually private constructor. """
        self.__market: IMarket = Market().getInstance()
        self.__productId = 0
        self.__productId_lock = threading.Lock()
        if RoleManagment.__instance is None:
            RoleManagment.__instance = self

    def appointManagerToStore(self, storeID, assignerID,
                              assigneeID):  # check if the asssignee he member and assignerID!!
        try:
            return self.__market.appointManagerToStore(storeID, assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def appointOwnerToStore(self, storeID, assignerID, assigneeID):  # check if the assignee he member and assignerID!!
        try:
            return self.__market.appointOwnerToStore(storeID, assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def setStockManagerPermission(self, storeID, assignerID, assigneeID):
        try:
            return self.setStockManagerPermission(storeID, assignerID, assigneeID)
        except Exception as e:
            return e

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeID):
        try:
            return self.__market.setAppointOwnerPermission(storeID, assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def setChangePermission(self, storeID, assignerID, assigneeID):
        try:
            return self.__market.setChangePermission(storeID, assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def setRolesInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            return self.__market.setRolesInformationPermission(storeID, assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            return self.__market.setRolesInformationPermission(storeID, assignerID, assigneeID)
        except Exception as e:
            raise Exception(e)

    def createProduct(self, name, price, category, keywords):
        if name is None:
            raise Exception("product name cannot be None")
        if category is None:
            raise Exception("product category cannot be None")
        return Product(self.__getProductId(), name, price, category, keywords)

    def addProductToStore(self, storeID, userID, product):
        try:
            self.__market.addProductToStore(storeID, userID, product)
            return product.getProductId()
        except Exception as e:
            raise Exception(e)

    def addProductQuantityToStore(self, storeID, userID, productId, quantity):
        try:
            return self.__market.addProductQuantityToStore(storeID, userID, productId, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromStore(self, storeID, userID, product):
        try:
            return self.__market.removeProductFromStore(storeID, userID, product)
        except Exception as e:
            raise Exception(e)

    def updateProductPrice(self, storeID, userID, productId, newPrice):
        try:
            return self.__market.updateProductPrice(storeID, userID, productId, newPrice)
        except Exception as e:
            raise Exception(e)

    def updateProductName(self, userID, storeID, productID, newName):
        try:
            return self.__market.updateProductPrice(storeID, userID, productID, newName)
        except Exception as e:
            raise Exception(e)

    def updateProductCategory(self, userID, storeID, productID, newCategory):
        try:
            return self.__market.updateProductPriceFromStore(storeID, userID, productID, newCategory)
        except Exception as e:
            raise Exception(e)

    def PrintRolesInformation(self, storeID, userID):
        try:
            return self.__market.printRolesInformation(storeID, userID)
        except Exception as e:
            raise Exception(e)

    def printPurchaseHistoryInformation(self, storeID, userID):
        try:
            return self.__market.printPurchaseHistoryInformation(storeID, userID)
        except Exception as e:
            raise Exception(e)

    def __getProductId(self):
        with self.__productId_lock:
            productId = self.__productId
            self.__productId += 1
            return productId
