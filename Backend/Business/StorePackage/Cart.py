import zope
from zope.interface import implements
import os, django

from Backend.Interfaces.IBag import IBag

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()
from Backend.Exceptions.CustomExceptions import NoSuchStoreException, NoSuchBagException
from Backend.Interfaces.ICart import ICart
from Backend.Business.StorePackage.Bag import Bag
from Backend.Business.StorePackage.Product import Product
from typing import Dict

from ModelsBackend.models import CartModel, BagsInCartModel


@zope.interface.implementer(ICart)
class Cart:

    def __init__(self, userId):
        # self.__userId = userId
        # self.__bags: Dict[int, Bag] = {}  # storeId : Bag
        self.__model = CartModel.objects.get_or_create(userid=userId)[0]

    def getUserId(self):
        return self.__model.userid

    def getAllBags(self):
        return [self.__buildBag(bag) for bag in BagsInCartModel.objects.filter(cart=self.__model)]

    def getBag(self, storeId):
        try:
            bag_model = BagsInCartModel.objects.get(cart=self.__model, storeID=storeId)
            return self.__buildBag(bag_model)
        except:
            raise NoSuchStoreException("storeId does not exists, can't add the bag to the cart")

    def getBagFromCart(self, cart, bag):
        return BagsInCartModel.objects.filter(cart=cart, bag=bag)[0]

    def removeBag(self, storeId):
        if BagsInCartModel.objects.filter(cart=self.__model, storeID=storeId).exists():
            BagsInCartModel.objects.filter(cart=self.__model, storeID=storeId).delete()
            return True
        else:
            return False

    def cleanBag(self, storeId):
        if BagsInCartModel.objects.filter(cart=self.__model, storeID=storeId).exists():
            bag_model = BagsInCartModel.objects.get(cart=self.__model, storeID=storeId)
            self.__buildBag(bag_model).cleanBag()
        else:
            raise NoSuchStoreException("storeId does not exists, can't clean the bag from the cart")

    def updateCart(self, cart):
        for bag in cart.getAllBags():
            if BagsInCartModel.objects.filter(cart=self.__model, storeID=bag.getStoreId()).exists():
                bag_to_add = self.__buildBag(BagsInCartModel.objects.get(cart=self.__model, storeID=bag.getStoreId()))
                bag_to_add.addBag(self.__buildBag(BagsInCartModel.objects.get(cart=cart.getModel(), storeID=bag.getStoreId())))
                # BagsInCartModel.objects.get(cart=self.__model, storeID=bag.getStoreId()).bag = bag_to_add.getModel()
            else:
                BagsInCartModel.objects.get(cart=self.__model, storeID=bag.getStoreId()).bag = \
                    BagsInCartModel.objects.get(cart=cart, storeID=bag.getStoreId()).bag

    def updateBag(self, bag):
        if BagsInCartModel.objects.filter(cart=self.__model, storeID=bag.storeId).exists():
            BagsInCartModel.objects.get(cart=self.__model, storeID=bag.storeId).bag = bag
            BagsInCartModel.objects.get(cart=self.__model, storeID=bag.storeId).save()
            return True
        else:
            return False

    # def calcSum(self):
    #     s = 0.0
    #     for bag in self.__bags.values():
    #         s += bag.calcSum()
    #     return s

    def calcSumOfBag(self, storeId, discounts):
        bag_model = BagsInCartModel.objects.get(cart=self.__model, storeID=storeId)
        bag = self.__buildBag(bag_model)
        return bag.calcSum(discounts)

    def isEmpty(self):
        for bag_model in BagsInCartModel.objects.filter(cart=self.__model):
            bag = self.__buildBag(bag_model)
            if not bag.isEmpty():
                return False
        return True

    def addProduct(self, storeId, product, quantity):
        if not BagsInCartModel.objects.filter(cart=self.__model, storeID=storeId).exists():
            bag = Bag(storeId, self.__model.userid)
            BagsInCartModel.objects.get_or_create(cart=self.__model, storeID=storeId, bag=bag.getModel())
        self.getBag(storeId).addProduct(product, quantity)

    def removeProduct(self, storeId, productId):
        quantity = self.getBag(storeId).removeProduct(productId)
        if self.getBag(storeId).isEmpty():
            self.removeBag(storeId)
        return quantity

    def updateProduct(self, storeId, productId, quantity):  # quantity can be negative!!!
        if not BagsInCartModel.objects.filter(cart=self.__model, storeID=storeId).exists():
            raise NoSuchBagException("can't update a product without a bag to his store")
        self.getBag(storeId).updateBag(productId, quantity)
        if self.getBag(storeId).isEmpty():
            self.removeBag(storeId)
        return True

    def cleanCart(self):
        for bag_model in BagsInCartModel.objects.filter(cart=self.__model):
            bag = self.__buildBag(bag_model)
            bag.cleanBag()

    def getAllProductsByStore(self):
        products: Dict[int, Dict[Product, int]] = {}  # [storeId: [product : quantity]]
        for bag_model in BagsInCartModel.objects.filter(cart=self.__model):
            bag = self.__buildBag(bag_model)
            products.update({bag.getStoreId(): bag.getProducts()})
        return products

    def getAllProducts(self):
        products: Dict[Product, int] = {}  # [product : quantity]
        for bag_model in BagsInCartModel.objects.filter(cart=self.__model):
            bag = self.__buildBag(bag_model)
            products.update(bag.getProducts())
        return products

    def printBags(self):
        printBags = ""
        for bag in self.__bags.values():
            printBags += "\n\t\t\tStore id:" + str(
                bag.getStoreId()) + " store products:" + "\t\t\t\t\t\t\t\t\t" + bag.printProducts()
        return printBags

    # def applyDiscount(self, bag: Bag):
    #     bag.applyDiscount()

    def __buildBag(self, bagModel):
        return Bag(bagModel.bag.storeId, bagModel.bag.userId)

    def getModel(self):
        return self.__model

    def removeCart(self):
        self.__model.delete()
