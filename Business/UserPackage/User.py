from Business.StorePackage.Cart import Cart
from Business.Histories.UserHistory import UserHistory
from Business.StorePackage.Bag import Bag
import uuid
class User:
    def __init__(self):
        self._shoppingCart = Cart()
        self.__id = str(uuid.uuid4()) # unique id


    def getUserID(self):
        return self.__id

    def getShoppingCart(self):
        return self._shoppingCart

    def getShopingCartProducts(self):
        return self.__shoppingCart.getAllProduct()

    def editProductInStoreBag(self, store, product, quantity): #store Istore ,Product Iproduct , quantity int
        storeBag = self.__shoppingCart.getBag(store) #have to check
        storeBag.editProduct(product, quantity)

    def userPurchaseCart(self, bank, phone , address): # bank - Bank , phone - string , address ->Address
        pass








