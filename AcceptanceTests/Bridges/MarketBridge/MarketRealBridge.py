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

    def edit_product_price(self, store_id, user_id, prod_id, new_price):
        return self._roleService.updateProductPrice(store_id, user_id, prod_id, new_price)

    def edit_product_Weight(self, user_id, store_id, prod_id, new_weight):
        return self._roleService.updateProductWeight(user_id, store_id, prod_id, new_weight)

    def appoint_store_owner(self, store_id, assigner_id, assignee_id):
        return self._roleService.appointOwnerToStore(store_id, assigner_id, assignee_id)

    def appoint_store_manager(self, store_id, assigner_id, assignee_id):
        return self._roleService.appointManagerToStore(store_id, assigner_id, assignee_id)

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
        return self._roleService.addSimpleDiscount_Store(userId, storeId, precent)

    def addSimpleConditionDiscount_Store(self, userId, storeId, condition, precent, fromVal, toVal):
        return self._roleService.addSimpleConditionDiscount_Store(userId, storeId, condition, precent, fromVal, toVal)

    def addSimpleDiscount_Category(self, userId, storeId, precent, category):
        return self._roleService.addSimpleDiscount_Category(userId, storeId, precent, category)

    def addSimpleConditionDiscount_Category(self, userId, storeId, precent, condition, category, fromVal, toVal):
        return self._roleService.addSimpleConditionDiscount_Category(userId, storeId, precent, condition, category, fromVal, toVal)

    def addSimpleDiscount_Product(self, userId, storeId, precent, productId):
        return self._roleService.addSimpleDiscount_Product(userId, storeId, precent, productId)

    def addSimpleConditionDiscount_Product(self, userId, storeId, precent, condition, productId, fromVal, toVal):
        return self._roleService.addSimpleConditionDiscount_Product(userId, storeId, precent, condition, productId, fromVal, toVal)

    def addConditionDiscountAdd(self, userId, storeId, dId1, dId2):
        return self._roleService.addConditionDiscountAdd(userId, storeId, dId1, dId2)

    def addConditionDiscountMax(self, userId, storeId, dId1, dId2):
        return self._roleService.addConditionDiscountMax(userId, storeId, dId1, dId2)

    def addConditionDiscountXor(self, userId, storeId, dId, pred1, pred2, decide):
        return self._roleService.addConditionDiscountXor(userId, storeId, dId, pred1, pred2, decide)

    def addConditionDiscountAnd(self, userId, storeId, dId, pred1, pred2):
        return self._roleService.addConditionDiscountAnd(userId, storeId, dId, pred1, pred2)

    def addConditionDiscountOr(self, userId, storeId, dId, pred1, pred2):
        return self._roleService.addConditionDiscountOr(userId, storeId, dId, pred1, pred2)

    def removeDiscount(self,  userId, storeId, discountId):
        return self._roleService.removeDiscount(userId, storeId, discountId)

    def createProductWeightRule(self, uid, sid, pid, less_than, bigger_than):
        return self._roleService.createProductWeightRule(uid, sid, pid, less_than, bigger_than)

    def createStoreWeightRule(self,uid, storeId, less_than, bigger_than):
        return self._roleService.createStoreWeightRule(uid, storeId, less_than, bigger_than)

    def createStoreQuantityRule(self,userId, storeId, less_than, bigger_than):
        return self._roleService.createStoreQuantityRule(userId, storeId, less_than, bigger_than)

    def createCategoryRule(self,userId, storeId, category, less_than, bigger_than):
        return self._roleService.createCategoryRule(userId, storeId, category, less_than, bigger_than)

    def createProductRule(self,userId, storeId, pid, less_than, bigger_than):
        return self._roleService.createProductRule(userId, storeId, pid, less_than, bigger_than)

    def createStoreTotalAmountRule(self, userId, storeId, less_than, bigger_than):
        return self._roleService.createStoreTotalAmountRule(userId, storeId, less_than, bigger_than)


