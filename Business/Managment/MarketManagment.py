from interfaces.IMarket import IMarket
from Business.Market import Market
from Business.Bank import Bank
from Business.Address import Address


class MarketManage:
    def __init__(self):
        self.__market: IMarket = Market()

    def createStore(self, storeName, userID, bank, address):
        try:
            self.__market.createStore(storeName, userID, bank, address)
        except Exception as e:
            raise Exception(e)

    def createBankAcount(self, accountNumber, branch):
        return Bank(accountNumber, branch)

    def createAddress(self, country, city, street, apartmentNum, zipCode):
        return Address(country, city, street, apartmentNum, zipCode)

    def addProductToCart(self, userID, storeID, product, quantity):
        try:
            return self.__market.addProductToCart(userID, storeID, product, quantity)
        except Exception as e:
            raise Exception(e)

    def removeProductFromCart(self, userID, storeID, productId):
        try:
            return self.__market.removeProductFromCart(storeID, userID, productId)
        except Exception as e:
            raise Exception(e)

    def updateProductFromCart(self, userID, storeID, productId, quantity):
        try:
            return self.__market.updateProductFromCart(storeID, userID, productId, quantity)
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

    def getProductPriceRange(self, minPrice, highPrice):
        try:
            return self.__market.getProductByPriceRange(self, minPrice, highPrice)
        except Exception as e:
            raise Exception(e)

    def purchaseCart(self, userID, bank):
        try:
            return self.__market.purchaseCart(userID, bank)
        except Exception as e:
            raise Exception(e)