import zope

from Backend.Business.Discounts.CategoryDiscount import CategoryDiscount
from Backend.Business.Discounts.ProductDiscount import ProductDiscount
from Backend.Business.Discounts.StoreDiscount import StoreDiscount
from Backend.Interfaces.IDiscount import IDiscount
from ModelsBackend.models import DiscountModel


@zope.interface.implementer(IDiscount)
class DiscountComposite:

    # discountTypes: max = 1, add = 2, xor = 3
    def __init__(self, discountId, discount1, discount2, discountType, decide):
        # self.__discountId = discountId
        # self.__discount1: IDiscount = discount1
        # self.__discount2: IDiscount = discount2
        # self.__discountType = discountType
        # self.__decide = decide
        self.__model = DiscountModel.objects.get_or_create(discountID=discountId, dID1=discount1, dID2=discount2,
                                                           composite_type=discountType, decide=decide,
                                                           type='Composite')[0]

    def calculate(self, bag):
        discount1 = self.__buildDiscountObject(self.__model.dID1)
        discount2 = self.__buildDiscountObject(self.__model.dID2)
        if self.__model.composite_type == 'Max':
            totalPrice1 = discount1.getTotalPrice(bag)
            totalPrice2 = discount2.getTotalPrice(bag)
            if totalPrice1 <= totalPrice2:
                return discount1.calculate(bag)
            else:
                return discount2.calculate(bag)
        if self.__model.composite_type == 'Add':
            calc1 = discount1.calculate(bag)
            calc2 = discount2.calculate(bag)
            newPrices = {}
            for prod in bag.getProducts():
                newPrices[prod] = calc1.get(prod) + calc2.get(prod)
            return newPrices
        if self.__model.composite_type == 'XOR':
            check1 = discount1.check(bag)
            check2 = discount2.check(bag)
            calc1 = discount1.calculate(bag)
            calc2 = discount2.calculate(bag)

            if check1 and not check2:
                return calc1
            if check2 and not check1:
                return calc2
            if check1 and check2:
                if self.__model.decide == 1:
                    return calc1
                elif self.__model.decide == 2:
                    return calc2
                else:
                    raise Exception("no such decide number")
            else:
                return discount1.calculate(bag)  # doesnt realy matter
        else:
            raise Exception("no such discount type")

    def getDiscountId(self):
        return self.__model.discountID

    def getDiscount1(self):
        return self.__model.dID1.discountID

    def getDiscount2(self):
        return self.__model.dID2.discountID

    def getDiscountType(self):
        return self.__model.composite_type

    def __buildDiscountObject(self, discount_model):
        if discount_model.type == 'Product':
            return ProductDiscount(discount_model.discountID, discount_model.productID, discount_model.percent)
        elif discount_model.type == 'Category':
            return CategoryDiscount(discount_model.discountID, discount_model.category, discount_model.percent)
        else:  # discount_model.type == 'Store'
            return StoreDiscount(discount_model.discountID, discount_model.percent)


    def remove(self):
        self.__model.delete()