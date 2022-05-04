import zope
from interface import implements

from AcceptanceTests.Bridges.UserBridge.IUserBridge import IUserBridge
from Service.MemberService import MemberService
from Service.RoleService import RoleService
from Service.UserService import UserService
from interface import implements

@zope.interface.implementer(IUserBridge)
class UserRealBridge:
    def __init__(self, user_service, market_service):
        self._userService = UserService()
        self._roleService = RoleService()
        self._memberService = MemberService()

    def request(self) -> bool:
        if self.check_access():
            self._real_subject.request()
        else:
            return True

    def login_guest(self):
        return self._userService.enterSystem()

    def register(self, username, password, phone, account_number, branch, country,
                 city, street, apartment_num, zip_code):
        return self._userService.memberSignUp(username, password, phone, account_number, branch,
                                               country, city, street, apartment_num, zip_code)

    def login_member(self, user_name, password):
        return self._userService.memberLogin(user_name, password)

    def add_product_to_cart(self, user_id, store_id, product_id, quantity):
        return self._userService.addProductToCart(user_id, store_id, product_id, quantity)

    def purchase_product(self, user_id, account_num, branch):
        return self._userService.purchaseCart(user_id, account_num, branch)

    def logout_member(self, user_id):
        return self._memberService.logoutMember(user_id)

    def open_store(self, store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code):
        return self._memberService.createStore(store_name, founder_id, account_num, branch, country, city, street, apartment_num, zip_code)

    def appoint_system_manager(self, userName, password, phone, accountNumber, brunch, country, city, street, apartmentNum, zipCode):
        return self._userService.systemManagerSignUp(userName, password, phone, accountNumber, brunch, country, city, street, apartmentNum, zipCode)

