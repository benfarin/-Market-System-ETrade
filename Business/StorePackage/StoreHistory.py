from Business.Transaction import Transaction


class StoreHistory:

    def __init__(self, storeId, storeName):
        self.__storeId = storeId
        self.__storeName = storeName
        self.__transactions = []

    def addTransaction(self, transaction):
        self.__transactions.append(transaction)

    def removeTransaction(self, transaction):
        self.__transactions.remove(transaction)

    def getTransactionHistory(self):
        return self.__transactions

    def getPurchaseHistoryInformation(self):
        info = "purchase history for store: " + self.__storeName + " ,storeId: " + str(self.__storeId) + " :\n"
        for transaction in self.__transactions:
            info += transaction.__str__() + "\n"
        return info

