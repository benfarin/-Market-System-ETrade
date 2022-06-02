import unittest
from Backend.Business.Address import Address
from Backend.Business.Bank import Bank
from Backend.Business.Managment.UserManagment import UserManagment
from Backend.Interfaces.IUser import IUser
from Backend.Business.UserPackage.User import User


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.__userManager: IUser = UserManagment().getInstance()
        self.__address1 = Address("Lebanon","beirut","gurion 14",34,95238)
        self.__address2 = Address("Jordan", "rabat amon", "beni 14", 3, 325)
        self.__bank1 = Bank(235235,213)
        self.__bank2 = Bank(643,2215)

        self.user_1 = User()
        self.user_2 = User()


    def test_memberSignUp(self):
        self.__userManager.memberSignUp("shalom","123456","089702342",self.__address1,self.__bank1,None)
        self.assertTrue(len(self.__userManager.getMembers()) > 0)

    def test_loginMember(self):
        self.__userManager.memberSignUp("shalom","123456","089702342",self.__address1,self.__bank1,None)
        self.__userManager.systemManagerSignUp("bar","123","089362716",self.__address2,self.__bank2)
        self.assertEqual(self.__userManager.memberLogin("shalom","123456"), "member logged in succesfully!")

    def tearDown(self):
        self.__address1.removeAddress()
        self.__address2.removeAddress()
        self.__bank1.removeBank()
        self.__bank2.removeBank()
        self.user_1.removeUser()
        self.user_2.removeUser()




if __name__ == '__main__':
    unittest.main()
