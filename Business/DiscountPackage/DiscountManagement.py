from Business.DiscountPackage.DiscountInfo import DiscountInfo
from Business.DiscountPackage.DiscountsRelation import DiscountRelation

class DiscountManagement:

    def __init__(self):
        self.__discount_info = []
        self.__discount_realtion = []

    def addDiscount(self, discount_data):
        self.__discount_info.append(discount_data)

    def removeDiscount(self,discount):
        self.__discount_info.remove(discount)
    def getDiscountById(self,discount_id):
        for discount_info in self.__discount_info:
            if discount_info.getIdDiscount() == discount_id:
                return discount_info
        return None

    def addRelation(self, discount_relation):
        self.__discount_realtion.append(discount_relation)

    def removeRelation(self,to_remove):
        self.__discount_realtion.remove(to_remove)

    def getAllDiscountRelation(self, id_store):
        set_discount_relations= []
        for discount_relation in self.__discount_realtion:
            if discount_relation.getStoreID() == id_store:
                set_discount_relations.append(discount_relation)
        return set_discount_relations

    def getAllDiscountInfo(self, id_store):
        set_discount_info = []
        for discount_info in self.__discount_info:
            if discount_info.getStoreID() == id_store:
                set_discount_info.append(discount_info)
        return set_discount_info

    def isComplex(self,discount_id):
        for  discount_info in self.__discount_info:
            if discount_info.getIdDiscount1() == discount_id or discount_info.getIdDiscount2() == discount_id:
                return True
        return  False