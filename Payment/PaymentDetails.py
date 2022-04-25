from Business.Bank import Bank


class PaymentDetails:
    def __init__(self, userId, clientbankAccount, recieverBankAccount, storeID, paymentAmount):
        self.__userId = userId
        self.__clientbankAccount: Bank = clientbankAccount
        self.__recieverBankAccount: Bank = recieverBankAccount
        self.__storeId = storeID
        self.__paymentAmount = paymentAmount

    def getUserId(self):
        return self.__userId

    def getClientBankAccount(self):
        return self.__clientbankAccount

    def getRecieverBankAccount(self):
        return self.__recieverBankAccount

    def getstoreID(self):
        return self.getstoreID()

    def getPaymentAmount(self):
        return self.__paymentAmount
