import sys

from  Business.DiscountRules import DiscountRules
from Business.StorePackage.Store import Store
from Business.DiscountPackage.DiscountManagement import DiscountManagement
from Business.DiscountPackage.DiscountInfo import DiscountInfo
from datetime import date
class requestNewSimpleDiscount:


    def __init__(self,counter, existingDiscountId, functionName, userID, storeId, discountType, precent, category,productId, originDiscountId)
        self.__counter = counter
        self.__existing_discount_id = existingDiscountId
        self.__function_name = functionName
        self.__userID = userID
        self.__store_ID = storeId
        self.__discount_type = discountType
        self.__percent = precent
        self.__catagory = category
        self.__product_id = productId
        self.__origin_discount_id = originDiscountId

    def applyFunction(self, store:Store):
        discountRule= DiscountRules.getInstance()
        discount_id = discountRule.createSimpleDiscount(store, self.__discount_type, self.__percent, self.__catagory, self.__product_id)
        discount_info : DiscountInfo = DiscountInfo(discount_id, self.__userID, self.__store_ID, self.__discount_type, 'simple', self.__percent, self.__catagory, self.__product_id, sys.maxsize, 0, date.today(), date.today() )
        manager : DiscountManagement = marketRuleService.getInstance().getDiscountManage()
        manager.addDiscount(discount_info)