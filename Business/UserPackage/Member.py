from Business.UserPackage.User import User
import bcrypt
import threading
from concurrent.futures import Future


def call_with_future(fn, future, args, kwargs):
    try:
        result = fn(*args, **kwargs)
        future.set_result(result)
    except Exception as exc:
        future.set_exception(exc)


def threaded(fn):
    def wrapper(*args, **kwargs):
        future = Future()
        threading.Thread(target=call_with_future, args=(fn, future, args, kwargs)).start()
        return future.result()

    return wrapper


class Member(User):
    def __init__(self, userName, password, phone, address, bank):
        super().__init__()  # extend the constructor of user class
        self.__isLoggedIn = False
        self.__userName = userName  # string
        self.__password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())  # string
        self.__phone = phone  # string
        self.__address = address  # type address class
        self.__bank = bank  # type bank

    def setLoggedIn(self, state):
        self.__isLoggedIn = state

    def addProductRating(self, productID, rating):
        pass

    def getPassword(self):
        return self.__password

    def getBank(self):
        return self.__bank

    def getUserName(self):
        return self.__userName

    def addStoreRating(self, storeID, rating):
        pass
