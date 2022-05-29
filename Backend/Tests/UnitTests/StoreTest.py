import unittest

from Backend.Business.Address import Address
from Backend.Business.Bank import Bank
from Backend.Business.StorePackage.Store import Store
from Backend.Business.UserPackage.Member import Member


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.bank = Bank(0,0)
        self.address = Address("Israel", "Tel-Aviv", "Dizengof", 0, 0)
        self.founder = Member("Test", "1234", "0500000000", self.address, self.bank)
        self.store = Store(0, "TestStore", self.founder, self.bank, self.address)

    def test_store_basic(self):
        self.assertEqual(self.store.getStoreOwners(), [self.founder])  # add assertion here

    def tearDown(self):
        self.founder.removeMember()
        self.store.removeStore()


if __name__ == '__main__':
    unittest.main()
