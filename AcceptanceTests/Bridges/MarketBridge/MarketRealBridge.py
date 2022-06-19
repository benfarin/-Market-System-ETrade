import zope
from AcceptanceTests.Bridges.MarketBridge.IMarketBridge import IMarketBridge
from Backend.Service.MemberService import MemberService
from Backend.Service.RoleService import RoleService
from Backend.Service.UserService import UserService


@zope.interface.implementer(IMarketBridge)
class MarketRealBridge:
    def __init__(self):
        self._roleService = RoleService()
        self._memberService = MemberService()
        self._userService = UserService()

    def request(self):
        print("RealSubject: Handling request.")

    def search_product_category(self, category):
        return self._userService.getProductByCategory(category, True)

    def search_product_name(self, product_name):
        return self._userService.getProductByName(product_name, True)

    def search_product_keyWord(self, keyWord):
        return self._userService.getProductByKeyword(keyWord, True)

    def search_product_price_range(self, price_min, price_max):
        return self._userService.getProductPriceRange(price_min, price_max, True)

    def get_cart(self, user_id):
        return self._userService.getCart(user_id, True)

    def get_store(self, store_id):
        return self._roleService.getStore(store_id, True)

    def get_all_stores(self):
        return self._roleService.getAllStores(True)

    def get_cart_info(self, user_id):
        return self._userService.getCart(user_id, True)

    def add_product_to_store(self, store_id, user_id, name, price, category, weight, key_words):
        return self._roleService.addProductToStore(store_id, user_id, name, price, category, weight, key_words, True)

    def remove_product_from_store(self, store_id, user_id, prod_id):
        return self._roleService.removeProductFromStore(store_id, user_id, prod_id, True)

    def edit_product_price(self, user_id, store_id, prod_id, new_price):
        return self._roleService.updateProductPrice(user_id, store_id, prod_id, new_price, True)

    def edit_product_Weight(self, user_id, store_id, prod_id, new_weight):
        return self._roleService.updateProductWeight(user_id, store_id, prod_id, new_weight, True)

    def appoint_store_owner(self, store_id, assigner_id, assignee_id):
        return self._roleService.appointOwnerToStore(store_id, assigner_id, assignee_id, True)

    def appoint_store_manager(self, store_id, assigner_id, assignee_id):
        return self._roleService.appointManagerToStore(store_id, assigner_id, assignee_id, True)

    def removeStoreOwner(self, storeId, assignerId, assigneeName):
        return self._roleService.removeStoreOwner(storeId, assignerId, assigneeName, True)

    def set_stock_manager_perm(self, store_id, assigner_id, assignee_id):
        return self._roleService.setStockManagerPermission(store_id, assigner_id, assignee_id, True)

    def set_change_perm(self, store_id, assigner_id, assignee_id):
        return self._roleService.setChangePermission(store_id, assigner_id, assignee_id, True)

    def add_quantity_to_store(self, store_id, user_id, productID, quantity):
        return self._roleService.addProductQuantityToStore(store_id, user_id, productID, quantity, True)

    def get_store_info(self, store_id, user_id):
        return self._roleService.getRolesInformation(store_id, user_id, True)

    def getAllStores(self):
        return self._roleService.getAllStores(True)

    def getUserStore(self,userId):
        return self._roleService.getUserStores(userId, True)

    def edit_product_name(self, user_id, store_id, prod_id, new_name):
        return self._roleService.updateProductName(user_id, store_id, prod_id, new_name, True)

    def edit_product_category(self, user_id, store_id, prod_id, new_category):
        return self._roleService.updateProductCategory(user_id, store_id, prod_id, new_category, True)

    def print_purchase_history(self, store_id, user_id):
        return self._roleService.getPurchaseHistoryInformation(store_id, user_id, True)

    def close_store(self, store_id, user_id):
        return self._memberService.removeStore(store_id, user_id, True)

    def removeStoreForGood(self, user_id, store_id):
        return self._memberService.removeStoreForGood(user_id, store_id, True)

    def addSimpleDiscount_Store(self, userId, storeId, precent):
        return self._roleService.addStoreDiscount(userId, storeId, precent, True)

    def addSimpleDiscount_Category(self, userId, storeId, category,precent):
        return self._roleService.addCategoryDiscount(userId, storeId, category,precent, True)

    def addSimpleDiscount_Product(self, userId, storeId,productId,precent):
        return self._roleService.addProductDiscount(userId, storeId, productId,precent, True)

    def addConditionDiscountAdd(self, userId, storeId, dId1, dId2):
        return self._roleService.addCompositeDiscountAdd(userId, storeId, dId1, dId2, True)

    def addConditionDiscountMax(self, userId, storeId, dId1, dId2):
        return self._roleService.addCompositeDiscountMax(userId, storeId, dId1, dId2, True)

    def addConditionDiscountXor(self, userId, storeId, dId1, dId2, decide):
        return self._roleService.addCompositeDiscountXor(userId, storeId, dId1, dId2, decide, True)

    def removeDiscount(self,  userId, storeId, discountId):
        return self._roleService.removeDiscount(userId, storeId, discountId, True)

    def addStoreTotalAmountDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        return self._roleService.addStoreTotalAmountDiscountRule(userId, storeId, discountId, atLeast, atMost, True)

    def addStoreQuantityDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        return self._roleService.addStoreQuantityDiscountRule(userId, storeId, discountId, atLeast, atMost, True)

    def addCategoryQuantityDiscountRule(self, userId, storeId, discountId, category, atLeast, atMost):
        return self._roleService.addCategoryQuantityDiscountRule(userId, storeId, discountId, category, atLeast, atMost, True)

    def addProductQuantityDiscountRule(self, userId, storeId, discountId, productId, atLeast, atMost):
        return self._roleService.addProductQuantityDiscountRule(userId, storeId, discountId, productId, atLeast, atMost, True)

    def addStoreWeightDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        return self._roleService.addStoreWeightDiscountRule(userId, storeId, discountId, atLeast, atMost, True)

    def addCategoryWeightDiscountRule(self, userId, storeId, discountId, category, atLeast, atMost):
        return self._roleService.addCategoryWeightDiscountRule(userId, storeId, discountId, category, atLeast, atMost, True)

    def addProductWeightDiscountRule(self, userId, storeId, discountId, productId, atLeast, atMost):
        return self._roleService.addProductWeightDiscountRule(userId, storeId, discountId, productId, atLeast, atMost, True)

    def addCompositeRuleDiscountAnd(self, userId, storeId, dId, rId1, rId2):
        return self._roleService.addCompositeRuleDiscountAnd(userId, storeId, dId, rId1, rId2, True)

    def addCompositeRuleDiscountOr(self, userId, storeId, dId, rId1, rId2):
        return self._roleService.addCompositeRuleDiscountOr(userId, storeId, dId, rId1, rId2, True)

    def removeRuleDiscount(self, userId, storeId, dId, rId):
        return self._roleService.removeRuleDiscount(userId, storeId, dId, rId, True)

    # purchase rules
    def addStoreTotalAmountPurchaseRule(self, userId, storeId, atLeast, atMost):
        return self._roleService.addStoreTotalAmountPurchaseRule(userId, storeId, atLeast, atMost, True)

    def addStoreQuantityPurchaseRule(self, userId, storeId, atLeast, atMost):
        return self._roleService.addStoreQuantityPurchaseRule(userId, storeId, atLeast, atMost, True)

    def addCategoryQuantityPurchaseRule(self, userId, storeId, category, atLeast, atMost):
        return self._roleService.addCategoryQuantityPurchaseRule(userId, storeId, category, atLeast,
                                                                  atMost, True)

    def addProductQuantityPurchaseRule(self, userId, storeId, productId, atLeast, atMost):
        return self._roleService.addProductQuantityPurchaseRule(userId, storeId, productId, atLeast,
                                                                 atMost, True)

    def addStoreWeightPurchaseRule(self, userId, storeId, atLeast, atMost):
        return self._roleService.addStoreWeightPurchaseRule(userId, storeId, atLeast, atMost, True)

    def addCategoryWeightPurchaseRule(self, userId, storeId, category, atLeast, atMost):
        return self._roleService.addCategoryWeightPurchaseRule(userId, storeId, category, atLeast, atMost, True)

    def addProductWeightPurchaseRule(self, userId, storeId, productId, atLeast, atMost):
        return self._roleService.addProductWeightPurchaseRule(userId, storeId, productId, atLeast, atMost, True)

    def addCompositeRulePurchaseAnd(self, userId, storeId, rId1, rId2):
        return self._roleService.addCompositeRulePurchaseAnd(userId, storeId, rId1, rId2, True)

    def addCompositeRulePurchaseOr(self, userId, storeId, rId1, rId2):
        return self._roleService.addCompositeRulePurchaseOr(userId, storeId, rId1, rId2, True)

    def removeRulePurchase(self, userId, storeId, rId):
        return self._roleService.removeRulePurchase(userId, storeId, rId, True)

    def appoint_owner_perm(self, store_id, assigner_id, assignee_name):
        return self._roleService.setAppointOwnerPermission(store_id, assigner_id, assignee_name, True)

    def set_roles_info_perm(self, store_id, assigner_id, assignee_name):
        return self._roleService.setRolesInformationPermission(store_id, assigner_id, assignee_name, True)

    def set_purchase_history_info_perm(self, store_id, assigner_id, assignee_name):
        return self._roleService.setPurchaseHistoryInformationPermission(store_id, assigner_id, assignee_name, True)

    def set_discount_perm(self, store_id, assigner_id, assignee_name):
        return self._roleService.setDiscountPermission(store_id, assigner_id, assignee_name, True)

    def remove_member(self, admin_name, member_name):
        return self._roleService.removeMember(admin_name, member_name, True)

    def get_all_store_trans(self, admin_name):
        return self._roleService.getAllStoreTransactions(admin_name, True)

    def get_all_user_trans(self, admin_name):
        return self._roleService.getAllUserTransactions(admin_name, True)

    def get_user_tran(self, admin_name, tran_id):
        return self._roleService.getUserTransaction(admin_name, tran_id, True)

    def get_store_tran_by_store_id(self, admin_name, store_id):
        return self._roleService.getStoreTransactionByStoreId(admin_name, store_id, True)

    def getAllSimpleDiscountOfStore(self, userId, storeId):
        return self._roleService.getAllSimpleDiscountOfStore(userId, storeId, True)

    def getAllCompositeDiscountOfStore(self, userId, storeId):
        return self._roleService.getAllCompositeDiscountOfStore(userId, storeId, True)

    def getAllSimplePurchaseRulesOfStore(self, userId, storeId):
        return self._roleService.getAllSimplePurchaseRulesOfStore(userId, storeId, True)

    def getAllCompositePurchaseRulesOfStore(self, userId, storeId):
        return self._roleService.getAllCompositePurchaseRulesOfStore(userId, storeId, True)

    def getAllSimpleRulesOfDiscount(self, userId, storeId, discountId):
        return self._roleService.getAllSimpleRulesOfDiscount(userId, storeId, discountId, True)

    def getAllCompositeRulesOfDiscount(self, userId, storeId, discountId):
        return self._roleService.getAllCompositeRulesOfDiscount(userId, storeId, discountId, True)

    def reset_management(self):
        return self._userService.resetManagement()

    def getUsersByDates(self, systemManagerName, fromDate, untilDate):
        return self._roleService.getUsersByDates(systemManagerName, fromDate, untilDate, True)












