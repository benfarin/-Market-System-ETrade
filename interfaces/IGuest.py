from interface import  implements,Interface
import IUser
class Guest(Interface,IUser):
    def login(self,name):
        pass

    def logout(self):
        pass

