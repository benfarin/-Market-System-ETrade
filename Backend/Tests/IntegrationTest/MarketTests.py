import unittest

from Backend.Business.Address import Address
from Backend.Business.Bank import Bank
from Backend.Business.Market import Market
from Backend.Business.StorePackage.Product import Product
from Backend.Business.StorePackage.Store import Store
from Backend.Business.UserPackage.Member import Member
from Backend.Interfaces.IMarket import IMarket
import threading


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

        self.__store = self.__market.createStore("foot-locker", self.__member1, self.__bank1,
                                                    self.__address2)
        self.__storeId1 = self.__store.getStoreId()


        self.__product1 = Product(1,0, "tara milk 5%", 5.5, "dairy", 10 ,["tara", "dairy drink", "5%"])
        self.__product2 = Product(2,0, "shoko", 6.90, "dairy",15, ["sugar", "chocolate", "dairy drink"])
        self.__product3 = Product(3,0, "dress", 199.99, "cloth",7, ["short sleeve", "red"])

        # store1: founder: member1, owners: [member1], managers: []
        # store2: founder: member2, owners: [member2], managers: []

    def test_createStore(self):   ##WORKING
        self.__store2 = self.__market.createStore("Decathlon", self.__member2, self.__bank1, self.__address3)
        self.assertIsNotNone(self.__store2)
        self.__storeId2 = self.__store2.getStoreId()

        # storeId1 = 0 , founder: member1
        # self.assertEqual(0, self.__storeId1)
        # # storeId2 = 1, founder: member2
        # self.assertEqual(1, self.__store2.getStoreId())

    def test_addProductToStore(self): ##WORKING
        self.test_createStore()
        self.assertTrue(self.__market.addProductToStore(self.__storeId1, self.__member1, self.__product1))
        self.assertTrue(self.__market.addProductToStore(self.__storeId1, self.__member1, self.__product2))
        self.assertTrue(self.__market.addProductToStore(self.__storeId2, self.__member2, self.__product3))


    def test_addProductToStore_FAIL(self):  ##WORKING
        # try to add a product to a non-existing store
        self.assertRaises(Exception, lambda: self.__market.addProductToStore(self.__storeId2, self.__member1, self.__product1))
        self.test_createStore()
        # member without the permission tries to add a product
        self.assertRaises(Exception, lambda: self.__market.addProductToStore(self.__storeId1, self.__member2, self.__product1))
        # try to add a product that all ready exists
        self.assertTrue(self.__market.addProductToStore(self.__storeId1, self.__member1, self.__product1))
        self.assertRaises(Exception, lambda: self.__market.addProductToStore(self.__storeId1, self.__member1, self.__product1))
        # try to add in the same time
        self.__market.appointOwnerToStore(self.__storeId1, self.__member1, self.__member3)
        self.assertTrue(self.__market.addProductToStore(self.__storeId1, self.__member1, self.__product3))
        self.assertRaises(Exception, lambda: self.__market.addProductToStore(self.__storeId1, self.__member3, self.__product3))

    def test_addProductQuantity(self):  ##WORKING
        self.test_addProductToStore()
        try:
            self.__market.addProductQuantityToStore(self.__storeId1, self.__member1, self.__product1.getProductId(), 100)
            self.__market.addProductQuantityToStore(self.__storeId1, self.__member1, self.__product2.getProductId(), 92)
            self.__market.addProductQuantityToStore(self.__storeId2, self.__member2, self.__product3.getProductId(), 31)

            self.__market.appointOwnerToStore(self.__storeId1, self.__member1, self.__member3)
            t1 = threading.Thread(target=self.__market.addProductQuantityToStore, args=
            (self.__storeId1, self.__member1, self.__product1.getProductId(), 10))
            t2 = threading.Thread(target=self.__market.addProductQuantityToStore, args=
            (self.__storeId1, self.__member3, self.__product1.getProductId(), 20))

            t1.start()
            t2.start()

            t1.join()
            t2.join()
            store0: Store = self.__market.getStoreById(self.__storeId1)
            self.assertTrue(130, store0.getProductQuantity()[self.__product1.getProductId()])

        except:
            self.assertTrue(False)

    def test_addProductQuantity_Fail(self): ##WORKING
        # try to add quantity to a product that doesn't exist
        self.assertRaises(Exception, lambda: self.__market.addProductQuantityToStore(self.__storeId1, self.__member1,
                                                                                     self.__product1.getProductId(),
                                                                                     100))
        self.test_addProductToStore()
        # a member without the permission tries to add quantity of the product
        self.assertRaises(Exception, lambda: self.__market.addProductQuantityToStore(self.__storeId1, self.__member3,
                                                                                     self.__product1.getProductId(),
                                                                                     100))
        # trying to add quantity = 0
        self.assertRaises(Exception, lambda: self.__market.addProductQuantityToStore(self.__storeId1, self.__member1,
                                                                                     self.__product1.getProductId(), 0))
        # trying to add quantity < 0
        self.assertRaises(Exception, lambda: self.__market.addProductQuantityToStore(self.__storeId1, self.__member1,
                                                                                     self.__product1.getProductId(),
                                                                                     -3))
    def test_addProductToCart(self):  ##WORKING
        self.test_addProductQuantity()
        self.assertTrue(self.__market.addProductToCart(self.__member1, self.__storeId1, self.__product1.getProductId(), 7))
        self.assertTrue(self.__market.addProductToCart(self.__member1, self.__storeId2, self.__product3.getProductId(), 3))
        self.assertTrue(self.__market.addProductToCart(self.__member2, self.__storeId1, self.__product2.getProductId(), 10))

    def test_addProductToCartWithoutStoreID(self):  ##WORKING
        self.test_addProductQuantity()
        self.assertTrue(self.__market.addProductToCartWithoutStore(self.__member1, self.__product1.getProductId(), 7))
        self.assertTrue(self.__market.addProductToCartWithoutStore(self.__member1, self.__product3.getProductId(), 3))
        self.assertTrue(self.__market.addProductToCartWithoutStore(self.__member2, self.__product2.getProductId(), 10))


    def test_addProductToCart_Fail(self): ##WORKING
        # try to add product to cart1111 from store that doesn't exist
        self.assertRaises(Exception,
                          lambda: self.__market.addProductToCart(self.__member1, self.__storeId1, self.__product1.getProductId(), 10))
        self.test_createStore()
        # try to add product that doesn't exist in the store
        self.assertRaises(Exception,
                          lambda: self.__market.addProductToCart(self.__member1, self.__storeId1, self.__product1.getProductId(), 10))

        self.assertTrue(self.__market.addProductToStore(self.__storeId1, self.__member1, self.__product1))
        self.__market.addProductQuantityToStore(self.__storeId1, self.__member1, self.__product1.getProductId(), 100)
        # try to buy product that doesn't have in stock
        self.assertRaises(Exception,
                          lambda: self.__market.addProductToCart(self.__member1, self.__storeId1, self.__product1.getProductId(),
                                                                 110))

    def test_removeProductFromCart(self):  ##WORKING
        self.test_addProductToCart()
        self.assertTrue(self.__market.removeProductFromCart(self.__storeId1, self.__member1, self.__product1.getProductId()))


    def test_purchaseCart(self):  ##WORKING
        self.test_addProductToCart()
        self.assertTrue(self.__market.purchaseCart(self.__member1, self.__bank1))
        # trans = self.__member1.getTransactionById(2)


        # print("\n")
        # for storeId in trans.getStoreTransactions().keys():
        #     print(trans.getStoreTransactions()[storeId].printPurchaseHistoryInformation())

    def test_removeStore(self): ##WORKING
        self.test_createStore()
        self.assertTrue(self.__market.removeStore(self.__storeId1, self.__member1))

    def test_recreateStore(self):   ##WORKING
        self.test_createStore()
        self.assertTrue(self.__market.removeStore(self.__storeId1, self.__member1))
        self.assertTrue(self.__market.recreateStore(self.__storeId1, self.__member1))


    def tearDown(self):
        self.__address1.removeAddress()
        self.__address2.removeAddress()
        self.__address3.removeAddress()
        self.__bank1.removeBank()
        self.__bank2.removeBank()
        self.__bank3.removeBank()
        self.__member1.removeMember()
        self.__member2.removeMember()
        self.__member3.removeMember()

        self.__store.removeStore()
        self.__store2.removeStore()

        self.__product1.removeProduct()
        self.__product2.removeProduct()
        self.__product3.removeProduct()


if __name__ == '__main__':
    unittest.main()
