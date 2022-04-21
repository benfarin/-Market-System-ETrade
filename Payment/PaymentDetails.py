from Business.Bank import Bank

class PaymentDetails:
    def __init__(self,client_id,clientbankAccount,recieverBankAccount,storeID,paymentAmount):
        self.__client_id =client_id
        self.__clientbankAccount : Bank= clientbankAccount
        self.__recieverBankAccount : Bank= recieverBankAccount
        self.__storeID=storeID
        self.__paymentAmount = paymentAmount
    def getClientId(self):
        return  self.__client_id
    def getClientBankAccount(self):
        return self.__clientbankAccount
    def getRecieverBankAccount(self):
        return self.__recieverBankAccount
    def getstoreID(self):
        return self.__storeID
    def getPaymentAmount(self):
        return self.__paymentAmount

