class UserTransaction:

    def __init__(self, userId):
        self.__UserId = userId
        self.__transactions = []

    def addTransaction(self, transaction):
        self.__transactions.append(transaction)

    def removeTransaction(self, transaction):
        self.__transactions.remove(transaction)

    def getTransactions(self):
        return self.__transactions
