import string
import random

from locust import HttpUser, task, between

class LoadNStressTests(HttpUser):

    wait_time = between(0.5, 2.5)

    def on_start(self):
        letters = string.ascii_lowercase
        result_str = ''.join(random.choice(letters) for i in range(5))
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
        # self.client.post("/login/", {
        #     "username": result_str,
        #     "password": "1234",
        # })




