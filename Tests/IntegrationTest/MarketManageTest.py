import unittest

from Business.Address import Address
from Business.Bank import Bank
from Business.Market import Market
from Business.StorePackage.Product import Product
from Business.StorePackage.Store import Store
from Business.UserPackage.Member import Member
from interfaces.IMarket import IMarket
from interfaces.IStore import IStore


class MyTestCase(unittest.TestCase):
    def setUp(self):
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
        self.__store3 : IStore = self.__market.createStore("foot-locker", self.__member1.getUserID(), self.__bank1,self.__address2)
        self.__product1 : Product = Product(1,"milk",75,"halavi","ff")
        self.__market.addProductToStore(self.__store3.getStoreId(),self.__member1.getUserID(),self.__product1)
        self.__market.addProductQuantityToStore(self.__store3.getStoreId(),self.__member1.getUserID(),self.__product1.getProductId(),100)


    def test_addActiveUser(self):
        self.assertTrue(self.__market.addActiveUser(self.__member1))

    def test_createStore(self):
        self.__market.addActiveUser(self.__member1)
        store1 : IStore = self.__market.createStore("foot-locker",self.__member1.getUserID(),self.__bank1,self.__address2)
        store2 : IStore = self.__market.getStoreById(store1.getStoreId())
        storeID = store2.getStoreId()
        self.assertEqual( storeID, store1.getStoreId())

    def test_addProductToCart(self):
        # store initial with 100 products!
        self.assertTrue(self.__market.addProductToCart(self.__member1.getUserID(),self.__store3.getStoreId(),self.__product1.getProductId(),7))
        self.assertRaises(Exception, lambda: self.__market.addProductToCart(self.__member1.getUserID(),self.__store3.getStoreId(),self.__product1.getProductId(),100))

    def test_removeProductFromCart(self):
        self.__market.addProductToCart(self.__member1.getUserID(), self.__store3.getStoreId(),
                                       self.__product1.getProductId(), 7)
        self.assertTrue(self.__market.removeProductFromCart(self.__store3.getStoreId(),self.__member1.getUserID(),self.__product1.getProductId()))

    def test_updateProductFromCart(self):
        #self.__market.addProductToCart(self.__member1.getUserID(), self.__store3.getStoreId(),
         #                              self.__product1.getProductId(), 7)
        #self.assertTrue(self.__market.updateProductFromCart(self.__member1.getUserID(),self.__store3.getStoreId(),self.__product1.getProductId(),99))
        pass
    def test_appointManagerToStore(self):
       # self.assertTrue(self.__market.appointManagerToStore(self.__store3.getStoreId(),self.__member1.getUserID(),self.__member2.getUserID()))
        self.assertRaises(Exception,lambda: self.__market.appointManagerToStore(self.__store3.getStoreId(),self.__member2.getUserID(),self.__member1.getUserID()))

if __name__ == '__main__':
    unittest.main()
