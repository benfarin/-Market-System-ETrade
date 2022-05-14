import sys

from  Business.DiscountRules import DiscountRules
from Business.StorePackage.Store import Store
from Business.DiscountPackage.DiscountManagement import DiscountManagement
from Business.DiscountPackage.DiscountInfo import DiscountInfo
from os import system
from Business.DiscountPackage.DiscountsRelation import DiscountRelation
from datetime import date
class requestNewConditionDiscount:


    def __init__(self,counter, functionName, userID, storeId, discountRelation: DiscountRelation,discountId1, discountId2, decide, originalDiscountID)
        self.__counter = counter
        self.__function_name = functionName
        self.__userID = userID
        self.__store_ID = storeId
        self.__discountRelation = discountRelation
        self.__origin_discount_id = originalDiscountID
        self.__decide = decide
        self.__discountID1 = discountId1
        self.__discountID2 = discountId2


    def applyFunction(self, store:Store):
        discountRule= DiscountRules.getInstance()
        discount_id = discountRule.GenerateConditionalDiscounts(store,self.__userID, self.__discountRelation, self.__store_ID, self.__discountID1, self.__discountID2, self.__decide, self.__origin_discount_id)
        discount_info : DiscountInfo = DiscountInfo(discount_id, self.__userID, self.__store_ID, self.__discount_type, 'simple', self.__percent, self.__catagory, self.__product_id, sys.maxsize, 0, date.today(), date.today() )
        manager : DiscountManagement = marketRuleService.getInstance().getDiscountManage()
        manager.addDiscount(discount_info)