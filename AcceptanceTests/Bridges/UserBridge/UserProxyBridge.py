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

    def register(self, username, password, confirm_pass, email):
        if self.check_access():
            return True
        else:
            return self._real_subject.register(username, password, confirm_pass, email)

    def login(self, username, password):
        if self.check_access():
            return True
        else:
            return self._real_subject.login(username, password)

    def add_product(self, product_id, store_id, quantity):
        if self.check_access():
            return True
        return self._real_subject.add_product(product_id, store_id, quantity)

    def get_cart_info(self, username):
        if self.check_access():
            return True
        return self._real_subject.get_cart_info(username)

    def purchase_product(self, username, product_ID, quantity):
        if self.check_access():
            return True
        return self._real_subject.purchase_product(username, product_ID, quantity)

