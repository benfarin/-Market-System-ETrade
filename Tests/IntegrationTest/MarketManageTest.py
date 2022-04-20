import unittest
from Business.MarketManage import MarketManage
from interfaces.IMarket import IMarket


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.__market  = MarketManage()
        self.__storeID = self.__market.createStore("ssss",0,0,0)
        self.__assigner = self.__market.addMember()

    def test_addProductQuantityToStore(self):
        self.__market.appointOwnerToStore(self.__storeID,2132121,3123)
        self.assertTrue(3123 in self.__market.getStores().get(12312).getStoreOwners())

if __name__ == '__main__':
    unittest.main()
