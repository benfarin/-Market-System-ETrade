from Business.Bank import Bank


class BankDTO:
    def __init__(self, bank: Bank):
        self.__accountNumber = bank.getAccountNumber()
        self.__branch = bank.getBranch()

    def getAccountNumber(self):
        return self.__accountNumber

    def setAccountNumber(self, accountNumber):
        self.__accountNumber = accountNumber

    def getBranch(self):
        return self.__branch

    def setBranch(self, branch):
        self.__branch = branch


