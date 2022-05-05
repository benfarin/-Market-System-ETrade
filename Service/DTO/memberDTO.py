class memberDTO:

    def __init__(self, memberId, memberName, phone, address, bank, transactions, paymentsIds, cart):
        self.__memberId = memberId
        self.__memberName = memberName
        self.__phone = phone
        self.__address = address
        self.__bank = bank
        self.__transactions = transactions
        self.__paymentsIds = paymentsIds
        self.__cart = cart

    def getMemberId(self):
        return self.__memberId

    def getMemberName(self):
        return self.__memberName

    def getPhone(self):
        return self.__phone

    def getAddress(self):
        return self.__address

    def getBank(self):
        return self.__bank

    def getTransactions(self):
        return self.__transactions

    def getPaymentsIds(self):
        return self.__paymentsIds

    def getCart(self):
        return self.__cart