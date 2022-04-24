from interfaces.IMarket import IMarket
from Business.Market import Market


def singleton_dec(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton_dec
class RoleManagment:

    def __init__(self):
        self.__market: IMarket = Market()

    def appointManagerToStore(self, storeID, assignerID, assigneeID):  # check if the asssignee he member and assignerID!!
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
            if self.checkOnlineMember(assignerID) is not None:
                self.__stores.get(storeID).setAppointManagerPermission(assignerID, assigneeID)
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

    def addProductToStore(self, storeID, userID, product):
        try:
            return self.__market.addProductToStore(storeID, userID, product)
        except Exception as e:
            raise Exception(e)

    def updateProductFromStore(self, storeId, userID, productId, newProduct):
        try:
            return self.__market.updateProductFromStore(storeId, userID, productId, newProduct)
        except Exception as e:
            raise Exception(e)

    def addProductQuantityToStore(self, storeID, userID, product, quantity):
        try:
            return self.__market.addProductQuantityToStore(storeID, userID, product, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromStore(self, storeID, userID, product):
        try:
            return self.__market.removeProductFromStore(storeID, userID, product)
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




