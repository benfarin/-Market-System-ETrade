from Business.UserManagment import UserManagment
from interfaces import IUser
class UserService:
    def __init__(self):
        self.__userManagment : IUser = UserManagment()
