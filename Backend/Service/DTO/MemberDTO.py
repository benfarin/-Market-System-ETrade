from Backend.Business.UserPackage.Member import Member
from Backend.Service.DTO.AddressDTO import AddressDTO
from Backend.Service.DTO.BankDTO import BankDTO
from Backend.Service.DTO.UserTransactionDTO import userTransactionDTO
from Backend.Service.DTO.CartDTO import CartDTO


class MemberDTO:

    def __init__(self, member: Member):
        self.__memberId = member.getUserID()
        self.__memberName = member.getMemberName()
        self.__phone = member.getPhone()
        self.__address = AddressDTO(member.getAddress())
        self.__bank = BankDTO(member.getBank())
        self.__transactions = []
        for transaction in member.getTransactions().values():
            self.__transactions.append(userTransactionDTO(transaction))
        self.__cart = CartDTO(member.getCart())

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
        toReturn += "\n\ttransactions: "
        for transaction in self.__transactions:
            toReturn += "\n\t\t" + transaction.__str__()
        return toReturn + "\n\t" + self.__cart.__str__()
