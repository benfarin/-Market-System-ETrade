import zope
from zope.interface import implements
import os, django

from Backend.Interfaces.IBag import IBag

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()
from Backend.Exceptions.CustomExceptions import NoSuchStoreException, NoSuchBagException, NotFoundException
from Backend.Interfaces.ICart import ICart
from Backend.Business.StorePackage.Bag import Bag
from Backend.Business.StorePackage.Product import Product
from typing import Dict

from ModelsBackend.models import CartModel, BagsInCartModel, BagModel


@zope.interface.implementer(ICart)
class Cart:

    def __init__(self, userId=None, model=None):
        # self.__userId = userId
        # self.__bags: Dict[int, Bag] = {}  # storeId : Bag

        if model is None:
            self.__model = CartModel.objects.get_or_create(userid=userId)[0]
            self.__userId = userId
            self.__bags: Dict[int, Bag] = {}  # storeId : Bag
        else:
            self.__model = model
            self.__userId = self.__model.userid
            self.__bags: Dict[int, Bag] = {}  # storeId : Bag
            for model in BagsInCartModel.objects.filter(cart=self.__model):
                bag = self.__buildBag(model)
                self.__bags[bag.getStoreId()] = bag

    # not sure if need the casting - it's for tests now...
    def getUserId(self):
        return int(self.__userId)

    def getAllBags(self):
        return self.__bags

    def getBag(self, storeId):
        try:
            bag = self.__bags[storeId]
            return bag
        except:
            raise NotFoundException("bag from store: " + str(storeId) + "couldn't be found")

    def getBagFromCart(self, cart, bag):
        return BagsInCartModel.objects.filter(cart=cart, bag=bag)[0]

    def removeBag(self, storeId):
        if self.__bags.get(storeId) is not None:
            self.__bags.pop(storeId)
            BagsInCartModel.objects.filter(cart=self.__model, storeID=storeId).delete()
            return True
        else:
            return False

    def cleanBag(self, storeId):
        if self.__bags.get(storeId) is not None:
            self.__bags.get(storeId).cleanBag()
        else:
            raise NoSuchStoreException("storeId does not exists, can't clean the bag from the cart")



    def updateCart(self, cart):
        for bag in cart.getAllBags().values():
            cartBag = self.__buildBag(BagsInCartModel.objects.get(cart=cart.getModel(), storeID=bag.getStoreId()))
            matchingBag = BagsInCartModel.objects.filter(cart=self.__model, storeID=bag.getStoreId())
            if len(matchingBag) == 1:
                bag_to_add = self.__buildBag(BagsInCartModel.objects.get(cart=self.__model, storeID=bag.getStoreId()))
                bag_to_add.addBag(cartBag)
            else:
                newBag = Bag(userId=self.__model.userid, storeId=bag.getStoreId())
                BagsInCartModel.objects.get_or_create(cart=self.__model, bag=newBag.getModel(),
                                                      storeID=bag.getStoreId())
                newBag.addBag(cartBag)


    def updateBag(self, bag):
        if self.__bags.get(bag.getStoreId()) is not None:
            self.__bags[bag.getStoreId()] = bag
            BagsInCartModel.objects.get(cart=self.__model, storeID=bag.getStoreId()).bag = bag.getModel()
            BagsInCartModel.objects.get(cart=self.__model, storeID=bag.getStoreId()).save()
            return True
        else:
            return False



    # def calcSum(self):
    #     s = 0.0
    #     for bag in self.__bags.values():
    #         s += bag.calcSum()
    #     return s

    def calcSumOfBag(self, storeId, discounts):   ###NEED TO CHANGE
        if len(BagsInCartModel.objects.filter(cart=self.__model, storeID=storeId)) != 1:
            raise NotFoundException("there is no bag in storeId: " + str(storeId) + " for this cart")
        bag_model = BagsInCartModel.objects.get(cart=self.__model, storeID=storeId)
        bag = self.__buildBag(bag_model)
        return bag.calcSum(discounts)

    def isEmpty(self):
        for bag in self.__bags.values():
            if not bag.isEmpty():
                return False
        return True

    def addProduct(self, storeId, product, quantity):
        if self.__bags.get(storeId) is None:
            bag = Bag(storeId, self.__userId)
            self.__bags[storeId] = bag
            BagsInCartModel.objects.get_or_create(cart=self.__model, storeID=storeId, bag=bag.getModel())
        self.getBag(storeId).addProduct(product, quantity)

    def removeProduct(self, storeId, productId):
        quantity = self.getBag(storeId).removeProduct(productId)
        if self.getBag(storeId).isEmpty():
            self.removeBag(storeId)
        return quantity

    def updateProduct(self, storeId, productId, quantity):  # quantity can be negative!!!
        if self.__bags.get(storeId) is None:
            raise NoSuchBagException("can't update a product without a bag to his store")
        self.getBag(storeId).updateBag(productId, quantity)
        if self.getBag(storeId).isEmpty():
            self.removeBag(storeId)
        return True

    def cleanCart(self):
        for bag in self.__bags.values():
            bag.cleanBag()

    def getAllProductsByStore(self):
        products: Dict[int, Dict[Product, int]] = {}  # [storeId: [product : quantity]]
        for bag in self.__bags.values():
            products.update({bag.getStoreId(): bag.getProducts()})
        return products

    def getAllProducts(self):
        products: Dict[Product, int] = {}  # [product : quantity]
        for bag in self.__bags.values():
            products.update(bag.getProducts())
        return

    def printBags(self):
        printBags = ""
        for bag in self.__bags.values():
            printBags += "\n\t\t\tStore id:" + str(
                bag.getStoreId()) + " store products:" + "\t\t\t\t\t\t\t\t\t" + bag.printProducts()
        return printBags

    # def applyDiscount(self, bag: Bag):
    #     bag.applyDiscount()

    def __buildBag(self, bagInCartModel):
        return Bag(model=bagInCartModel.bag)

    def getModel(self):
        return self.__model

    def removeCart(self):
        for bagInCartModel in BagsInCartModel.objects.filter(cart=self.__model):
            bag = self.__buildBag(bagInCartModel)
            bag.removeBag()
        for bagModel in BagModel.objects.filter(userId=self.__model.userid):
            bag = Bag(model=bagModel)
            bag.removeBag()
        self.__model.delete()

    def __eq__(self, other):
        return isinstance(other, Cart) and self.__model == other.getModel()

    def __hash__(self):
        return hash(self.__model.userid)

