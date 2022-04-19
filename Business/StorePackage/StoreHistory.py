from Business.Transaction import Transaction


class StoreHistory:

    def __init__(self, storeId):
        self.__storeId = storeId
        self.__transactions = []

    def addTransaction(self, transaction):
        self.__transactions.append(transaction)

    def removeTransaction(self, transaction):
        self.__transactions.remove(transaction)

    def getStoreTransactionHistory(self):
        return self.__transactions
