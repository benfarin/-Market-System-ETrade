import unittest

from Backend.Business.StorePackage.Product import Product
from Backend.Business.Transactions.StoreTransaction import StoreTransaction
from Backend.Business.Transactions.UserTransaction import UserTransaction


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.product1 = Product(0, 0, "TestProduct", 50, "TestCategory", 5, ["Check", "Check2"]).getModel()
        cls.product2 = Product(1, 0, "TestProduct", 50, "TestCategory", 5, ["Check", "Check2"]).getModel()
        cls.st = StoreTransaction(0, "Kfir's store", 1, 2, [cls.product1, cls.product2], 100)
        cls.st_2 = StoreTransaction(0, "Kfir's store", 2, 4, [cls.product1], 50)
        cls.ut = UserTransaction(0, 3, [cls.st.getModel(), cls.st_2.getModel()], 5, 150)

    def test_StoreTransaction(self):
        self.assertEqual(self.st.getStoreId(), 0)
        self.assertEqual(self.st.getStoreName(), "Kfir's store")
        self.assertEqual(self.st.getTransactionID(), 1)
        self.assertEqual(self.st.getPaymentId(), 2)
        self.assertEqual(self.st.getProducts(), [self.product1, self.product2])
        self.assertEqual(self.st.getAmount(), 100)

    def test_UserTransaction(self):
        self.assertEqual(self.ut.getUserId(), 0)
        self.assertEqual(self.ut.getUserTransactionId(), 3)
        self.assertEqual(self.ut.getStoreTransactions(), [self.st.getModel(), self.st_2.getModel()])
        self.assertEqual(self.ut.getPaymentId(), 5)
        self.assertEqual(self.ut.getTotalAmount(), 150)


if __name__ == '__main__':
    unittest.main()
