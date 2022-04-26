class CreditCard:
    def __init__(self,holderCardName, cardNumber, month, year, cvv, holderID):
        self.__holderCardName = holderCardName
        self.__cardNumber = cardNumber
        self.__month = month
        self.__year = year
        self.__cvv = cvv
        self.__holderID = holderID

    def getHolderCardName(self):
        return  self.__holderCardName
    def setHolderCardName(self,holderCardName):
        self.__holderCardName = holderCardName
    def getCardNumber(self):
        return self.__cardNumber
    def setCardNumber(self, cardNumber):
        self.__cardNumber = cardNumber
    def getMonth(self):
        return self.__month
    def setMonth(self, month):
        self.__month = month
    def getYear(self):
        return  self.__year
    def setYear(self,year):
        self.__year = year
    def getCVV(self):
        return self.__cvv
    def setCVV(self, cvv):
        self.__cvv = cvv
    def getHolderID(self):
        return self.__holderID
    def setHolderID(self, holderID):
        self.__holderID = holderID
    # def __str__(self):
    #     return " Holder card name: " + self.__holderCardName + " card number: " + self.__cardNumber \
    #            +" exp: " + self.__month + "\\" + self.__year + " cvv: " + self.__cvv + " holder ID: " + self.__holderID
