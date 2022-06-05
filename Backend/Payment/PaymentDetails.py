from Backend.Business.Bank import Bank


class PaymentDetails:
    def __init__(self, userId, cardNumber, month, year, holderCardName, cvv, holderID,
                 storeBank, paymentAmount):
        self.__userId = userId
        self.__cardNumber = cardNumber
        self.__month = month
        self.__year = year
        self.__holderCardName = holderCardName
        self.__cvv = cvv
        self.holderID = holderID
        self.__storeBank: Bank = storeBank
        self.__paymentAmount = paymentAmount

    def getUserId(self):
        return self.__userId

    def getCardNumber(self):
        return self.__cardNumber

    def getMonth(self):
        return self.__month

    def getYear(self):
        return self.__year

    def getHolderCardName(self):
        return self.__holderCardName

    def getCVV(self):
        return self.__cvv

    def getHolderID(self):
        return self.holderID

    def getStoreBank(self):
        return self.__storeBank

    def getPaymentAmount(self):
        return self.__paymentAmount
