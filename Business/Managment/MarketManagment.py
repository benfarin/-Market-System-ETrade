from interfaces.IMarket import IMarket
from Business.Market import Market


class MarketManage:
    def __init__(self):
        self.__market: IMarket = Market()

    def createStore(self, storeName, userID, bank, address):
        try:
            self.__market.createStore(storeName, userID, bank, address)
        except Exception as e:
            raise Exception(e)

    def addGuest(self):
        pass

    def addMember(self, userName, password, phone, address, bank):
        pass

    def addProductToCart(self, userID, storeID, product, quantity):
        try:
            return self.__market.addProductToCart(userID, storeID, product, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromCart(self, userID, storeID, product):
        try:
            return self.__market.removeProductFromCart(userID, storeID, product)
        except Exception as e:
            raise Exception(e)

    def updateProductFromCart(self, userID, storeID, product, quantity):
        try:
            return self.__market.updateProductFromCart(userID, storeID, product, quantity)
        except Exception as e:
            raise Exception(e)

    def ChangeProductQuanInCart(self, userID, storeID, product, quantity):
        try:
            return self.__market.ChangeProductQuanInCart(userID, storeID, product, quantity)
        except Exception as e:
            raise Exception(e)

    def addTransaction(self, storeID, transaction):
        try:
            return self.__market.addTransaction(storeID, transaction)
        except Exception as e:
            raise Exception(e)

    def removeTransaction(self, storeID, transaction):
        try:
            return self.__market.removeTransaction(storeID, transaction)
        except Exception as e:
            raise Exception(e)

    def getProductByCategory(self, category):
        try:
            return self.__market.getProductByCatagory(category)
        except Exception as e:
            raise Exception(e)

    def getProductsByName(self, nameProduct):
        try:
            return self.__market.getProductsByName(nameProduct)
        except Exception as e:
            raise Exception(e)

    def getProductByKeyWord(self, keyword):
        try:
            return self.__market.getProductByKeyWord(keyword)
        except Exception as e:
            raise Exception(e)

    def purchaseCart(self, userID, bank):
        try:
            return self.__market.purchaseCart(userID, bank)
        except Exception as e:
            raise Exception(e)
