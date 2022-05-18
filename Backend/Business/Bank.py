class Bank:

    def __init__(self, accountNumber, branch):
        self.__accountNumber = accountNumber
        self.__branch = branch

    def getAccountNumber(self):
        return self.__accountNumber

    def setAccountNumber(self, accountNumber):
        self.__accountNumber = accountNumber

    def getBranch(self):
        return self.__branch

    def setBranch(self, branch):
        self.__branch = branch

    def printForEvents(self):
        return "\n\t\t\taccount number: " + str(self.__accountNumber) + "\n\t\t\tbranch: " + str(self.__branch)

    # def __str__(self):
    #     return "Account Number: " + self.__accountNumber + " branch: " + self.__branch