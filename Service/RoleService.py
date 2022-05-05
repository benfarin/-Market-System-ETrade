from Business.Managment.MemberManagment import MemberManagment
from Business.Managment.RoleManagment import RoleManagment
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')


class RoleService:

    def __init__(self):
        self.__marketManage = MemberManagment.getInstance()
        self.__roleManagment = RoleManagment.getInstance()

    def appointManagerToStore(self, storeID, assignerID, assigneID):  # check if the asssigne he member and assignerID!!
        try:
            self.__roleManagment.appointManagerToStore(storeID, assignerID, assigneID)
            logging.info("success to appoint manager to store " + str(storeID))
            return True
        except Exception as e:
            logging.error("Failed to appoint " + str(assigneID) + " as manager")
            return e

    def appointOwnerToStore(self, storeID, assignerID, assigneID):  # check if the asssigne he member and assignerID!!
        try:
            self.__roleManagment.appointOwnerToStore(storeID, assignerID, assigneID)
            logging.info("success to appoint owner to store " + str(storeID))
            return True
        except Exception as e:
            logging.error("Failed to appoint " + str(assigneID) + " as owner")
            return e

    def setStockManagerPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__roleManagment.setStockManagerPermission(storeID, assignerID, assigneeID)
            logging.info("success to set stock manager permission in store " + str(storeID))
            return True
        except Exception as e:
            logging.error("Failed to set permissions to user " + str(assigneeID))
            return e

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__roleManagment.setAppointOwnerPermission(storeID, assignerID, assigneeID)
            logging.info("success to set owner permission in store " + str(storeID))
            return True
        except Exception as e:
            logging.error("Failed to set permissions to user " + str(assigneeID))
            return e

    def setChangePermission(self, storeID, assignerID, assigneeID):
        try:
            self.__roleManagment.setChangePermission(storeID, assignerID, assigneeID)
            logging.info("success to change permission in store " + str(storeID) + "for user " + str(assigneeID))
            return True
        except Exception as e:
            logging.error("Failed to set permissions to user " + str(assigneeID))
            return e

    def setRolesInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__roleManagment.setRolesInformationPermission(storeID, assignerID, assigneeID)
            return True
        except Exception as e:
            logging.error("Failed to set permissions to user " + str(assigneeID))
            return e

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__roleManagment.setPurchaseHistoryInformationPermission(storeID, assignerID, assigneeID)
            return True
        except Exception as e:
            logging.error("Failed to set permissions to user " + str(assigneeID))
            return e

    def addProductToStore(self, storeID, userID, name, price, category, keywords):
        try:
            product = self.__roleManagment.createProduct(name, price, category, keywords)
            self.__roleManagment.addProductToStore(storeID, userID, product)
            logging.info("success to add product " + name + "to store " + str(storeID))
            return product
        except Exception as e:
            logging.error("Failed to add new product to store " + str(storeID))
            return e

    def addProductQuantityToStore(self, storeID, userID, productId, quantity):
        try:
            self.__roleManagment.addProductQuantityToStore(storeID, userID, productId, quantity)
            logging.info(
                "success to add " + str(quantity) + "units for product " + str(productId) + "to store " + str(storeID))
            return True
        except Exception as e:
            logging.error("Failed to add product quantity in store " + str(storeID))
            return e

    def removeProductFromStore(self, storeID, userID, productId):
        try:
            self.__roleManagment.removeProductFromStore(storeID, userID, productId)
            logging.info("success to remove product " + str(productId) + "from store " + str(storeID))
            return True
        except Exception as e:
            logging.error("Failed to remove product " + str(productId) + " in store " + str(storeID))
            return e

    def PrintRolesInformation(self, storeID, userID):
        try:
            toReturn = self.__roleManagment.PrintRolesInformation(storeID, userID)
            return toReturn
        except Exception as e:
            logging.error("Failed to print roles information for store " + str(storeID))
            return e

    def printPurchaseHistoryInformation(self, storeID, userID):
        try:
            toReturn = self.__roleManagment.printPurchaseHistoryInformation(storeID, userID)
            return toReturn
        except Exception as e:
            logging.error("Failed to print purchase history information for store " + str(storeID))
            return e

    def updateProductPrice(self, storeID, userID, productId, newPrice):
        try:
            self.__roleManagment.updateProductPrice(storeID, userID, productId, newPrice)
            logging.info("success to update product " + str(productId) + "to price " + str(newPrice))
            return True
        except Exception as e:
            logging.error("Failed to update price for product " + str(productId) + "in store " + str(storeID))
            return e

    def updateProductName(self, userID, storeID, productID, newName):
        try:
            self.__roleManagment.updateProductPrice(storeID, userID, productID, newName)
            logging.info("success to update product " + str(productID) + "to name " + newName)
            return True
        except Exception as e:
            logging.error("Failed to update name for product " + str(productID) + "in store " + str(storeID))
            return e

    def updateProductCategory(self, userID, storeID, productID, newCategory):
        try:
            self.__roleManagment.updateProductPrice(storeID, userID, productID, newCategory)
            logging.info("success to update product " + str(productID) + "to category " + newCategory)
            return True
        except Exception as e:
            logging.error("Failed to update category for product " + str(productID) + "in store " + str(storeID))
            return e

