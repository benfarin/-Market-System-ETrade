from Business.UserPackage.User import User



class Member(User):
    def __init__(self, userName, password, phone, address, bank):
        super().__init__() # extend the constructor of user class
        self.__isLoggedIn = False
        self.__userName = userName #string
        self.__password = password #string
        self.__phone = phone # string
        self.__address = address #type address class
        self.__bank = bank # type bank


    def setLoggedIn(self,state):
        self.__isLoggedIn = state

    def addProductRating(self, productID, rating):
        pass

    def getPassword(self):
        return self.__password

    def getUserName(self):
        return self.__userName

    def addStoreRating(self, storeID, rating):
        pass

    def getMemberHistory(self):
        return self.__userHistory

    def getMemberHistory(self,nameMember):
        member = self.__membersFromCart.get(self.getUserByName(nameMember))
        return member.getMemberHistory()