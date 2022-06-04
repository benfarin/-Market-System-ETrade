
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()
from ModelsBackend.models import BankModel
class Bank:

    def __init__(self, accountNumber=None, branch=None, model=None):
        # self.__accountNumber = accountNumber
        # self.__branch = branch
        if model is None:
            self.__b = BankModel.objects.get_or_create(accountNumber=accountNumber, branch=branch)[0]
        else:
            self.__b = model

    def getAccountNumber(self):
        return self.__b.accountNumber

    def setAccountNumber(self, accountNumber):
        self.__b.accountNumber = accountNumber
        self.__b.save()

    def getBranch(self):
        return self.__b.branch

    def setBranch(self, branch):
        self.__b.branch = branch
        self.__b.save()

    # def printForEvents(self):
    #     return "\n\t\t\taccount number: " + str(self.__accountNumber) + "\n\t\t\tbranch: " + str(self.__branch)

    def getModel(self):
        return self.__b

    def removeBank(self):
        self.__b.delete()

    def __eq__(self, other):
        return isinstance(other, Bank) and self.__b == other.getModel()

    def __hash__(self):
        return hash(self.__b.branch and self.__b.accountNumber)



    # def __str__(self):
    #     return "Account Number: " + self.__accountNumber + " branch: " + self.__branch