from interface import implements
import IUserBridge
from AcceptanceTests.Bridges.UserBridge import UserRealBridge


class UserProxyBridge(implements(IUserBridge)):
    def __init__(self, real_subject: UserRealBridge):
        self._real_subject = real_subject

    def request(self) -> bool:
        if self.check_access():
            self._real_subject.request()
        else:
            return True

    def check_access(self):
        return self._real_subject is None

    def register(self, username, password, phone, address, bank, cart):
        if self.check_access():
            return True
        else:
            return self._real_subject.register(username, password, phone, address, bank, cart)

    def login_guest(self):
        if self.check_access():
            return True
        else:
            return self._real_subject.login()

    def login(self, user_id, password):
        if self.check_access():
            return True
        else:
            return self._real_subject.login(user_id, password)

    def add_product(self, username, product_id, store_id, quantity):
        if self.check_access():
            return True
        return self._real_subject.add_product(username, product_id, store_id, quantity)

    def get_cart_info(self, username):
        if self.check_access():
            return True
        return self._real_subject.get_cart_info(username)

    def purchase_product(self, username, product_ID, quantity):
        if self.check_access():
            return True
        return self._real_subject.purchase_product(username, product_ID, quantity)

