from Backend.Business.UserPackage.Member import Member
from Backend.Business.Market import Market


class SystemManager(Member):
    def __init__(self, userName, password, phone, address, bank):
        super().__init__(userName, password, phone, address, bank)
        self.__market = Market.getInstance()

    def getAllStoreTransactions(self):
        try:
            return self.__market.getAllStoreTransactions()
        except Exception as e:
            raise Exception(e)

    def getAllUserTransactions(self):
        try:
            return self.__market.getAllUserTransactions()
        except Exception as e:
            raise Exception(e)

    def getStoreTransaction(self, transactionId):
        try:
            return self.__market.getStoreTransaction(transactionId)
        except Exception as e:
            raise Exception(e)

    def getUserTransaction(self, transactionId):
        try:
            return self.__market.getUserTransaction(transactionId)
        except Exception as e:
            raise Exception(e)

    def getStoreTransactionByStoreId(self, storeId):
        try:
            return self.__market.getStoreTransactionByStoreId(storeId)
        except Exception as e:
            raise Exception(e)
