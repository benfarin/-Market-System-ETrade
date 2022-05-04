import unittest

from Business.Address import Address
from Business.Bank import Bank
from Business.Market import Market
from Business.StorePackage.Product import Product
from Business.UserPackage.Member import Member
from interfaces.IMarket import IMarket


class MarketTests(unittest.TestCase):
    def setUp(self):
        self.__market: IMarket = Market().getInstance()
        self.__address1 = Address("Israel", "modiin", "avni hoshen", 4, 71813)
        self.__address2 = Address("Germany", "berlin", "rotchild", 1, 32523)
        self.__address3 = Address("Turkey", "ankra", "golda", 1, 32523)
        self.__bank1 = Bank(189301, 92049)
        self.__bank2 = Bank(83968, 7124)
        self.__bank3 = Bank(1145, 12)
        self.__member1 = Member("amos", "123", "089701866", self.__address1, self.__bank1)
        self.__member2 = Member("shimshon", "089751479", "34934", self.__address2, self.__bank2)
        self.__member3 = Member("gershon", "089717468", "2325", self.__address2, self.__bank2)

        self.__product1 = Product(1, "tara milk 5%", 5.5, "dairy", ["tara", "dairy drink", "5%"])
        self.__product2 = Product(2, "shoko", 6.90, "dairy", ["sugar", "chocolate", "dairy drink"])
        self.__product3 = Product(3, "dress", 199.99, "cloth", ["short sleeve", "red"])

        # store1: founder: member1, owners: [member1], managers: []
        # store2: founder: member2, owners: [member2], managers: []

    def test_createStore(self):
        # storeId1 = 0 , founder: member1
        self.__storeId1 = self.__market.createStore("foot-locker", self.__member1, self.__bank1,self.__address2)
        self.assertEqual(0, self.__storeId1)

        # storeId2 = 1, founder: member2
        self.__storeId2 = self.__market.createStore("Decathlon", self.__member2, self.__bank1, self.__address3)
        self.assertEqual(1, self.__storeId2)

    def test_addProductToStore(self):
        self.test_createStore()
        self.assertTrue(self.__market.addProductToStore(0, self.__member1, self.__product1))
        self.assertTrue(self.__market.addProductToStore(0, self.__member1, self.__product2))
        self.assertTrue(self.__market.addProductToStore(1, self.__member2, self.__product3))

    def test_addProductToStore_FAIL(self):
        # try to add a product to a non-existing store
        self.assertRaises(Exception, lambda: self.__market.addProductToStore(1, self.__member1, self.__product1))
        self.test_createStore()
        # member without the permission tries to add a product
        self.assertRaises(Exception, lambda: self.__market.addProductToStore(0, self.__member2, self.__product1))
        # try to add a product that all ready exists
        self.assertTrue(self.__market.addProductToStore(0, self.__member1, self.__product1))
        self.assertRaises(Exception,lambda: self.__market.addProductToStore(0, self.__member1, self.__product1))

    def test_addProductQuantity(self):
        self.test_addProductToStore()
        try:
            self.__market.addProductQuantityToStore(0, self.__member1, self.__product1.getProductId(), 100)
            self.__market.addProductQuantityToStore(0, self.__member1, self.__product2.getProductId(), 92)
            self.__market.addProductQuantityToStore(1, self.__member2, self.__product3.getProductId(), 31)
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_addProductQuantity_Fail(self):
        # try to add quantity to a product that doesn't exist
        self.assertRaises(Exception, lambda: self.__market.addProductQuantityToStore(0, self.__member1,
                                                                                     self.__product1.getProductId(),
                                                                                     100))
        self.test_addProductToStore()
        # a member without the permission tries to add quantity of the product
        self.assertRaises(Exception, lambda: self.__market.addProductQuantityToStore(0, self.__member3,
                                                                                     self.__product1.getProductId(),
                                                                                     100))
        # trying to add quantity = 0
        self.assertRaises(Exception, lambda: self.__market.addProductQuantityToStore(0, self.__member1,
                                                                                     self.__product1.getProductId(), 0))
        # trying to add quantity < 0
        self.assertRaises(Exception, lambda: self.__market.addProductQuantityToStore(0, self.__member1,
                                                                                     self.__product1.getProductId(),
                                                                                     -3))

    def test_addProductToCart(self):
        self.test_addProductQuantity()
        self.assertTrue(self.__market.addProductToCart(self.__member1, 0, self.__product1.getProductId(), 7))
        self.assertTrue(self.__market.addProductToCart(self.__member1, 1, self.__product3.getProductId(), 3))
        self.assertTrue(self.__market.addProductToCart(self.__member2, 0, self.__product2.getProductId(), 10))
        print(self.__member1.getCart().printBags())
        print(self.__member2.getCart().printBags())

    def test_addProductToCart_Fail(self):
        # try to add product to cart from store that doesn't exist
        self.assertRaises(Exception, lambda: self.__market.addProductToCart(self.__member1, 0, self.__product1.getProductId(), 10))
        self.test_createStore()
        # try to add product that doesn't exist in the store
        self.assertRaises(Exception, lambda: self.__market.addProductToCart(self.__member1, 0, self.__product1.getProductId(), 10))

        self.assertTrue(self.__market.addProductToStore(0, self.__member1, self.__product1))
        self.__market.addProductQuantityToStore(0, self.__member1, self.__product1.getProductId(), 100)
        # try to buy product that doesn't have in stock
        self.assertRaises(Exception, lambda: self.__market.addProductToCart(self.__member1, 0, self.__product1.getProductId(), 110))

    def test_removeProductFromCart(self):
        self.test_addProductToCart()
        self.assertTrue(self.__market.removeProductFromCart(0, self.__member1, self.__product1.getProductId()))
        print(self.__member1.getCart())

    def test_updateProductFromCart(self):
        pass

    def test_purchaseCart(self):
        self.test_addProductToCart()
        self.assertTrue(self.__market.purchaseCart(self.__member1, self.__bank1))
        trans = self.__member1.getTransaction(2)
        print("\n")
        for storeId in trans.getStoreTransactions().keys():
            print(trans.getStoreTransactions()[storeId].getPurchaseHistoryInformation())

    def test_removeStore(self):
        self.test_createStore()
        self.assertEqual(self.__market.removeStore(0, self.__member1), "Store removed successfully!")


if __name__ == '__main__':
    unittest.main()
