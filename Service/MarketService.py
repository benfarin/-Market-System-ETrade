from Business.MarketManage import MarketManage
from interfaces import IMarket
class MarketService:
    def __init__(self):
        self.__market: IMarket = MarketManage()
    def addGuest(self):
        self.__market.addGuest()
    def addProductToCart(self,userID,storeId,product,quantity):
        return self.__market.addProductToCart(userID, storeId, product, quantity)
    def removeProductFromCart(self,userID,storeID ,product):
        return self.__market.removeProductFromCart(userID,storeID ,product)
    def updateProductFromCart(self,userID,storeID,product,quantity):
       return  self.__market.updateProductFromCart(userID,storeID,product,quantity)
    def checkOnlineMember(self, userID):
           return self.__market.checkOnlineMember(userID)

    def getStoreByName(self,store_name):
        return self.__market.getStoreByName(store_name)

    def getStoreById(self,id_store): #maybe should be private
        return self.__market.getStoreById(id_store)

    def getProductByCatagory(self,catagory):
        return self.__market.getProductByCatagory(catagory)

    def getProductsByName(self,nameProduct):
        return  self.__market.getProductsByName(nameProduct)

    def getProductByKeyWord(self, keyword):
        return  self.__market.getProductByKeyWord(keyword)

    def getUserByName(self,userName):
        return self.__market.getUserByName(userName)

    def createStore(self,storeName, userID, bankAccount, address):
        return  self.__market.createStore(storeName, userID, bankAccount, address)

    def getStores(self):
        return self.__market.getStores()

    def getActiveUsers(self):
        return self.__market.getActiveUsers()

    def getProducts(self):
        return self.__market.getProducts()

    def addMember(self,userID, password, phone, address, bank):
         self.__market.addMember(userID, password, phone, address, bank)

    def getStoreHistory(self,userID,storeID): # --------------------------------------------------
        return self.__market.getStoreHistory(userID,storeID)

    def removeProductFromCart(self,userID,storeID ,product):
         self.__market.removeProductFromCart(userID,storeID ,product)

    def updateProductFromCart(self,userID,storeID,product,quantity):
        self.__market.updateProductFromCart(userID,storeID,product,quantity)

    def ChangeProductQuanInCart(self,userID,storeID,product,quantity):
        return self.__market.ChangeProductQuanInCart(userID,storeID,product,quantity)

    def appointManagerToStore(self,storeID, assignerID , assigneID ): # check if the asssigne he member and assignerID!!
        return self.__market.appointManagerToStore(storeID, assignerID , assigneID )
    def appointOwnerToStore(self,storeID, assignerID , assigneID):# check if the asssigne he member and assignerID!!
        return self.__market.appointOwnerToStore(storeID, assignerID , assigneID)

    def setStockManagerPermission(self,storeID ,assignerID, assigneeID):
       return self.__market.setStockManagerPermission(storeID ,assignerID, assigneeID)

    def setAppointOwnerPermission(self,storeID ,assignerID, assigneeID):
        return self.__market.setAppointOwnerPermission(storeID ,assignerID, assigneeID)

    def setChangePermission(self,storeID, assignerID, assigneeID):
        return self.__market.setChangePermission(storeID, assignerID, assigneeID)

    def setRolesInformationPermission(self,storeID, assignerID, assigneeID):
        self.__market.setRolesInformationPermission(storeID, assignerID, assigneID)

    def setPurchaseHistoryInformationPermission(self,storeID, assignerID, assigneeID):
        return self.__market.setPurchaseHistoryInformationPermission(storeID, assignerID, assigneeID)

    def addProductToStore(self,storeID , userID, product):
        return self.__market.addProductToStore(storeID , userID, product)

    def addProductQuantityToStore(self, storeID ,userID,product, quantity):
        return self.__market.addProductQuantityToStore(storeID ,userID,product, quantity)

    def removeProductFromStore(self,storeID , userID, product):
        return self.__market.removeProductFromStore(storeID , userID, product)

    def PrintRolesInformation(self,storeID ,userID):
        return self.__market.PrintRolesInformation(storeID ,userID)

    def addTransaction(self,storeID ,transaction):
        return self.__market.addTransaction(storeID ,transaction)

    def removeTransaction(self,storeID ,transaction):
        return self.__market.removeTransaction(storeID ,transaction)

    def printPurchaseHistoryInformation(self,storeID ,userID):
         return self.__market.printPurchaseHistoryInformation(storeID ,userID)

    def updateProductFromStore(self, userId, productId, newProduct):
        return self.__market.updateProductFromStore(userId, productId, newProduct)


