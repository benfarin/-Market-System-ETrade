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

    def register(self, username, password, phone, account_number, branch, country,
                 city, street, apartment_num, bank, ICart):
        if self.check_access():
            return True
        else:
            return self._real_subject.register(username, password, phone, account_number, branch, country,
                 city, street, apartment_num, bank, ICart)

    def login_guest(self):
        if self.check_access():
            return True
        else:
            return self._real_subject.login_member()

    def login_member(self, user_id, password):
        if self.check_access():
            return True
        else:
            return self._real_subject.login_member(user_id, password)

    def add_product(self, user_id, store_id, product_id, quantity):
        if self.check_access():
            return True
        return self._real_subject.add_product_to_cart(user_id, store_id, product_id, quantity)

    def purchase_product(self, user_id, account_num, branch):
        if self.check_access():
            return True
        return self._real_subject.purchase_product(user_id, account_num, branch)

    def logout_member(self, user_id):
        if self.check_access():
            return True
        else:
            return self._real_subject.logout_member(user_id)
