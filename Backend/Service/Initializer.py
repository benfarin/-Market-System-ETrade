import django, os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Frontend.settings')
django.setup()

from Backend.Service.MemberService import MemberService
from Backend.Service.RoleService import RoleService
from Backend.Service.UserService import UserService
from django.conf import settings


class Initializer:
    def __init__(self):
        self.__roleService = RoleService()
        self.__memberService = MemberService()
        self.__userService = UserService()
        self.__userService.systemManagerSignUp(settings.ADMIN_USERNAME, settings.ADMIN_PASSWORD, "0500000000", 999, 0, "Israel", "Be'er Sheva",
                                               "Ben-Gurion", 0, 999999)

    def getRoleService(self):
        return self.__roleService

    def getMemberService(self):
        return self.__memberService

    def getUserService(self):
        return self.__userService
