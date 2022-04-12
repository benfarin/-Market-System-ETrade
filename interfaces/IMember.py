from interface import  implements,Interface
import IUser
class Member(Interface,IUser):
    def login(self,name,password):
        pass

    def logout(self,name): # if the member logout,  maybe he want a new name to be guest, we call to login of guest after we finish all the proccess of logout the member.
        pass