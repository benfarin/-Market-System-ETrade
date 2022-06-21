import string
import random

from locust import HttpUser, task, between



class User_Class1(HttpUser):
    @task
    def home_page(self):
        self.client.get("/")

class User_Class2(HttpUser):

    @task
    def register(self):
        self.client.get("/")
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(5))
        # register
        self.client.post("/signup/", {
            "username" : result_str,
            "password" : "1234" ,
            "phone" : "05400000",
            "account_num" : 1,
            "branch_num" : 1,
            "country" : "Israel",
            "city" : "Mitzpe Ramon",
            "street" : "A",
            "apartment_num" : 1,
            "zip_code" : 1,
        })

class User_Class3(HttpUser):

    @task
    def login(self):
        # home-page
        self.client.get("/")
        # random user name
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(5))
        # register
        self.client.post("/signup/", {
            "username" : result_str,
            "password" : "1234" ,
            "phone" : "05400000",
            "account_num" : 1,
            "branch_num" : 1,
            "country" : "Israel",
            "city" : "Mitzpe Ramon",
            "street" : "A",
            "apartment_num" : 1,
            "zip_code" : 1,
        })
        # login
        self.client.post("/login/", {
            "username": result_str,
            "password": "1234",
        })

class User_Class4(HttpUser):
    @task
    def open_store(self):
        # home-page
        self.client.get("/")
        # random user name
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(5))
        # register
        self.client.post("/signup/", {
            "username" : result_str,
            "password" : "1234" ,
            "phone" : "05400000",
            "account_num" : 1,
            "branch_num" : 1,
            "country" : "Israel",
            "city" : "Mitzpe Ramon",
            "street" : "A",
            "apartment_num" : 1,
            "zip_code" : 1,
        })
        # login
        self.client.post("/login/", {
            "username": result_str,
            "password": "1234",
        })
        # random store-name
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(5))

        self.client.post("/addstore/", {
        "storeName": result_str,
        "accountNumber" : 1,
        "brunch" : 1,
        "country" : "Israel",
        "city" : "Ashkelon",
        "street" : "Ashkeluna",
        "apartment_num" : 1,
        "zip_code" : 11,
        })

class User(HttpUser):
    tasks = [User_Class1, User_Class2, User_Class3, User_Class4]
    wait_time = between(0.5, 2.5)

    # @task
    # def my_stores(self):
    #     self.client.get(f"/storeid?={storeid}")

