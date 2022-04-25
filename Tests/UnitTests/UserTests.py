import unittest
from Business.Address import Address
from Business.Bank import Bank
from Business.Managment.UserManagment import UserManagment
from interfaces.IUser import IUser


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.__userManager: IUser = UserManagment().getInstance()
        self.__address1 = Address("Lebanon","beirut","gurion 14",34,95238)
        self.__address2 = Address("Jordan", "rabat amon", "beni 14", 3, 325)
        self.__bank1 = Bank(235235,213)
        self.__bank2 = Bank(643,2215)



    def test_memberSignUp(self):
       self.__userManager.memberSignUp("shalom","123456","089702342",self.__address1,self.__bank1,None)



if __name__ == '__main__':
    unittest.main()
