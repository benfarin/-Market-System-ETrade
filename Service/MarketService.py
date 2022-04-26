from Business.Managment.MarketManagment import MarketManage
from Business.Managment.RoleManagment import RoleManagment
from Service.Events.Events import Events
from Service.Events.EventLog import EventLog


class MarketService:
    def __init__(self):
        self.__marketManage = MarketManage()
        self.__roleManagment = RoleManagment()
        self.__events = Events()

    def getEvents(self):
        return self.__events

    def createStore(self, storeName, founderId, accountNumber, brunch, country, city, street, apartmentNum, zipCode):
        try:
            bank = self.__marketManage.createBankAcount(accountNumber, brunch)
            address = self.__marketManage.createAddress(country, city, street, apartmentNum, zipCode)
            self.__marketManage.createStore(storeName, founderId,bank, address)
            eventLog = EventLog("create store", "store name: " + storeName, "founderId: " + str(founderId),
                                "bankAccount: " + bank.printForEvents(), "address: " + address.printForEvents())
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def addProductToCart(self, userID, storeId, productId, quantity):
        try:
            self.__marketManage.addProductToCart(userID, storeId, productId, quantity)
            eventLog = EventLog("add product to cart", "userId: " + str(userID), "storeId: ", str(storeId),
                                "productId: " + productId, "quantity: " + str(quantity))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def removeProductFromCart(self, userId, storeId, productId):
        try:
            self.__marketManage.removeProductFromCart(userId, storeId, productId)
            eventLog = EventLog("remove product from cart", "userId: " + str(userId), "storeId: ", str(storeId),
                                "productId: " + productId)
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def updateProductFromCart(self, userID, storeID, productId, quantity):
        try:
            self.__marketManage.updateProductFromCart(userID, storeID, productId, quantity)
            eventLog = EventLog("update product from cart", "userId: " + str(userID), "storeId: ", str(storeID),
                                "productId: " + productId, "quantity: " + str(quantity))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def getProductByCategory(self, category):
        try:
            self.__marketManage.getProductByCategory(category)
            self.__events.addEventLog(EventLog("get product by category", "category: " + category))
            return True
        except Exception as e:
            return e

    def getProductsByName(self, nameProduct):
        try:
            self.__marketManage.getProductsByName(nameProduct)
            self.__events.addEventLog(EventLog("get product by name", "name: " + nameProduct))
            return True
        except Exception as e:
            return e

    def getProductByKeyword(self, keyword):
        try:
            self.__marketManage.getProductByKeyWord(keyword)
            self.__events.addEventLog(EventLog("get product by name", "keyword: " + keyword))
            return True
        except Exception as e:
            return e

    def getProductPriceRange(self, minPrice, highPrice):
        try:
            self.__marketManage.getProductPriceRange(minPrice, highPrice)
            self.__events.addEventLog(EventLog("get product by price range", "min price: " + minPrice,
                                               "high price: " + highPrice))
            return True
        except Exception as e:
            return e

    def purchaseCart(self, userID, accountNumber, branch):
        try:
            bank = self.__marketManage.createBankAcount(accountNumber, branch)
            self.__marketManage.purchaseCart(userID, bank)
            eventLog = EventLog("purchase cart", "userId: " + str(userID), "accountNumber: " + str(accountNumber)
                                , "branch: " + str(branch))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def appointManagerToStore(self, storeID, assignerID, assigneID):  # check if the asssigne he member and assignerID!!
        try:
            self.__roleManagment.appointManagerToStore(storeID, assignerID, assigneID)
            eventLog = EventLog("appoint manager to store", "storeId: " + str(storeID), "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneID))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def appointOwnerToStore(self, storeID, assignerID, assigneID):  # check if the asssigne he member and assignerID!!
        try:
            self.__roleManagment.appointOwnerToStore(storeID, assignerID, assigneID)
            eventLog = EventLog("appoint owner to store", "storeId: " + str(storeID), "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneID))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def setStockManagerPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__roleManagment.setStockManagerPermission(storeID, assignerID, assigneeID)
            eventLog = EventLog("set stock manager permission", "storeId: " + str(storeID),
                                "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneeID))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__roleManagment.setAppointOwnerPermission(storeID, assignerID, assigneeID)
            eventLog = EventLog("set appoint owner permission", "storeId: " + str(storeID),
                                "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneeID))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def setChangePermission(self, storeID, assignerID, assigneeID):
        try:
            self.__roleManagment.setChangePermission(storeID, assignerID, assigneeID)
            eventLog = EventLog("set change permissions", "storeId: " + str(storeID), "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneeID))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def setRolesInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__roleManagment.setRolesInformationPermission(storeID, assignerID, assigneeID)
            eventLog = EventLog("set roles info permission", "storeId: " + str(storeID),
                                "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneeID))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            self.__roleManagment.setPurchaseHistoryInformationPermission(storeID, assignerID, assigneeID)
            eventLog = EventLog("set purchase history info permission", "storeId: " + str(storeID),
                                "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneeID))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def addProductToStore(self, storeID, userID, name, price, category, keywords):
        try:
            product = self.__roleManagment.createProduct(name, price, category, keywords)
            self.__roleManagment.addProductToStore(storeID, userID, product)
            eventLog = EventLog("add product to store", "storeId: " + str(storeID), "userId: " + str(userID)
                                , "product: " + product.printForEvents())
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def addProductQuantityToStore(self, storeID, userID, productId, quantity):
        try:
            self.__roleManagment.addProductQuantityToStore(storeID, userID, productId, quantity)
            eventLog = EventLog("add product quantity to store", "storeId: " + str(storeID), "userId: " + str(userID)
                                , "productId: " + productId, "quantity: " + quantity)
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def removeProductFromStore(self, storeID, userID, productId):
        try:
            self.__roleManagment.removeProductFromStore(storeID, userID, productId)
            eventLog = EventLog("remove product from store", "storeId: " + str(storeID), "userId: " + str(userID)
                                , "productId: " + productId)
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def updateProductPriceFromStore(self, storeId, userId, productId, newPrice):
        try:
            self.__roleManagment.updateProductPriceFromStore(storeId, userId, productId, newPrice)
            eventLog = EventLog("update product price from store", "storeId: " + str(storeId), "userId: " + str(userId),
                                "productId: " + str(productId), "new price: " + str(newPrice))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def PrintRolesInformation(self, storeID, userID):
        try:
            self.__roleManagment.PrintRolesInformation(storeID, userID)
            eventLog = EventLog("print roles info", "storeId: " + str(storeID), "userId: " + str(userID))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e

    def printPurchaseHistoryInformation(self, storeID, userID):
        try:
            self.__roleManagment.printPurchaseHistoryInformation(storeID, userID)
            eventLog = EventLog("print purchase history info", "storeId: " + str(storeID), "userId: " + str(userID))
            self.__events.addEventLog(eventLog)
            return True
        except Exception as e:
            return e
