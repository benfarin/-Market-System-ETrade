from Business.Managment.MarketManagment import MarketManage
from Service.Events.Events import Events
from Service.Events.EventLog import EventLog
from interfaces import IMarket


class MarketService:
    def __init__(self):
        self.__market: IMarket = MarketManage()
        self.__events = Events()

    def getEvents(self):
        return self.__events

    def addGuest(self):
        try:
            self.__market.addGuest()
            self.__events.addEventLog(EventLog("add guest"))
        except Exception as e:
            return e  # maybe need to print, need to talk about it

    def addProductToCart(self, userID, storeId, product, quantity):
        try:
            toReturn = self.__market.addProductToCart(userID, storeId, product, quantity)
            eventLog = EventLog("add product to cart", "userId: " + str(userID), "storeId: ", str(storeId),
                                "product: " + product.printForEvents(), "quantity: " + str(quantity))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def removeProductFromCart(self, userId, storeId, product):
        try:
            toReturn = self.__market.removeProductFromCart(userId, storeId, product)
            eventLog = EventLog("remove product from cart", "userId: " + str(userId), "storeId: ", str(storeId),
                                "product: " + product.printForEvents())
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def updateProductFromCart(self, userID, storeID, product, quantity):
        try:
            toReturn = self.__market.updateProductFromCart(userID, storeID, product, quantity)
            eventLog = EventLog("update product from cart", "userId: " + str(userID), "storeId: ", str(storeID),
                                "product: " + product.printForEvents(), "quantity: " + str(quantity))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def getStoreByName(self, store_name):
        try:
            toReturn = self.__market.getStoreByName(store_name)
            self.__events.addEventLog(EventLog("get store by name", "storeName: " + store_name))
            return toReturn
        except Exception as e:
            return e

    def getStoreById(self, id_store):  # maybe should be private
        try:
            toReturn = self.__market.getStoreById(id_store)
            self.__events.addEventLog(EventLog("get store by Id", "store Id: " + str(id_store)))
            return toReturn
        except Exception as e:
            return e

    def getProductByCategory(self, category):
        try:
            toReturn = self.__market.getProductByCatagory(category)
            self.__events.addEventLog(EventLog("get product by category", "category: " + category))
            return toReturn
        except Exception as e:
            return e

    def getProductsByName(self, nameProduct):
        try:
            toReturn = self.__market.getProductsByName(nameProduct)
            self.__events.addEventLog(EventLog("get product by name", "name: " + nameProduct))
            return toReturn
        except Exception as e:
            return e

    def getProductByKeyword(self, keyword):
        try:
            toReturn = self.__market.getProductByKeyWord(keyword)
            self.__events.addEventLog(EventLog("get product by name", "keyword: " + keyword))
            return toReturn
        except Exception as e:
            return e

    def getUserByName(self, userName):
        try:
            toReturn = self.__market.getUserByName(userName)
            self.__events.addEventLog(EventLog("get user by name", "name: " + userName))
            return toReturn
        except Exception as e:
            return e

    def createStore(self, storeName, founderId, bankAccount, address):
        try:
            toReturn = self.__market.createStore(storeName, founderId, bankAccount, address)
            eventLog = EventLog("create store", "store name: " + storeName, "founderId: " + str(founderId),
                                "bankAccount: " + bankAccount.printForEvents(), "address: " + address.printForEvents())
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def addMember(self, userID, password, phone, address, bank):
        try:
            toReturn = self.__market.addMember(userID, password, phone, address, bank)
            eventLog = EventLog("add member", "userId: " + str(userID), "password: " + password, "phone: " + phone,
                                "address: " + address.printForEvents(), "bank: " + bank.printForEvents())
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def ChangeProductQuanInCart(self, userID, storeID, product, quantity):
        try:
            toReturn = self.__market.ChangeProductQuanInCart(userID, storeID, product, quantity)
            eventLog = EventLog("change product quantity in cart", "userId: " + str(userID), "storeId: " + str(storeID),
                                "product: " + product.printForEvents(), "quantity: " + str(quantity))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def appointManagerToStore(self, storeID, assignerID, assigneID):  # check if the asssigne he member and assignerID!!
        try:
            toReturn = self.__market.appointManagerToStore(storeID, assignerID, assigneID)
            eventLog = EventLog("appoint manager to store", "storeId: " + str(storeID), "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneID))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def appointOwnerToStore(self, storeID, assignerID, assigneID):  # check if the asssigne he member and assignerID!!
        try:
            toReturn = self.__market.appointOwnerToStore(storeID, assignerID, assigneID)
            eventLog = EventLog("appoint owner to store", "storeId: " + str(storeID), "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneID))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def setStockManagerPermission(self, storeID, assignerID, assigneeID):
        try:
            toReturn = self.__market.setStockManagerPermission(storeID, assignerID, assigneeID)
            eventLog = EventLog("set stock manager permission", "storeId: " + str(storeID), "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneeID))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def setAppointOwnerPermission(self, storeID, assignerID, assigneeID):
        try:
            toReturn = self.__market.setAppointOwnerPermission(storeID, assignerID, assigneeID)
            eventLog = EventLog("set appoint owner permission", "storeId: " + str(storeID), "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneeID))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def setChangePermission(self, storeID, assignerID, assigneeID):
        try:
            toReturn = self.__market.setChangePermission(storeID, assignerID, assigneeID)
            eventLog = EventLog("set change permissions", "storeId: " + str(storeID), "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneeID))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def setRolesInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            toReturn = self.__market.setRolesInformationPermission(storeID, assignerID, assigneeID)
            eventLog = EventLog("set roles info permission", "storeId: " + str(storeID), "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneeID))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def setPurchaseHistoryInformationPermission(self, storeID, assignerID, assigneeID):
        try:
            toReturn = self.__market.setPurchaseHistoryInformationPermission(storeID, assignerID, assigneeID)
            eventLog = EventLog("set purchase history info permission", "storeId: " + str(storeID),
                                "assignerId: " + str(assignerID)
                                , "assigneeId: " + str(assigneeID))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    # need to add here all the fields of the product! because someone need to create the product
    def addProductToStore(self, storeID, userID, product):
        try:
            toReturn = self.__market.addProductToStore(storeID, userID, product)
            eventLog = EventLog("add product to store", "storeId: " + str(storeID), "userId: " + str(userID)
                                , "product: " + product.printForEvents())
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def addProductQuantityToStore(self, storeID, userID, product, quantity):
        try:
            toReturn = self.__market.addProductQuantityToStore(storeID, userID, product, quantity)
            eventLog = EventLog("add product quantity to store", "storeId: " + str(storeID), "userId: " + str(userID)
                                , "product: " + product.printForEvents(), "quantity: " + quantity)
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    # here we can take only the productId
    def removeProductFromStore(self, storeID, userID, product):
        try:
            toReturn = self.__market.removeProductFromStore(storeID, userID, product)
            eventLog = EventLog("remove product from store", "storeId: " + str(storeID), "userId: " + str(userID)
                                , "product: " + product.printForEvents())
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    # need to add here all the fields of the product! because someone need to create the product
    # maybe we should only take the new price/name/category
    def updateProductFromStore(self, userId, productId, newProduct):
        # not yet implemented
        pass

    def PrintRolesInformation(self, storeID, userID):
        try:
            toReturn = self.__market.PrintRolesInformation(storeID, userID)
            eventLog = EventLog("print roles info", "storeId: " + str(storeID), "userId: " + str(userID))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    def printPurchaseHistoryInformation(self, storeID, userID):
        try:
            toReturn = self.__market.printPurchaseHistoryInformation(storeID, userID)
            eventLog = EventLog("print purchase history info", "storeId: " + str(storeID), "userId: " + str(userID))
            self.__events.addEventLog(eventLog)
            return toReturn
        except Exception as e:
            return e

    # internal method
    def addTransaction(self, storeID, transaction):
        return self.__market.addTransaction(storeID, transaction)

    # internal method
    def removeTransaction(self, storeID, transaction):
        return self.__market.removeTransaction(storeID, transaction)

