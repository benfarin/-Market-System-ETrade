from Backend.Business.UserPackage.User import User
from ModelsBackend.models import UserModel
import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Frontend.settings")
django.setup()

class Guest(User):
    def __init__(self):
        super().__init__()
        self.__g = UserModel(userid=super().getUserID(), cart=super().getCart().getModel())
        self.__g.save()