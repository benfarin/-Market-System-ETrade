from Business.MarketManage import MarketManage
from interfaces import IMarket
class MarketService:
    def __init__(self):
        self.__market: IMarket = MarketManage()
    def addGuest(self):
        self.__market.addGuest()
    def addProductToCart(self,username,storeId,product,quantity):
        return self.__market.addProductToCart(username, storeId, product, quantity)
    def removeProductFromCart(self,userName,storeID ,product):
        return self.__market.removeProductFromCart(userName,storeID ,product)
    def updateProductFromCart(self,userName,storeID,product,quantity):
       return  self.__market.updateProductFromCart(userName,storeID,product,quantity)
    def checkOnlineMember(self, userName):
           return self.__market.checkOnlineMember(userName)

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

    def createStore(self,storeName, userName, bankAccount, address):
        return  self.__market.createStore(storeName, userName, bankAccount, address)

    def getStores(self):
        return self.__market.getStores()

    def getActiveUsers(self):
        return self.__market.getActiveUsers()

    def getProducts(self):
        return self.__market.getProducts()

    def addMember(self,userName, password, phone, address, bank):
         self.__market.addMember(userName, password, phone, address, bank)

    def getStoreHistory(self,userName,storeID): # --------------------------------------------------
        return self.__market.getStoreHistory(userName,storeID)

    def removeProductFromCart(self,userName,storeID ,product):
         self.__market.removeProductFromCart(userName,storeID ,product)

    def updateProductFromCart(self,userName,storeID,product,quantity):
        self.__market.updateProductFromCart(userName,storeID,product,quantity)

    def ChangeProductQuanInCart(self,userName,storeID,product,quantity):
        return self.__market.ChangeProductQuanInCart(userName,storeID,product,quantity)

    def appointManagerToStore(self,storeID, assignerID , assigneID ): # check if the asssigne he member and assignerID!!
        return self.__market.appointManagerToStore(storeID, assignerID , assigneID )
    def appointOwnerToStore(self,storeID, assignerID , assigneID):# check if the asssigne he member and assignerID!!
        return self.__market.appointOwnerToStore(storeID, assignerID , assigneID)

    def setStockManagerPermission(self,storeID ,assignerName, assigneeName):
       return self.__market.setStockManagerPermission(storeID ,assignerName, assigneeName)

    def setAppointOwnerPermission(self,storeID ,assignerName, assigneeName):
        return self.__market.setAppointOwnerPermission(storeID ,assignerName, assigneeName)

    def setChangePermission(self,storeID, assignerName, assigneeName):
        return self.__market.setChangePermission(storeID, assignerName, assigneeName)

    def setRolesInformationPermission(self,storeID, assignerName, assigneeName):
        self.__market.setRolesInformationPermission(storeID, assignerName, assigneeName)

    def setPurchaseHistoryInformationPermission(self,storeID, assignerName, assigneeName):
        return self.__market.setPurchaseHistoryInformationPermission(storeID, assignerName, assigneeName)

    def addProductToStore(self,storeID , userName, product):
        return self.__market.addProductToStore(storeID , userName, product)

    def addProductQuantityToStore(self, storeID ,userName,product, quantity):
        return self.__market.addProductQuantityToStore(storeID ,userName,product, quantity)

    def removeProductFromStore(self,storeID , userName, product):
        return self.__market.removeProductFromStore(storeID , userName, product)

    def PrintRolesInformation(self,storeID ,userName):
        return self.__market.PrintRolesInformation(storeID ,userName)

    def addTransaction(self,storeID ,transaction):
        return self.__market.addTransaction(storeID ,transaction)

    def removeTransaction(self,storeID ,transaction):
        return self.__market.removeTransaction(storeID ,transaction)

    def printPurchaseHistoryInformation(self,storeID ,userName):
         return self.__market.printPurchaseHistoryInformation(storeID ,userName)

    def updateProductFromStore(self, userId, productId, newProduct):
        return self.__market.updateProductFromStore(userId, productId, newProduct)


