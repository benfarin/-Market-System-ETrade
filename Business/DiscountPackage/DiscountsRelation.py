class DiscountRelation:

    def __init__(self, userID, discountID, discountRuleRelation, storeID, ID_Discount1, id_Discount2, decide):
        self.__userID = userID
        self.__discountID = discountID
        self.__discountRuleRelation = discountRuleRelation
        self.__storeID = storeID
        self.__id_discount1 = ID_Discount1
        self.__id_discount2 = id_Discount2
        self.__decide = decide

    def getUserID(self):
        return  self.__userID

    def getDiscountID(self):
        return self.__discountID

    def getDiscountRuleRelation(self):
        return self.__discountRuleRelation

    def getStoreID(self):
        return  self.__storeID

    def getIdDiscount1(self):
        return self.__id_discount1

    def getIdDiscount2(self):
        return self.__id_discount2

    def getDecide(self):
        return  self.__decide

    def setUserID(self,uid):
          self.__userID = uid

    def setDiscountID(self, discountID):
         self.__discountID = discountID

    def setDiscountRuleRelation(self, discountRule):
         self.__discountRuleRelation = discountRule

    def setStoreID(self, sid):
          self.__storeID = sid

    def setIdDiscount1(self, discountID1):
         self.__id_discount1 = discountID1

    def setIdDiscount2(self, discountID2):
         self.__id_discount2 = discountID2

    def setDecide(self, decide):
          self.__decide = decide


