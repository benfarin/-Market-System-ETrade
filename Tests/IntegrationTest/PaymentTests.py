import unittest

from Business.Address import Address
from Business.Bank import Bank
from Business.Market import Market
from Business.StorePackage.Product import Product
from Payment.PaymentDetails import PaymentDetails
from Payment.PaymentStatus import PaymentStatus
from Payment.PaymentSystem import PaymentSystem
from Payment.paymentlmpl import Paymentlmpl
from interfaces.IMarket import IMarket
from Business.UserPackage.Member import Member
from interfaces.IStore import IStore


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.__paymentlmpl: Paymentlmpl = Paymentlmpl().getInstance()
        self.__market: IMarket = Market().getInstance()
        self.__address1 = Address("Israel", "modiin", "avni hoshen", 4, 71813)
        self.__address2 = Address("Germany", "berlin", "rotchild", 1, 32523)
        self.__address3 = Address("Turkey", "ankra", "golda", 1, 32523)
        self.__address4 = Address("austria", "viena", "begin", 1, 32523)
        self.__bank1 = Bank(189301, 92049)
        self.__bank2 = Bank(83968, 7124)
        self.__bank3 = Bank(1145, 12)
        self.__bank4 = Bank(7452, 134)
        self.__member1 = Member("amos", "123", "089701866", self.__address1, self.__bank1)
        self.__member2 = Member("shimshon", "089751479", "34934", self.__address2, self.__bank2)
        self.__member3 = Member("gershon", "089717468", "2325", self.__address2, self.__bank2)
        self.__market.addActiveUser(self.__member1)
        self.__store3: IStore = self.__market.createStore("foot-locker", self.__member1.getUserID(), self.__bank1,
                                                          self.__address2)
        self.__product1: Product = Product(1, "milk", 75, "halavi", "ff")
        self.__market.addProductToStore(self.__store3.getStoreId(), self.__member1.getUserID(), self.__product1)
        self.__market.addProductQuantityToStore(self.__store3.getStoreId(), self.__member1.getUserID(),
                                                self.__product1.getProductId(), 100)

        self.__paymentDetails: PaymentDetails = PaymentDetails(self.__member1.getUserID(),self.__member1.getBank(),self.__store3.getStoreBankAccount(),self.__store3.getStoreId(),750)

    def test_createPayment(self):
        paymentStaus1 :PaymentStatus = self.__paymentlmpl.createPayment(self.__paymentDetails)
        self.assertEqual("payment succeeded", paymentStaus1 .getStatus())

if __name__ == '__main__':
    unittest.main()
