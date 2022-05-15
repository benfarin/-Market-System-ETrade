from Business.UserPackage.Member import Member


class MemberDTO:

    def __init__(self, member: Member):
        self.__memberId = member.getUserID()
        self.__memberName = member.getMemberName()
        self.__phone = member.getPhone()
        self.__address = member.getAddress()
        self.__bank = member.getBank()
        self.__transactions = member.getTransactions()
        self.__paymentsIds = member.getPaymentsIds()
        self.__cart = member.getCart()

    def getUserID(self):
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