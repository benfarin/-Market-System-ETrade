from interface import implements
import IUserBridge


class UserRealBridge(implements(IUserBridge)):
    def __init__(self, user_service, market_service):
        self._user_service = user_service
        self._market_service = market_service

    def login_guest(self):
        return self._user_service.login_member()

    def register(self, username, password, phone, account_number, branch, country,
                 city, street, apartment_num, bank, ICart):
        return self._user_service.memberSignUp(username, password, phone, account_number, branch,
                                               country, city, street, apartment_num, bank, ICart)

    def login_member(self, user_id, password):
        return self._user_service.memberLogin(user_id, password)

    def add_product_to_cart(self, user_id, store_id, product_id, quantity):
        return self._market_service.addProductToCart(user_id, store_id, product_id, quantity)

    def purchase_product(self, user_id, account_num, branch):
        return self._market_service.purchaseCart(user_id, account_num, branch)

    def logout_member(self, user_id):
        return self._user_service.logoutMember(user_id)

    def open_store(self, store_name, founder_id, account_num, branch, country, city, street, appartment_num, zip_code):
        return self._market_service.createStore(store_name, founder_id, account_num, branch, country, city, street, appartment_num, zip_code)

