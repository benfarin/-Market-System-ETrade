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
        return self._userService.getProductByCategory(category)

    def search_product_name(self, product_name):
        return self._userService.getProductByName(product_name)

    def search_product_keyWord(self, keyWord):
        return self._userService.getProductByKeyword(keyWord)

    def search_product_price_range(self, price_min, price_max):
        return self._userService.getProductPriceRange(price_min, price_max)

    def get_cart(self, user_id):
        return self._userService.getCart(user_id)

    def get_store(self, store_id):
        return self._roleService.getStore(store_id)

    def get_all_stores(self):
        return self._roleService.getAllStores()

    def get_cart_info(self, user_id):
        return self._userService.getCart(user_id)

    def add_product_to_store(self, store_id, user_id, name, price, category, weight, key_words):
        return self._roleService.addProductToStore(store_id, user_id, name, price, category, weight, key_words)

    def remove_product_from_store(self, store_id, user_id, prod_id):
        return self._roleService.removeProductFromStore(store_id, user_id, prod_id)

    def edit_product_price(self, user_id, store_id, prod_id, new_price):
        return self._roleService.updateProductPrice(user_id, store_id, prod_id, new_price)

    def edit_product_Weight(self, user_id, store_id, prod_id, new_weight):
        return self._roleService.updateProductWeight(user_id, store_id, prod_id, new_weight)

    def appoint_store_owner(self, store_id, assigner_id, assignee_id):
        return self._roleService.appointOwnerToStore(store_id, assigner_id, assignee_id)

    def appoint_store_manager(self, store_id, assigner_id, assignee_id):
        return self._roleService.appointManagerToStore(store_id, assigner_id, assignee_id)

    def removeStoreOwner(self, storeId, assignerId, assigneeName):
        return self._roleService.removeStoreOwner(storeId, assignerId, assigneeName)

    def set_stock_manager_perm(self, store_id, assigner_id, assignee_id):
        return self._roleService.setStockManagerPermission(store_id, assigner_id, assignee_id)

    def set_change_perm(self, store_id, assigner_id, assignee_id):
        return self._roleService.setChangePermission(store_id, assigner_id, assignee_id)

    def add_quantity_to_store(self, store_id, user_id, productID, quantity):
        return self._roleService.addProductQuantityToStore(store_id, user_id, productID, quantity)

    def get_store_info(self, store_id, user_id):
        return self._roleService.getRolesInformation(store_id, user_id)

    def getAllStores(self):
        return self._roleService.getAllStores()

    def getUserStore(self,userId):
        return self._roleService.getUserStores(userId)

    def edit_product_name(self, user_id, store_id, prod_id, new_name):
        return self._roleService.updateProductName(user_id, store_id, prod_id, new_name)

    def edit_product_category(self, user_id, store_id, prod_id, new_category):
        return self._roleService.updateProductCategory(user_id, store_id, prod_id, new_category)

    def print_purchase_history(self, store_id, user_id):
        return self._roleService.getPurchaseHistoryInformation(store_id, user_id)

    def close_store(self, store_id, user_id):
        return self._memberService.removeStore(store_id, user_id)

    def addSimpleDiscount_Store(self, userId, storeId, precent):
        return self._roleService.addStoreDiscount(userId, storeId, precent)

    def addSimpleDiscount_Category(self, userId, storeId, category,precent):
        return self._roleService.addCategoryDiscount(userId, storeId, category,precent)

    def addSimpleDiscount_Product(self, userId, storeId,productId,precent):
        return self._roleService.addProductDiscount(userId, storeId, productId,precent)

    def addConditionDiscountAdd(self, userId, storeId, dId1, dId2):
        return self._roleService.addCompositeDiscountAdd(userId, storeId, dId1, dId2)

    def addConditionDiscountMax(self, userId, storeId, dId1, dId2):
        return self._roleService.addCompositeDiscountMax(userId, storeId, dId1, dId2)

    def addConditionDiscountXor(self, userId, storeId, dId1, dId2, decide):
        return self._roleService.addCompositeDiscountXor(userId, storeId, dId1, dId2, decide)

    def removeDiscount(self,  userId, storeId, discountId):
        return self._roleService.removeDiscount(userId, storeId, discountId)

    def addStoreTotalAmountDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        return self._roleService.addStoreTotalAmountDiscountRule(userId, storeId, discountId, atLeast, atMost)

    def addStoreQuantityDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        return self._roleService.addStoreQuantityDiscountRule(userId, storeId, discountId, atLeast, atMost)

    def addCategoryQuantityDiscountRule(self, userId, storeId, discountId, category, atLeast, atMost):
        return self._roleService.addCategoryQuantityDiscountRule(userId, storeId, discountId, category, atLeast, atMost)

    def addProductQuantityDiscountRule(self, userId, storeId, discountId, productId, atLeast, atMost):
        return self._roleService.addProductQuantityDiscountRule(userId, storeId, discountId, productId, atLeast, atMost)

    def addStoreWeightDiscountRule(self, userId, storeId, discountId, atLeast, atMost):
        return self._roleService.addStoreWeightDiscountRule(userId, storeId, discountId, atLeast, atMost)

    def addCategoryWeightDiscountRule(self, userId, storeId, discountId, category, atLeast, atMost):
        return self._roleService.addCategoryWeightDiscountRule(userId, storeId, discountId, category, atLeast, atMost)

    def addProductWeightDiscountRule(self, userId, storeId, discountId, productId, atLeast, atMost):
        return self._roleService.addProductWeightDiscountRule(userId, storeId, discountId, productId, atLeast, atMost)

    def addCompositeRuleDiscountAnd(self, userId, storeId, dId, rId1, rId2):
        return self._roleService.addCompositeRuleDiscountAnd(userId, storeId, dId, rId1, rId2)

    def addCompositeRuleDiscountOr(self, userId, storeId, dId, rId1, rId2):
        return self._roleService.addCompositeRuleDiscountOr(userId, storeId, dId, rId1, rId2)

    def removeRuleDiscount(self, userId, storeId, dId, rId):
        return self._roleService.removeRuleDiscount(userId, storeId, dId, rId)

    # purchase rules
    def addStoreTotalAmountPurchaseRule(self, userId, storeId, atLeast, atMost):
        return self._roleService.addStoreTotalAmountPurchaseRule(userId, storeId, atLeast, atMost)

    def addStoreQuantityPurchaseRule(self, userId, storeId, atLeast, atMost):
        return self._roleService.addStoreQuantityPurchaseRule(userId, storeId, atLeast, atMost)

    def addCategoryQuantityPurchaseRule(self, userId, storeId, category, atLeast, atMost):
        return self._roleService.addCategoryQuantityPurchaseRule(userId, storeId, category, atLeast,
                                                                  atMost)

    def addProductQuantityPurchaseRule(self, userId, storeId, productId, atLeast, atMost):
        return self._roleService.addProductQuantityPurchaseRule(userId, storeId, productId, atLeast,
                                                                 atMost)

    def addStoreWeightPurchaseRule(self, userId, storeId, atLeast, atMost):
        return self._roleService.addStoreWeightPurchaseRule(userId, storeId, atLeast, atMost)

    def addCategoryWeightPurchaseRule(self, userId, storeId, category, atLeast, atMost):
        return self._roleService.addCategoryWeightPurchaseRule(userId, storeId, category, atLeast, atMost)

    def addProductWeightPurchaseRule(self, userId, storeId, productId, atLeast, atMost):
        return self._roleService.addProductWeightPurchaseRule(userId, storeId, productId, atLeast, atMost)

    def addCompositeRulePurchaseAnd(self, userId, storeId, rId1, rId2):
        return self._roleService.addCompositeRulePurchaseAnd(userId, storeId, rId1, rId2)

    def addCompositeRulePurchaseOr(self, userId, storeId, rId1, rId2):
        return self._roleService.addCompositeRulePurchaseOr(userId, storeId, rId1, rId2)

    def removeRulePurchase(self, userId, storeId, rId):
        return self._roleService.removeRulePurchase(userId, storeId, rId)

    def appoint_owner_perm(self, store_id, assigner_id, assignee_name):
        return self._roleService.setAppointOwnerPermission(store_id, assigner_id, assignee_name)

    def set_roles_info_perm(self, store_id, assigner_id, assignee_name):
        return self._roleService.setRolesInformationPermission(store_id, assigner_id, assignee_name)

    def set_purchase_history_info_perm(self, store_id, assigner_id, assignee_name):
        return self._roleService.setPurchaseHistoryInformationPermission(store_id, assigner_id, assignee_name)

    def set_discount_perm(self, store_id, assigner_id, assignee_name):
        return self._roleService.setDiscountPermission(store_id, assigner_id, assignee_name)

    def remove_member(self, admin_name, member_name):
        return self._roleService.removeMember(admin_name, member_name)

    def get_all_store_trans(self, admin_name):
        return self._roleService.getAllStoreTransactions(admin_name)

    def get_all_user_trans(self, admin_name):
        return self._roleService.getAllUserTransactions(admin_name)

    def get_user_tran(self, admin_name, tran_id):
        return self._roleService.getUserTransaction(admin_name, tran_id)

    def get_store_tran_by_store_id(self, admin_name, store_id):
        return self._roleService.getStoreTransactionByStoreId(admin_name, store_id)

    def get_all_rules(self, user_id, store_id):
        return self._roleService.getAllRules(user_id, store_id)











