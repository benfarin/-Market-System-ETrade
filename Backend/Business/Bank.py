from ModelsBackend.models import BankModel
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()

class Bank:

    def __init__(self, accountNumber, branch):
        self.__accountNumber = accountNumber
        self.__branch = branch
        self.__b = BankModel(accountNumber=self.__accountNumber, branch=self.__branch)
        self.__b.save()

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

    def getModel(self):
        return self.__b

    # def __str__(self):
    #     return "Account Number: " + self.__accountNumber + " branch: " + self.__branch