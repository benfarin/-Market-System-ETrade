import zope
from AcceptanceTests.Bridges.MarketBridge.IMarketBridge import IMarketBridge
from Service.MemberService import MemberService
from Service.RoleService import RoleService
from Service.UserService import UserService

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

    def get_cart_info(self, user_id):
        return self._userService.getCart(user_id)

    def add_product_to_store(self, store_id, user_id, name, price, category, key_words):
        return self._roleService.addProductToStore(store_id, user_id, name, price, category, key_words)

    def remove_product_from_store(self, store_id, user_id, prod_id):
        return self._roleService.removeProductFromStore(store_id, user_id, prod_id)

    def edit_product_price(self, store_id, user_id, prod_id, new_price):
        return self._roleService.updateProductPrice(store_id, user_id, prod_id, new_price)

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
        return self._roleService.PrintRolesInformation(store_id, user_id)

    def edit_product_name(self,user_id, store_id, prod_id, new_name):
        return self._roleService.updateProductName(user_id, store_id, prod_id, new_name)

    def edit_product_category(self, user_id, store_id, prod_id, new_category):
        return self._roleService.updateProductCategory(user_id, store_id, prod_id, new_category)

    def print_purchase_history(self, store_id, user_id):
        return self._roleService.printPurchaseHistoryInformation(store_id, user_id)





    # def close_store(self, store_id):
    #     return self._market_service.
    # def define_purchase(self, store_id, purchase):
    #     pass
    #
    # def discount_store(self, id, discount):
    #     pass
    #
    # def discount_prod(self, store_id, prod_id, discount):
    #     pass

    # def edit_purchase(self, store_id, new_purchase):
    #     pass
    #
    # def edit_discount(self, store_id, new_discount):
    #     pass

