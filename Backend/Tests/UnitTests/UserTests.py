import unittest
from Backend.Business.Address import Address
from Backend.Business.Bank import Bank
from Backend.Business.Managment.UserManagment import UserManagment
from Backend.Business.UserPackage.Guest import Guest
from Backend.Business.UserPackage.Member import Member
from Backend.Interfaces.IUser import IUser
from Backend.Business.UserPackage.User import User


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.__userManager: IUser = UserManagment().getInstance()
        self.__address1 = Address("Lebanon","beirut","gurion 14",34,95238)
        self.__address2 = Address("Jordan", "rabat amon", "beni 14", 3, 325)
        self.__bank1 = Bank(235235,213)
        self.__bank2 = Bank(643,2215)

        self.guest1 = Guest()
        self.member1 = Member("Ori", "1234", "0500000000", self.__address1, self.__bank1)


    def test_memberSignUp(self):
        self.__userManager.memberSignUp("shalom","123456","089702342",self.__address1,self.__bank1)
        self.assertTrue(len(self.__userManager.getMembers()) > 0)

    def test_loginMember(self):
        self.assertEqual(self.__userManager.memberLogin(self.guest1.getUserID(), "Ori","1234"), self.member1)

    def tearDown(self):
        self.__address1.removeAddress()
        self.__address2.removeAddress()
        self.__bank1.removeBank()
        self.__bank2.removeBank()
        self.guest1.removeUser()
        self.member1.removeUser()




if __name__ == '__main__':
    unittest.main()
