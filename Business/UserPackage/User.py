from Business.StorePackage.Cart import Cart
from Business.StorePackage.Bag import Bag
from Payment.PaymentStatus import PaymentStatus
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
        if self._cart.isEmpty() or self._cart.checkPolicy() == False :
            return False
        sum_to_pay = self._cart.calcSum()
        purchaseStatus : PaymentStatus = self._cart.purchase(self.__id,bank,phone,address,sum_to_pay)
        #history should added here
        return purchaseStatus.status



    def updateProductInCart(self, storeId, productId, quantity):
        self._cart.updateProduct(storeId,productId,quantity)
    def removeProduct(self, storeId, productId):
        self._cart.removeProduct(storeId,productId)

    def addProduct(self, storeId, product, quantity):
        self._cart.addProduct( storeId, product, quantity)









