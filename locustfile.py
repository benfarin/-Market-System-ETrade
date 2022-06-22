import string
import random

from locust import HttpUser, task, between

store_num = 6
prod_num = 9

def random_name():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))
    return result_str

class user_class1(HttpUser):
    @task
    def home_page(self):
        self.client.get("/")

class user_class2(HttpUser):
    @task
    def register(self):
        # home
        self.client.get("/")
        # register
        self.client.post("/signup/", {
            "username" : "user_"+random_name(),
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

class user_class3(HttpUser):

    @task
    def login(self):
        # home-page
        self.client.get("/")
        # register
        username = random_name()
        self.client.post("/signup/", {
            "username" : "user_"+username,
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
            "username": "user_"+username,
            "password": "1234",
        })

class user_class4(HttpUser):
    @task
    def open_store(self):
        global store_num
        # home-page
        self.client.get("/")
        username = random_name()
        # register
        self.client.post("/signup/", {
            "username" : "user_"+username,
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
            "username": "user_"+username,
            "password": "1234",
        })

        self.client.post("/addstore/", {
        "storeName": "store_"+random_name(),
        "accountNumber" : 1,
        "brunch" : 1,
        "country" : "Israel",
        "city" : "Ashkelon",
        "street" : "Ashkeluna",
        "apartment_num" : 1,
        "zip_code" : 11,
        })
        store_num += 1

class user_class5(HttpUser):
    @task
    def open_store_and_add_products(self):
        global store_num, prod_num
        # home-page
        self.client.get("/")
        # random user name
        username = random_name()
        # register
        self.client.post("/signup/", {
            "username" : "user_"+username,
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
            "username": "user_"+username,
            "password": "1234",
        })
        self.client.post("/addstore/", {
        "storeName": "store_"+random_name(),
        "accountNumber" : 1,
        "brunch" : 1,
        "country" : "Israel",
        "city" : "Ashkelon",
        "street" : "Ashkeluna",
        "apartment_num" : 1,
        "zip_code" : 11,
        })
        store_num += 1
        this_store = store_num
        for i in range(10):
            self.client.post("/store/"+str(this_store)+"/addproduct/",{
                "name" : "product_"+random_name(),
                "category" : "category",
                "price" : 20,
                "weight" : 1,
                "keywords" : "juice",
            })
            self.client.post("/store/"+str(this_store)+"/"+str(prod_num)+"/products_manage/quantity/",{
                "quantity": 30,
            })
            prod_num += 1

class User(HttpUser):
    tasks = [user_class1, user_class2, user_class3, user_class4, user_class5]
    wait_time = between(0.5, 2.5)