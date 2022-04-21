class PaymentDetails:
    def __init__(self,client_id,clientbankAccount,recieverBankAccount,storeID,paymentAmount):
        self.__client_id =client_id
        self.__clientbankAccount = clientbankAccount
        self.__recieverBankAccount = recieverBankAccount
        self.__storeID=storeID
        self.__paymentAmount = paymentAmount
        