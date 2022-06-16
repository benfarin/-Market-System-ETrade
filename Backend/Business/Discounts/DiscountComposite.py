import zope

from Backend.Business.Discounts.CategoryDiscount import CategoryDiscount
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.Discounts.StoreDiscount import StoreDiscount
from Backend.Interfaces.IDiscount import IDiscount
from ModelsBackend.models import DiscountModel


@zope.interface.implementer(IDiscount)
class DiscountComposite:

    # discountTypes: max = 1, add = 2, xor = 3
    def __init__(self, discountId=None, discount1=None, discount2=None, discountType=None, decide=None, model=None):
        if model is None:
            self.__model = DiscountModel.objects.get_or_create(discountID=discountId, dID1=discount1.getModel(),
                                                               dID2=discount2.getModel(),
                                                               composite_type=discountType, decide=decide,
                                                               type='Composite')[0]
            self.__discountId = discountId
            self.__discount1 = discount1
            self.__discount2 = discount2
            self.__discountType = discountType
            self.__decide = decide
        else:
            self.__model = model
            self.__discountId = model.discountID
            self.__discount1 = self.__buildDiscountObject(model.dID1)
            self.__discount2 = self.__buildDiscountObject(model.dID2)
            self.__discountType = model.composite_type
            self.__decide = model.decide

    def calculate(self, bag):
        # discount1 = self.__buildDiscountObject(self.__model.dID1)
        # discount2 = self.__buildDiscountObject(self.__model.dID2)
        if self.__discountType == 'Max':
            totalPrice1 = self.__discount1.getTotalPrice(bag)
            totalPrice2 = self.__discount2.getTotalPrice(bag)
            if totalPrice1 <= totalPrice2:
                return self.__discount1.calculate(bag)
            else:
                return self.__discount2.calculate(bag)
        if self.__discountType == 'Add':
            calc1 = self.__discount1.calculate(bag)
            calc2 = self.__discount2.calculate(bag)
            newPrices = {}
            for prod in bag.getProducts():
                newPrices[prod] = calc1.get(prod) + calc2.get(prod)
            return newPrices
        if self.__discountType == 'XOR':
            check1 = self.__discount1.check(bag)
            check2 = self.__discount2.check(bag)
            calc1 = self.__discount1.calculate(bag)
            calc2 = self.__discount2.calculate(bag)

            if check1 and not check2:
                return calc1
            if check2 and not check1:
                return calc2
            if check1 and check2:
                if self.__decide == 1:
                    return calc1
                elif self.__decide == 2:
                    return calc2
                else:
                    raise Exception("no such decide number")
            else:
                return self.__discount1.calculate(bag)  # doesnt realy matter
        else:
            raise Exception("no such discount type")

    def check(self, bag):
        # discount1 = self.__buildDiscountObject(self.__model.dID1)
        # discount2 = self.__buildDiscountObject(self.__model.dID2)
        return self.__discount1.check(bag) and self.__discount2.check(bag)

    def getTotalPrice(self, bag):
        # discount1 = self.__buildDiscountObject(self.__model.dID1)
        # discount2 = self.__buildDiscountObject(self.__model.dID2)
        return self.__discount1.getTotalPrice(bag) + self.__discount2.getTotalPrice(bag)

    def getAllDiscountRules(self):
        # discount1 = self.__buildDiscountObject(self.__model.dID1)
        # discount2 = self.__buildDiscountObject(self.__model.dID2)
        rules = []
        for rule in self.__discount1.getAllDiscountRules():
            rules.append(rule)
        for rule in self.__discount2.getAllDiscountRules():
            rules.append(rule)
        return rules

    def getDiscountId(self):
        return self.__discountId
        # return self.__model.discountID

    def getDiscount1(self):
        return self.__discount1
        # return self.__buildDiscountObject(self.__model.dID1)

    def getDiscount2(self):
        return self.__discount2
        # return self.__buildDiscountObject(self.__model.dID2)

    def getDiscountType(self):
        return self.__discountType
        # return self.__model.composite_type

    def getClassType(self):
        return 'Composite'
        # return self.__model.type

    def getDecide(self):
        return self.__decide
        # return self.__model.decide

    def isComp(self):
        return True

    def __buildDiscountObject(self, discount_model):
        if discount_model.type == 'Product':
            return ProductDiscount(model=discount_model)
        elif discount_model.type == 'Category':
            return CategoryDiscount(model=discount_model)
        elif discount_model.type == 'Store':
            return StoreDiscount(model=discount_model)
        else:
            return DiscountComposite(model=discount_model)

    def remove(self):
        if self.__discount1 is not None:
            # discount1 = self.__buildDiscountObject(self.__model.dID1)
            self.__discount1.remove()
        if self.__discount2 is not None:
            # discount2 = self.__buildDiscountObject(self.__model.dID2)
            self.__discount2.remove()
        self.__discount1 = None
        self.__discount2 = None
        self.__model.delete()

    def getModel(self):
        return self.__model

    def __eq__(self, other):
        return isinstance(other, DiscountComposite) and self.__model == other.getModel()

    def __hash__(self):
        return hash(self.__discountId)