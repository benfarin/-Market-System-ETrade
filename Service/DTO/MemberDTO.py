from Business.UserPackage.Member import Member


class MemberDTO:

    def __init__(self, member: Member):
        self.__memberId = member.getUserID()
        self.__memberName = member.getMemberName()
        self.__phone = member.getPhone()
        self.__address = member.getAddress()
        self.__bank = member.getBank()
        self.__transactions = member.getTransactions()
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

    def getCart(self):
        return self.__cart

    def __str__(self):
        toReturn = "member: "
        toReturn += "\n\tid: " + str(self.__memberId)
        toReturn += "\n\tname: " + self.__memberName
        toReturn += "\n\tphone: " + self.__phone
        toReturn += "\n\t" + self.__address.__str__()
        toReturn += "\n\t" + self.__bank.__str__()
        for transaction in self.__transactions.values():
            toReturn += "\n\t" + transaction.__str__()
        return toReturn + "\n\t" + self.__cart.__str__()
