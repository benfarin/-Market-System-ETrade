import string
import random

from locust import HttpUser, task, between

store_num = 6
user_names = []

def random_name():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(5))
    return result_str

class user_class1(HttpUser):
    # only getting the home page
    @task
    def home_page(self):
        self.client.get("/")

class user_class2(HttpUser):
    # registering the system
    @task
    def register(self):
        global user_names
        # home
        self.client.get("/")
        # register
        username = "user_"+random_name()
        self.client.post("/signup/", {
            "username" : username,
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
        user_names.append(username)

class user_class3(HttpUser):

    @task
    def login(self):
        global user_names
        # home-page
        self.client.get("/")
        # register
        username = "user_"+random_name()
        self.client.post("/signup/", {
            "username" : username,
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
            "username": username,
            "password": "1234",
        })
        user_names.append(username)

class user_class4(HttpUser):
    @task
    def open_store(self):
        global store_num, user_names
        # home-page
        self.client.get("/")
        username = "user_"+random_name()
        # register
        self.client.post("/signup/", {
            "username" : username,
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
            "username": username,
            "password": "1234",
        })
        user_names.append(username)
        # create a store
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
        global store_num, user_names
        # home-page
        self.client.get("/")
        # random user name
        username = "user_"+random_name()
        # register
        self.client.post("/signup/", {
            "username" : username,
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
        user_names.append(username)
        # login
        self.client.post("/login/", {
            "username": username,
            "password": "1234",
        })
        # create a store
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
        # add 10 products to store
        for i in range(10):
            self.client.post("/store/"+str(this_store)+"/addproduct/",{
                "name" : "product_"+random_name(),
                "category" : "category",
                "price" : 20,
                "weight" : 1,
                "keywords" : "juice",
            })
        # self.client.post("/store/"+str(this_store)+"/products_manage/quantity/", {
        #     "quantity" : 30
        # })

class user_class6(HttpUser):
    @task
    def stores_and_appoint(self):
        global store_num, user_names
        # home-page
        self.client.get("/")
        # random user name
        username = "user_" +random_name()
        # register
        self.client.post("/signup/", {
            "username": username,
            "password": "1234",
            "phone": "05400000",
            "account_num": 1,
            "branch_num": 1,
            "country": "Israel",
            "city": "Mitzpe Ramon",
            "street": "A",
            "apartment_num": 1,
            "zip_code": 1,
        })
        # login
        self.client.post("/login/", {
            "username": username,
            "password": "1234",
        })
        # create a store
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
        # appoint another store owner
        self.client.post("/store/"+str(this_store)+"/appoint_owner/",{
            "assignee_name" : user_names[random.randint(0,len(user_names))]
        })
        user_names.append(username)
        # # create another store
        # self.client.post("/addstore/", {
        # "storeName": "store_"+random_name(),
        # "accountNumber" : 1,
        # "brunch" : 1,
        # "country" : "Israel",
        # "city" : "Ashkelon",
        # "street" : "Ashkeluna",
        # "apartment_num" : 1,
        # "zip_code" : 11,
        # })
        # store_num += 1

# class user_class7(HttpUser):
#     @task
#     def ap

class User(HttpUser):
    tasks = [user_class1, user_class2, user_class3, user_class4, user_class5, user_class6]
    wait_time = between(0.5, 2.5)

    # @task
    # def my_stores(self):
    #     self.client.get(f"/storeid?={storeid}")

