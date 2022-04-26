from interface import implements
from AcceptanceTests.Bridges.MarketBridge.IMarketBridge import IMarketBridge


class MarketRealBridge(implements(IMarketBridge)):
    def __init__(self, market_service):
        self._market_service = market_service

    def request(self):
        print("RealSubject: Handling request.")

    def search_product_category(self, category):
        return self._market_service.getProductByCatagory(category)

    def search_product_name(self, product_name):
        return self._market_service.getProductByName(product_name)

    def search_product_keyWord(self, keyWord):
        return self._market_service.getProductsByKeyword(keyWord)

    def search_product_price_range(self, price_min, price_max):
            return self._market_service.getProductPriceRange(price_min, price_max)

    def add_product(self, store_id, user_id, name, price, category, keyWords):
        return self._market_service.addProductToStore(store_id, user_id, name, price, category, keyWords)

    def remove_product(self, store_id, user_id, prod_id):
        return self._market_service.removeProductFromStore(store_id, user_id, prod_id)

    def edit_product_price(self, store_id, user_id, prod_id, new_price):
        return self._market_service.editProductPriceFromStore(store_id, user_id, prod_id, new_price)

    def appoint_store_owner(self, store_id, assigner_id, assignee_id):
        return self._market_service.appointOwnerToStore(store_id, assigner_id, assignee_id)

    def appoint_store_manager(self, store_id, assigner_id, assignee_id):
        return self._market_service.appointManagerToStore(store_id, assigner_id, assignee_id)

    def set_stock_manager_perm(self, store_id, assigner_id, assignee_id):
        return self._market_service.setStockManagerPermission(store_id, assigner_id, assignee_id)

    def set_change_perm(self, store_id, assigner_id, assignee_id):
        return self._market_service.setChangePermission(store_id, assigner_id, assignee_id)

    def close_store(self, store_id):
        pass

    # def get_store_info(self, store_id):
    #     pass

    # def edit_product_name(self, store_id, prod_id, new_name):
    #     pass
    #
    # def edit_product_category(self, store_id, prod_id, new_category):
    #     pass

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

