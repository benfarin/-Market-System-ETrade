from interface import implements
import IUserBridge


class UserRealBridge(implements(IUserBridge)):
    def __init__(self, user_service, market_service):
        self._user_service = user_service
        self._market_service = market_service

    def login_guest(self):
        return self._user_service.login()

    def register(self, username, password, phone, address, bank, cart):
        return self._user_service.memberSignUp(username, password, phone, address, bank, cart)

    def login(self, user_id, password):
        return self._user_service.memberLogin(user_id, password)

    def add_product(self, username, product_id, store_id, quantity):
        return self._user_service.saveProducts(username, product_id, store_id, quantity)

    def purchase_product(self, username, product_ID, quantity):
        return self._user_service.purchase_product(username, product_ID, quantity)

