import zope
from zope.interface import implements

import os, django
from Backend.Business.StorePackage.Product import Product

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()

from Backend.Exceptions.CustomExceptions import QuantityException, ProductException, NotFoundException
from Backend.Interfaces.IBag import IBag
from ModelsBackend.models import BagModel, ProductsInBagModel, ProductModel


@zope.interface.implementer(IBag)
class Bag:

    def __init__(self, storeId=None, userId=None, model=None):
        # self.__storeId = storeId
        # self.__products = {}  # product : quantity
        if model is None:
            self.__b = BagModel.objects.get_or_create(storeId=storeId, userId=userId)[0]
        else:
            self.__b = model

    def getStore(self):
        pass

    def isEmpty(self):
        return not ProductsInBagModel.objects.filter(bag_ID=self.__b).exists()

    def getStoreId(self):
        return self.__b.storeId

    def getBag(self):
        return self

    def addProduct(self, product, quantity):
        if quantity <= 0:
            raise QuantityException("cannot add negative quantity of product")
        check = ProductsInBagModel.objects.filter(bag_ID=self.__b, product_ID=product.getModel())
        if len(check) > 1:
            raise Exception("there is more then one product with that id in this bag!")
        if not check.exists():
            ProductsInBagModel.objects.get_or_create(bag_ID=self.__b, product_ID=product.getModel(), quantity=quantity)
            return True
        p = check[0]
        p.quantity += quantity
        p.save()
        return True

    def removeProduct(self, productId):
        for product in ProductsInBagModel.objects.filter(bag_ID=self.__b):
            if product.product_ID.product_id == productId:
                quantity = product.quantity
                ProductsInBagModel.objects.get(bag_ID=self.__b, product_ID=product.product_ID,
                                               quantity=quantity).delete()
                return quantity
        raise ProductException("no such product in the Bag")

    def updateBag(self, productId, quantity):
        for product in ProductsInBagModel.objects.filter(bag_ID=self.__b):
            if product.product_ID.product_id == productId:
                product.quantity += quantity
                product.save()
                if product.quantity <= 0:
                    ProductsInBagModel.objects.get(bag_ID=self.__b, product_ID=product.product_ID.product_id).delete()
                return True
        raise ProductException("no such product in the Bag")

    def getProducts(self):
        products = {}
        for prod in ProductsInBagModel.objects.filter(bag_ID=self.__b):
            product = self._buildProduct(prod.product_ID)
            products[product] = prod.quantity
        return products

    def addBag(self, bag):
        for product in ProductsInBagModel.objects.filter(bag_ID=bag.getModel()):

            productInBag = self.checkSameProduct(product)
            if productInBag is not None:
                productInBag.quantity += ProductsInBagModel.objects.get(bag_ID=bag.getModel(),
                                                                        product_ID=product.product_ID.product_id).quantity
                productInBag.save()
            else:
                if len(ProductModel.objects.filter(product_id=product.product_ID.product_id)) != 1:
                    raise NotFoundException("product: " + str(product.product_ID.product_id) + "has not found")

                p = ProductModel.objects.get(product_id=product.product_ID.product_id)
                newProduct = ProductsInBagModel.objects.get_or_create(bag_ID=self.__b, product_ID=p,
                                                                      quantity=product.quantity)
                newProduct[0].save()
        return True

    def checkSameProduct(self, product):
        for p in ProductsInBagModel.objects.filter(bag_ID=self.__b):
            if product.product_ID == p.product_ID:
                return p
        return None

    def getProductQuantity(self, product):
        try:
            return ProductsInBagModel.objects.get(bag_ID=self.__b, product_ID=product.getModel()).quantity
        except:
            raise NotFoundException("product: " + str(product.getProductId()) + "has not found")

    def getProductQuantityByProductId(self, productId):
        if len(ProductModel.objects.filter(product_id=productId)) != 1:
            raise NotFoundException("product: " + str(productId) + "has not found")
        product = self._buildProduct(ProductModel.objects.get(product_id=productId))
        return self.getProductQuantity(product)

    def calcSum(self, discounts):
        return self.applyDiscount(discounts)

    def cleanBag(self):
        ProductsInBagModel.objects.filter(bag_ID=self.__b).delete()

    def printProducts(self):
        products_print = ""
        for product in ProductsInBagModel.objects.filter(bag_ID=self.__b):
            products_print += "\n\t\t\tid product:" + str(product.product_ID.product_id) + " name:" + str(
                product.product_ID.name) + " quantity:" + str(product.quantity)
        return products_print

    def __searchProductByProductId(self, pId):
        for product in ProductsInBagModel.objects.filter(bag_ID=self.__b):
            if product.product_ID == pId:
                return product
        return None

    def applyDiscount(self, discounts):
        if discounts is None:
            return self.calc()
        minPrice = float('inf')
        for discount in discounts:
            newPrice = self.calcWithDiscount(discount.calculate(self))
            if newPrice < minPrice:
                minPrice = newPrice
        if minPrice < float('inf'):
            return minPrice
        else:
            return self.calc()
        # if discounts is None or discounts == {}:
        #     return self.calc()
        # minPrice = float('inf')
        # for discount in discounts.values():
        #     newPrice = self.calcWithDiscount(discount.calculate(self))
        #     if newPrice < minPrice:
        #         minPrice = newPrice
        # if minPrice < float('inf'):
        #     return minPrice
        # else:
        #     return self.calc()

    def calcWithDiscount(self, discount_of_product):
        s = 0
        for prod in discount_of_product:
            first = (1 - discount_of_product[prod])
            second = ProductsInBagModel.objects.get(bag_ID=self.__b, product_ID=prod.getModel()).quantity
            third = prod.getProductPrice()
            s += first * second * third

        return s

    def calc(self):
        s = 0.0
        for product in ProductsInBagModel.objects.filter(bag_ID=self.__b):
            s += product.product_ID.price * product.quantity
        return s

    def getModel(self):
        return self.__b

    def _buildProduct(self, model):
        return Product(model=model)

    def removeBag(self):
        for productInBag in ProductsInBagModel.objects.filter(bag_ID=self.__b):
            productInBag.delete()
        self.__b.delete()

    def __eq__(self, other):
        return isinstance(other, Bag) and self.__b == other.getModel()

    def __hash__(self):
        return hash(self.__b.storeId and self.__b.userId)

