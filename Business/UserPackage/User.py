from Business.StorePackage.Cart import Cart
from Business.StorePackage.Bag import Bag
import uuid
class User:
    def __init__(self):
        self.__id = str(uuid.uuid4()) # unique id
        self._cart = Cart(self.__id)
        self._memberCheck = False


    def getUserID(self):
        return self.__id

    def getCart(self):
        return self._cart

    def getMemberCheck(self):
        return self.__memberCheck
    def setICart(self,icart):
        self._cart=icart

    def setMemberCheck(self,state):
        self.__memberCheck = state

    def getShopingCartProducts(self):
        return self._cart.getAllProduct()

    def userPurchaseCart(self, bank, phone , address): # bank - Bank , phone - string , address ->Address
        pass








